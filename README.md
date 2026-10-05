# Power Apps — Bibliotecas UAI

No hay que instalar nada ni crear flujos nuevos: todo usa el flujo que ya funciona
**`Copiade:BuscarLibroFOLIO`** (consulta DAX al Power BI).

## 1. App Descarte con cámara — `descarte/Pantalla_Descarte_Camara.txt`

1. Abrir la app en **Editar** → **Guardar** (respaldo).
2. Borrar la pantalla `scrDescarteB`.
3. Copiar todo el archivo → clic derecho en el árbol → **Pegar**.
4. Guardar.

Lee códigos con **cámara** (botón CÁMARA), **pistola** o **digitando + Enter**.

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

Borrar el bloque `barCamara` / `barCamara_1` del texto, pegar el resto, e insertar
**Insertar → Medios → Lector de código de barras** con OnScan:

- Préstamo: `Set(varEntrada, Trim(First(Self.Barcodes).Value)); Select(btnProcesar)`
- Descarte: `Set(varEntrada, Trim(First(Self.Barcodes).Value)); Select(btnProcesarEscaneo)`

## Pendiente

- El nombre del usuario no se busca (el Power BI no tiene tabla de usuarios). Si existe
  una, se agrega al flujo.
- Power BI muestra los préstamos nuevos después de la actualización del conjunto de datos.

## Cruce de existencias · Ficha de Descarte PP 2026 (`cruce-existencias/`)

- `Consulta_DAX_Cruce_Existencias.txt`: consulta DAX con los 209 códigos de la ficha que no tienen existencias; trae todos los ejemplares de esos títulos en FOLIO.
- `Flujo_FolioCruceExistencias.txt`: flujo de un solo uso que ejecuta la consulta y deja el resultado como CSV en SharePoint.
- `cruce_existencias.py`: marca 1/0 por biblioteca si existe el mismo número del título (HRID + volumen), con el mismo criterio de las filas ya completas de la ficha, y genera el listado de las filas que faltaban.
