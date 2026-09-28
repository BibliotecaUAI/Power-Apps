# Power Apps — Bibliotecas UAI

No hay que instalar nada ni crear flujos nuevos: todo usa el flujo que ya funciona
**`Copiade:BuscarLibroFOLIO`** (consulta DAX al Power BI).

## 1. App Descarte — dos pantallas

- `descarte/Pantalla_1_Lectura_1a1.txt` → pantalla `scrDescarteB` (libro por libro).
- `descarte/Pantalla_2_Lectura_Masiva.txt` → pantalla `scrDescarteMasiva` (tanda de códigos).

Arriba a la izquierda, los botones **LECTURA 1 A 1** / **LECTURA MASIVA** cambian de pantalla.

1. Abrir la app en **Editar** → **Guardar** (respaldo).
2. Borrar la pantalla `scrDescarteB`.
3. Copiar todo `Pantalla_1_Lectura_1a1.txt` → clic derecho en el árbol → **Pegar**.
4. Copiar todo `Pantalla_2_Lectura_Masiva.txt` → clic derecho en el árbol → **Pegar**.
5. Agregar la cámara a mano en cada pantalla: ver **`descarte/Paso_Camara.md`**.
6. Guardar.

**Lectura masiva:** escanear (pistola o cámara) o pegar un código por línea →
**1 · BUSCAR EN FOLIO** (máx. 200) → revisar la vista previa (Listo / Ya en ficha /
No en FOLIO) → **2 · GUARDAR N EN LA FICHA**. Solo se guardan los "Listo"; los datos
que no vienen de FOLIO quedan con su valor por defecto (POL vacío, Forma de
adquisición "Desconocida", Bibliografía "Por confirmar", etc.).
Por ahora usa el mismo flujo `Copiade:BuscarLibroFOLIO`, un código a la vez: 100 códigos
pueden tardar 1–3 minutos. El flujo "FolioLote" (una sola consulta) lo hará más rápido.

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
