# Flujo "ListaMorososFOLIO" (para la pantalla Morosos)

Otra copia del flujo de libros. Devuelve la lista de usuarios morosos (según `f_loans[pre_Sub_estado] = "MOROSO"`
del Power BI), agrupada por RUT, con los 400 de más días de atraso.

## Pasos

1. Power Automate → **FolioBuscar** → **…** → **Guardar como** → `ListaMorososFOLIO`.
2. Abrir la copia → **Editar**:
   1. **Trigger:** dejarlo igual (la entrada `codigo` no se usa, la app manda "todos").
   2. **ConsultaPBI → Texto de la consulta:** borrar todo y pegar la consulta de abajo (no hay nada que reemplazar).
   3. **Respond:** igual que en FolioBuscar.
3. **Guardar** y **Activar**.
4. En la app: **Power Automate → Agregar flujo →** `ListaMorososFOLIO`.

## Consulta DAX

```
DEFINE
    VAR m = FILTER(f_loans, f_loans[pre_Sub_estado] = "MOROSO" && NOT ISBLANK(f_loans[users.RUT]))
    VAR g = GROUPBY(
        m,
        f_loans[users.RUT],
        "n", COUNTX(CURRENTGROUP(), 1),
        "dias", MAXX(CURRENTGROUP(), f_loans[pre_Dias_morosidad]),
        "nombre", MAXX(CURRENTGROUP(), f_loans[users.Nombre]),
        "tipo", MAXX(CURRENTGROUP(), f_loans[Tipo de Usuario]),
        "bib", MAXX(CURRENTGROUP(), f_loans[bibloteca.prestamo])
    )
    VAR primeros = g
    VAR q = UNICHAR(34)
    VAR lista = CONCATENATEX(
        primeros,
        "{" & q & "rut" & q & ":" & q & f_loans[users.RUT] & q
        & "," & q & "nombre" & q & ":" & q & SUBSTITUTE([nombre], q, "'") & q
        & "," & q & "tipo" & q & ":" & q & [tipo] & q
        & "," & q & "bib" & q & ":" & q & [bib] & q
        & "," & q & "n" & q & ":" & q & [n] & q
        & "," & q & "dias" & q & ":" & q & [dias] & q
        & "}",
        ",",
        [dias], DESC
    )
    VAR j = "{" & q & "total" & q & ":" & q & COUNTROWS(g) & q
        & "," & q & "libros" & q & ":" & q & COUNTROWS(m) & q
        & "," & q & "lista" & q & ":[" & lista & "]}"
EVALUATE ROW("datos", j)
```

Los correos a morosos los sigue enviando **tu flujo actual desde Power BI** (la tabla HTML). Esta pantalla es solo para ver y filtrar.


Nota: no usar `top` como nombre de variable (es palabra reservada en DAX).
