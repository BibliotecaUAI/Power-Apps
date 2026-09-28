# Propuesta — Menú, Préstamo y Devolución (ficticios)

Todo dentro de la misma app, horizontal, **negro y plateado** (sin rojos).
El **moroso** se distingue con un **borde rojo destellante** (tarjeta del usuario y fila en devolución).
Préstamos y devoluciones son **ficticios**: se anotan en Excel, no en FOLIO. Sin reservas.

Bocetos: `prestamo/boceto/` (inicio, menú, préstamo, moroso, devolución).

## Plazos (hoja `Plazos` del Excel, se pueden editar)

| Tipo de material | Días |
|---|---|
| Libro | 28 |
| iPad | 14 |
| Kindle | 28 |
| Calculadora / Test / Mapa | 1 |
| Colección histórica | Solo sala (no se presta) |

El tipo se toma de FOLIO (tipo de material / ubicación). Hay que confirmar los nombres exactos que usa FOLIO.

## Identificar al usuario

- Digitar el **RUT**, o
- **Escanear el QR de la cédula de identidad** con la cámara: el QR trae el RUN, la app lo extrae sola.
- Datos del usuario (nombre, apellido, nombre sugerido, unidad académica, programa, correo):
  desde **FOLIO** (hay que agregar la tabla de usuarios al Power BI) o, mientras tanto,
  desde la hoja `Usuarios` del Excel.

## Correos

- **Al prestar:** resumen del préstamo al correo del usuario (libros + fechas de vencimiento).
- **Morosos:** flujo de Power Automate cada mañana → a cada moroso, un correo con el detalle
  de lo vencido (como el del dashboard de servicios).
- En pruebas, todos los correos van a una dirección de prueba.

## Excel `prestamo/Prestamos_Ficticios.xlsx`

- `tblUsuarios`: RUT, Nombre, Apellido, NombreSugerido, TipoUsuario, UnidadAcademica, Programa, Correo
- `tblPrestamos`: IdPrestamo, RUT, Nombre, Apellido, NombreSugerido, UnidadAcademica, Programa, Correo,
  CodigoBarra, Titulo, TipoMaterial, Biblioteca, FechaPrestamo, FechaVencimiento, FechaDevolucion,
  Estado, DiasAtraso, CorreoEnviado, RegistradoPor, Observaciones
- `tblPlazos`: TipoMaterial, Dias, SoloSala

Nombres de columnas sin espacios a propósito (lección aprendida con el conector Excel).

## Orden de trabajo

1. Aprobar boceto.
2. Subir el Excel a SharePoint y conectarlo a la app.
3. Menú + Inicio (y el menú en Descarte).
4. Préstamo (con QR de cédula y correo de resumen).
5. Devolución (1 a 1 / masiva).
6. Flujo de correo a morosos.
7. Panel.
