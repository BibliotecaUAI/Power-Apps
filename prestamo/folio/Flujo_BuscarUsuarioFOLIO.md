# Flujo "BuscarUsuarioFOLIO" (copia del que busca libros)

La forma más fácil: en Power Automate, abrir **FolioBuscar** → **…** → **Guardar como** →
nombre `BuscarUsuarioFOLIO`. Luego cambiar solo 3 cosas:

1. **Trigger (Power Apps V2):** renombrar la entrada `codigo` → `rut`.
2. **ConsultaPBI → Texto de la consulta:** borrar todo y pegar la consulta de abajo.
   Donde dice `RUT_AQUI`, borrar esas letras e insertar el contenido dinámico **rut** del trigger.
3. **Respond:** igual que en FolioBuscar (salida de texto `datos`).

## Consulta DAX

```
DEFINE
    VAR r = UPPER(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("RUT_AQUI", ".", ""), "-", ""), " ", ""))
    VAR c = LEFT(r, LEN(r) - 1)
    VAR u = FILTER(f_users, f_users[rut] = r || f_users[rutCuerpo] = c || f_users[rutCuerpo] = r)
    VAR q = LEFT(CHAR(34), 1)
    VAR j = IF(
        COUNTROWS(u) = 0,
        "{" & q & "encontrado" & q & ":" & q & "NO" & q & "}",
        "{" & q & "encontrado" & q & ":" & q & "SI" & q
        & "," & q & "rut" & q & ":" & q & MAXX(u, f_users[rut]) & q
        & "," & q & "nombre" & q & ":" & q & MAXX(u, f_users[nombre]) & q
        & "," & q & "apellido" & q & ":" & q & MAXX(u, f_users[apellido]) & q
        & "," & q & "nombreSugerido" & q & ":" & q & MAXX(u, f_users[nombreSugerido]) & q
        & "," & q & "correo" & q & ":" & q & MAXX(u, f_users[correo]) & q
        & "," & q & "tipoUsuario" & q & ":" & q & MAXX(u, f_users[tipoUsuario]) & q
        & "," & q & "unidadAcademica" & q & ":" & q & MAXX(u, f_users[unidadAcademica]) & q
        & "," & q & "programa" & q & ":" & q & MAXX(u, f_users[programa]) & q
        & "," & q & "activo" & q & ":" & q & MAXX(u, f_users[activo]) & q
        & "}"
    )
EVALUATE ROW("datos", j)
```

Si en FolioBuscar el Respond usa otra expresión para sacar `datos`, usar **la misma**
(normalmente: `first(body('ConsultaPBI')?['results'][0]['tables'][0]['rows'])?['[datos]']`).

## En la app

Power Automate → Agregar flujo → `BuscarUsuarioFOLIO`. Se usará igual que el de libros:
`ParseJSON('BuscarUsuarioFOLIO'.Run(rut).datos)`.

## QR de la cédula

El QR trae un texto con `RUN=12345678-9&type=...`. La app toma lo que está entre
`RUN=` y `&`. Si se escanea otra cosa o se digita, usa el texto tal cual.
