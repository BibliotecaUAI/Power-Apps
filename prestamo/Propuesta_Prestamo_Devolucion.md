# Propuesta — Menú, Préstamo y Devolución (ficticios)

Todo dentro de la **misma app** "Descarte de Libros UAI", horizontal, estilo negro/plateado.
Los préstamos y devoluciones son **ficticios**: se anotan en Excel, **no** en FOLIO.
Sin reservas.

## Pantallas (bocetos en `prestamo/boceto/`)

| Pantalla | Qué hace |
|---|---|
| **Menú lateral** | Barra negra a la izquierda con íconos. Al tocar ☰ se abre con los nombres. Marca con una línea plateada dónde estás. |
| **Inicio** | 4 tarjetas: Descarte, Préstamo, Devolución, Panel, con sus números del día. |
| **Préstamo** | 1) carné/RUT → busca al usuario en el Excel de usuarios · 2) escanear libros (se suman a la lista, datos de FOLIO) · 3) vencimiento automático según tipo de usuario → REGISTRAR. |
| **Devolución** | Interruptor 1 a 1 / masiva. Escanear libros → cruza con los préstamos → marca a tiempo / atrasado / no estaba prestado → REGISTRAR. |
| **Panel** | (después) préstamos activos, vencidos, ranking; desde Power BI o el mismo Excel. |

## Excel nuevo: `Prestamos_Ficticios.xlsx`

**Tabla `tblUsuarios`** (la llenas tú con usuarios de prueba)

| Carne | RUT | Nombre | Tipo | Carrera o Unidad | Correo | Habilitado |
|---|---|---|---|---|---|---|
| U-000123 | 20.456.789-K | Martina Rojas Pérez | Pregrado | Ingeniería Comercial | mrojas@alumnos.uai.cl | SI |

**Tabla `tblPrestamos`** (la llena la app)

| IdPrestamo | Carne | Nombre | Codigo de Barra | HRID | Titulo | Biblioteca | Fecha Prestamo | Fecha Vencimiento | Fecha Devolucion | Estado | Dias Atraso | Registrado Por | Observaciones |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

- Préstamo = fila nueva con Estado "Activo".
- Devolución = la app busca la fila Activa de ese código y le pone Fecha Devolucion, Días Atraso y Estado "Devuelto".

**Plazos por tipo de usuario** (a confirmar): Pregrado 7 días · Postgrado 14 · Académico 30 · Funcionario 14.

## Orden de trabajo

1. Tú apruebas el boceto (o pides cambios).
2. Te entrego el Excel listo (`Prestamos_Ficticios.xlsx`) → lo subes a SharePoint.
3. Menú + Inicio (y se agrega el menú a las pantallas de Descarte).
4. Préstamo.
5. Devolución.
6. Panel.
