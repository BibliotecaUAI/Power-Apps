# Power Apps — Bibliotecas UAI

No hay que instalar nada ni crear flujos nuevos: todo usa el flujo que ya funciona
**`Copiade:BuscarLibroFOLIO`** (consulta DAX al Power BI).

## 1. App Descarte de Libros UAI — pantallas en `pantallas/`

| Archivo | Pantalla |
|---|---|
| `1_Inicio.txt` | scrInicio (menú + 4 tarjetas) |
| `2_Descarte_1a1.txt` | scrDescarteB |
| `3_Descarte_Masiva.txt` | scrDescarteMasiva |
| `4_Prestamo.txt` | scrPrestamo (en construcción) |
| `5_Devolucion.txt` | scrDevolucion (en construcción) |
| `6_Panel.txt` | scrPanel (en construcción) |

Todas llevan el menú lateral. Datos: `tblFichaDescarte` y las tablas de
`prestamo/Prestamos_Ficticios.xlsx` (`tblPrestamos`, `tblUsuarios`, `tblPlazos`).
Cámara: `descarte/Paso_Camara.md`.

## 2. App Préstamo de prueba — `prestamo-prueba/`

1. Subir `Prestamos_Prueba.xlsx` a OneDrive/SharePoint.
2. Crear **App de lienzo en blanco** → Configuración → Pantalla → tamaño **390 × 844**.
3. **Datos → Agregar datos → Excel Online (Business)** → el archivo → tabla `Prestamos_Prueba`.
4. **Power Automate → Agregar flujo** → `Copiade:BuscarLibroFOLIO`.
5. Copiar todo `scrPrestamo.pa.yaml` → clic derecho en el árbol → **Pegar**.
6. Borrar `Screen1` y dejar `scrPrestamo` como pantalla de inicio.
7. En `btnDashboard` → OnSelect, poner la URL del informe de Power BI.

Pasos de la app: **carné → ejemplar (se busca en FOLIO) → confirmar → fila en Excel**.

## Si falla al pegar la cámara

Borrar el bloque `barCamara` del texto, pegar el resto, e insertar
**Insertar → Medios → Lector de código de barras** con OnScan:

- Préstamo: `Set(varEntrada, Trim(First(Self.Barcodes).Value)); Select(btnProcesar)`
- Descarte: ver `descarte/Paso_Camara.md` (posición, colores y OnScan).

## Pendiente

- El nombre del usuario no se busca (el Power BI no tiene tabla de usuarios). Si existe
  una, se agrega al flujo.
- Power BI muestra los préstamos nuevos después de la actualización del conjunto de datos.
