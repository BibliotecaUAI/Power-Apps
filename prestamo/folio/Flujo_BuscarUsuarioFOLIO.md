# Flujo "BuscarUsuarioFOLIO" (copia del que busca libros)

No hay que tocar el Power BI: usa las tablas que ya existen (`f_users` y `f_loans`, que llena el recolector).
El RUT está en el **código de barras** del usuario (`f_users[us.barcode]`, ej. `10891774-1`).

## Pasos

1. Power Automate → **Mis flujos** → abrir **FolioBuscar** → **…** → **Guardar como** → nombre `BuscarUsuarioFOLIO`.
2. Abrir la copia → **Editar**. Cambiar solo 3 cosas:
   1. **Trigger (Power Apps V2):** renombrar la entrada `codigo` → `rut`.
   2. **ConsultaPBI → Texto de la consulta:** borrar todo y pegar la consulta de abajo.
      Luego seleccionar las letras `RUT_AQUI` (sin borrar las comillas) y reemplazarlas por el
      **contenido dinámico `rut`** del trigger.
   3. **Respond:** dejarlo igual que en FolioBuscar (salida de texto `datos`).
3. **Guardar** y **Activar** el flujo.

## Consulta DAX

```
DEFINE
    VAR r = UPPER(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("RUT_AQUI", ".", ""), "-", ""), " ", ""))
    VAR u = FILTER(f_users, UPPER(SUBSTITUTE(SUBSTITUTE(f_users[us.barcode], ".", ""), "-", "")) = r)
    VAR bc = MAXX(u, f_users[us.barcode])
    VAR tipo = MAXX(TOPN(1, FILTER(f_loans, f_loans[users.RUT] = bc), f_loans[loanDateTime], DESC), f_loans[Tipo de Usuario])
    VAR mor = COUNTROWS(FILTER(f_loans, f_loans[users.RUT] = bc && f_loans[pre_Sub_estado] = "MOROSO"))
    VAR q = UNICHAR(34)
    VAR j = IF(
        COUNTROWS(u) = 0,
        "{" & q & "encontrado" & q & ":" & q & "NO" & q & "}",
        "{" & q & "encontrado" & q & ":" & q & "SI" & q
        & "," & q & "rut" & q & ":" & q & r & q
        & "," & q & "nombre" & q & ":" & q & SUBSTITUTE(MAXX(u, f_users[us.personal.firstName]), q, "'") & q
        & "," & q & "apellido" & q & ":" & q & SUBSTITUTE(MAXX(u, f_users[us.personal.lastName]), q, "'") & q
        & "," & q & "correo" & q & ":" & q & MAXX(u, f_users[us.personal.email]) & q
        & "," & q & "tipoUsuario" & q & ":" & q & tipo & q
        & "," & q & "unidadAcademica" & q & ":" & q & SUBSTITUTE(MAXX(u, f_users[f_usersUnidad.unidadAcademica]), q, "'") & q
        & "," & q & "programa" & q & ":" & q & SUBSTITUTE(MAXX(u, f_users[f_usersUnidad.Programa]), q, "'") & q
        & "," & q & "morososFolio" & q & ":" & q & (mor + 0) & q
        & "}"
    )
EVALUATE ROW("datos", j)
```

Notas:
- **Tipo de usuario** se toma del último préstamo de esa persona en FOLIO (`f_loans`); si nunca ha pedido nada, queda vacío.
- **morososFolio** = cuántos préstamos tiene en estado MOROSO en FOLIO (según el Power BI).
- Si el Respond de FolioBuscar usa otra expresión para sacar `datos`, usar **la misma** en la copia.

## En la app

Power Automate (ícono en la barra izquierda) → **Agregar flujo** → `BuscarUsuarioFOLIO`.
Si Power Apps le pone otro nombre (ej. `'Copiade:BuscarUsuarioFOLIO'`), avisar para ajustar la pantalla.

## QR de la cédula

El QR trae un texto con `RUN=12345678-9&type=...`. La app toma lo que está entre
`RUN=` y `&`. Si se digita el RUT, lo usa tal cual (con o sin puntos y guion).
