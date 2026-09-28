# Power Apps — Bibliotecas UAI

| Carpeta | Contenido |
|---|---|
| `prestamo-prueba/` | App **Préstamo de prueba**: lee usuario y ejemplar desde FOLIO (vía Power Automate) y registra un préstamo ficticio en Excel (`Prestamos_Prueba`), que alimenta el dashboard de Power BI. |
| `descarte/` | Parche para la app **Descarte de Material**: agrega lectura con **cámara**, además de pistola y digitado. |

Las tres formas de ingreso (cámara, pistola lectora, digitado) pasan por **un único botón
técnico** (`btnProcesar` / `btnProcesarEscaneo`). Así la lógica de consulta a FOLIO existe
una sola vez y se comporta igual venga de donde venga el código.

```
 Cámara (barCamara.OnScan) ─┐
 Pistola (Enter → OnChange) ─┼─► Set(varEntrada, código) ─► Select(btnProcesar) ─► Flujo PA ─► FOLIO
 Digitado (Enter o "Leer") ──┘
```

---

## 1. App "Préstamo de prueba"

### Instalar

1. **Excel**: subir `prestamo-prueba/Prestamos_Prueba.xlsx` a SharePoint/OneDrive.
   Ya trae la tabla **`Prestamos_Prueba`** (todas las columnas en formato texto) y una
   fila de ejemplo `PRUEBA-0000` con estado `Closed`. Puedes borrarla.
2. **Flujos**: crear `BuscarUsuarioFOLIO` y `BuscarEjemplarFOLIO` según
   [`prestamo-prueba/flujos-power-automate.md`](prestamo-prueba/flujos-power-automate.md).
3. **App nueva** (lienzo) → **Configuración → Pantalla → Tamaño personalizado 390 × 844**,
   con *Escalar para ajustar* y *Bloquear relación de aspecto* activados.
4. **Datos → Agregar datos → Excel Online (Business)** → el archivo → tabla `Prestamos_Prueba`.
5. **Power Automate → Agregar flujo** → los dos flujos.
6. Copiar todo el contenido de [`prestamo-prueba/scrPrestamo.pa.yaml`](prestamo-prueba/scrPrestamo.pa.yaml)
   → en **Vista de árbol**, clic derecho → **Pegar** (o Ctrl+V). Se crea `scrPrestamo`.
7. Poner `scrPrestamo` como **StartScreen** y borrar la `Screen1` vacía.
8. En `btnDashboard.OnSelect`, reemplazar la URL por la del informe de Power BI.

### Si el lector de cámara no se pega

El control `BarcodeReader` cambia de versión según el entorno. Si Studio reclama por
`barCamara`:

1. Borra ese bloque del YAML y pega el resto.
2. **Insertar → Medios → Lector de código de barras**. Renómbralo `barCamara` y ubícalo en X 20, Y 382, ancho 350 y alto 52.
3. Pega en sus propiedades:
   - `OnScan` = `Set(varEntrada, Trim(First(Self.Barcodes).Value)); Select(btnProcesar)`
   - `Text` = `"📷  Escanear con cámara"`
   - `Visible` = `(varPaso = "usuario" || varPaso = "ejemplar") && !varBuscando`
4. Opcional: dale fondo `#111111`, texto blanco y radio 12 para que coincida con el boceto.

### Flujo de la pantalla

| `varPaso` | Qué se ve | Qué valida |
|---|---|---|
| `usuario` | Visor, cámara, campo de código | Que el carné exista en FOLIO y que el usuario esté **activo** |
| `ejemplar` | Lo mismo, más la tarjeta del usuario leído (con el botón *Cambiar*) | Que el ejemplar exista, que esté **Available** y que no tenga un préstamo de prueba `Open` en el Excel |
| `confirmar` | Tarjetas de usuario y ejemplar, más las fechas (hoy y hoy + 14 días) | Vuelve a comprobar el duplicado justo antes de guardar |
| `listo` | Resumen de la fila escrita | — |

### Columnas de `Prestamos_Prueba`

`id, userBarcode, userName, userGroup, itemBarcode, itemHrid, itemTitle, library, location,
loanDate, dueDate, returnDate, status, action, operator, createdAt, source`

- Las fechas se guardan como texto ISO (`yyyy-mm-dd`). En Power Query se convierten con
  *Cambiar tipo → Fecha* (configuración regional Inglés/EE. UU. o ISO).
- `library` sale de FOLIO (`/location-units/libraries`) y es la columna para filtrar por
  biblioteca en el dashboard.
- `status` = `Open` al crear. Una devolución de prueba debería poner `Closed` y llenar
  `returnDate`.
- El Excel conector agrega una columna oculta `__PowerAppsId__`. No hay que borrarla.

### Consideraciones

- **Correlativo `PRUEBA-0001…`**: se calcula como el máximo + 1 justo antes de guardar, con
  `Refresh`. Si dos personas registran en el mismo segundo podrían obtener el mismo número.
  Para una prueba es aceptable; en producción conviene usar SharePoint List o Dataverse
  (ID autonumérico).
- **Power BI**: si el informe importa este Excel, un préstamo nuevo aparece recién en la
  siguiente actualización del dataset. Con licencia Pro son 8 actualizaciones al día;
  `PowerBIIntegration.Refresh()` no sirve con Excel (solo con DirectQuery).
- **Cámara dentro del visual de Power BI**: la cámara no siempre está disponible dentro del
  visual embebido. La pistola y el digitado sí funcionan siempre. Para escanear con el
  celular, publica la app también en Power Apps Mobile.

---

## 2. Parche "Descarte de Material": cámara + pistola + digitado

Hoy toda la lógica vive en `txtEscaneo_1.OnChange` y lee `txtEscaneo_1.Text`, por eso solo
funcionan la pistola y el digitado. El parche mueve esa lógica, **sin cambiar su
comportamiento**, a un botón técnico que recibe el código desde cualquiera de las tres
fuentes.

1. En `scrDescarteB`, pega [`descarte/controles-nuevos.pa.yaml`](descarte/controles-nuevos.pa.yaml)
   (clic derecho sobre la pantalla → **Pegar**). Se agregan:
   - `barCamara_1`: botón **CÁMARA** entre el campo de escaneo y *ESCÁNER · ON/OFF*.
   - `btnProcesarEscaneo`: 1 × 1 px, transparente, con la lógica que antes estaba en OnChange.
     Además envuelve la llamada al flujo en `IfError`, para que un fallo del flujo muestre
     el aviso "No se pudo consultar FOLIO" en vez de un error rojo.
2. Cambia estas propiedades de **`txtEscaneo_1`**:
   - `OnChange`:
     ```
     =If(!IsBlank(Trim(Self.Text)), Set(varEntrada, Trim(Self.Text)); Select(btnProcesarEscaneo))
     ```
   - `Width`: `=290` (antes 360), para dejar espacio al botón de cámara.
   - `HintText`: `="Escanee o digite el código y presione Enter…"`
3. Si `BarcodeReader` no se pega, insértalo a mano como en la sección 1 y copia su `OnScan`:
   ```
   =Set(varEntrada, Trim(First(Self.Barcodes).Value)); Select(btnProcesarEscaneo)
   ```

El **modo ráfaga** (`varRafaga`) también funciona con la cámara: si el lote está completo,
cada lectura se guarda sola.
