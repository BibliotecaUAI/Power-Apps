# Flujos de Power Automate — Préstamo de prueba

La app llama a dos flujos con el mismo patrón que ya usa `Copiade:BuscarLibroFOLIO`
en la app de Descarte:

- Disparador **"Cuando Power Apps llama a un flujo (V2)"** con **una entrada de texto** (el código).
- Acción final **"Responder a una aplicación o flujo de Power Apps"** con **una salida de texto llamada `datos`**
  que contiene un JSON serializado.

La app hace `ParseJSON(Flujo.Run(cod).datos)`, así que los nombres de las claves del JSON
tienen que ser exactamente los de este documento.

> **Forma rápida:** en Power Automate abre `BuscarLibroFOLIO` → **Guardar como** →
> renómbralo. Así conservas tal cual la autenticación a FOLIO (URL de Okapi, tenant, token)
> que ya funciona, y solo cambias la consulta y el JSON de respuesta.

Variables que se asumen (usa las mismas que tu flujo actual):

| Nombre       | Ejemplo                                   |
|--------------|-------------------------------------------|
| `okapiUrl`   | `https://okapi-uai.folio.ebsco.com`       |
| `tenant`     | `fs000xxxxx`                              |
| `token`      | salida del paso de login de tu flujo      |

Cabeceras en cada HTTP: `x-okapi-tenant: @{variables('tenant')}`,
`x-okapi-token: @{variables('token')}`, `Accept: application/json`.

> Nunca dejes usuario/contraseña de FOLIO escritos en el flujo: usa variables de entorno
> (soluciones) o Azure Key Vault.

---

## 1. `BuscarUsuarioFOLIO`

**Entrada:** `codigo` (texto) — código de barras del carné.

1. **HTTP – Buscar usuario** (GET)
   ```
   @{variables('okapiUrl')}/users?limit=1&query=@{encodeUriComponent(concat('barcode=="', triggerBody()['text'], '"'))}
   ```
2. **Componer – usuario**
   ```
   @first(body('HTTP_–_Buscar_usuario')?['users'])
   ```
3. **Condición:** `@{outputs('Componer_–_usuario')}` *no es igual a* (vacío)
   - **Sí**
     1. **HTTP – Grupo** (GET)
        ```
        @{variables('okapiUrl')}/groups/@{outputs('Componer_–_usuario')?['patronGroup']}
        ```
     2. **Componer – respuesta**
        ```json
        {
          "encontrado": "SI",
          "id":     "@{outputs('Componer_–_usuario')?['id']}",
          "nombre": "@{outputs('Componer_–_usuario')?['personal']?['firstName']} @{outputs('Componer_–_usuario')?['personal']?['lastName']}",
          "grupo":  "@{coalesce(body('HTTP_–_Grupo')?['desc'], body('HTTP_–_Grupo')?['group'])}",
          "activo": "@{if(equals(outputs('Componer_–_usuario')?['active'], true), 'SI', 'NO')}"
        }
        ```
     3. **Responder a Power Apps** → `datos` = `@{string(outputs('Componer_–_respuesta'))}`
   - **No** → **Responder a Power Apps** → `datos` = `{"encontrado":"NO"}`

**Respuesta esperada:**
```json
{"encontrado":"SI","id":"…","nombre":"Usuario de prueba","grupo":"Estudiante de pregrado","activo":"SI"}
```

---

## 2. `BuscarEjemplarFOLIO`

**Entrada:** `codigo` (texto) — código de barras del ejemplar.

1. **HTTP – Buscar ejemplar** (GET)
   ```
   @{variables('okapiUrl')}/inventory/items?limit=1&query=@{encodeUriComponent(concat('barcode=="', triggerBody()['text'], '"'))}
   ```
2. **Componer – item**: `@first(body('HTTP_–_Buscar_ejemplar')?['items'])`
3. **Condición:** item no vacío
   - **Sí**
     1. **HTTP – Ubicación** (GET) `@{variables('okapiUrl')}/locations/@{outputs('Componer_–_item')?['effectiveLocation']?['id']}`
     2. **HTTP – Biblioteca** (GET) `@{variables('okapiUrl')}/location-units/libraries/@{body('HTTP_–_Ubicación')?['libraryId']}`
     3. **Componer – respuesta**
        ```json
        {
          "encontrado": "SI",
          "hrid":       "@{outputs('Componer_–_item')?['hrid']}",
          "titulo":     "@{outputs('Componer_–_item')?['title']}",
          "ubicacion":  "@{outputs('Componer_–_item')?['effectiveLocation']?['name']}",
          "biblioteca": "@{body('HTTP_–_Biblioteca')?['name']}",
          "estado":     "@{outputs('Componer_–_item')?['status']?['name']}"
        }
        ```
     4. **Responder a Power Apps** → `datos` = `@{string(outputs('Componer_–_respuesta'))}`
   - **No** → `datos` = `{"encontrado":"NO"}`

`estado` se devuelve **en inglés tal como lo entrega FOLIO** (`Available`, `Checked out`, …);
la app lo traduce y solo permite continuar si es `Available`.

**Respuesta esperada:**
```json
{"encontrado":"SI","hrid":"it00000123","titulo":"Título de ejemplo","ubicacion":"Colección general","biblioteca":"Biblioteca Peñalolén","estado":"Available"}
```

---

## Conectar los flujos a la app

En Power Apps Studio: **Power Automate** (panel izquierdo) → **Agregar flujo** →
`BuscarUsuarioFOLIO` y `BuscarEjemplarFOLIO`. Si les pones otro nombre, reemplázalo en
`btnProcesar.OnSelect` (líneas `BuscarUsuarioFOLIO.Run` y `BuscarEjemplarFOLIO.Run`).

## Probar un flujo sin la app

**Probar → Manualmente**, ingresar un código real y revisar que la salida `datos` sea un
JSON válido (pégalo en cualquier validador JSON). Si `nombre` o `titulo` contienen comillas
dobles, el `Componer` de Power Automate las escapa solo; por eso se recomienda armar el JSON
con **Componer** + `string()` y no concatenando texto.
