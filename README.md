# Power Apps — Bibliotecas UAI

No hay que instalar nada ni crear flujos nuevos: todo usa el flujo que ya funciona
**`Copiade:BuscarLibroFOLIO`** (consulta DAX al Power BI).

## 1. App Descarte — dos pantallas

Arriba a la izquierda hay un **interruptor**: bolita a la izquierda = **Lectura 1 a 1**,
bolita a la derecha = **Lectura masiva**.

### Instalar (una vez)

1. Abre la app en Power Apps → **Editar**.
2. Presiona **Guardar** (es tu respaldo).
3. En la lista de pantallas (izquierda), borra **scrDescarteB**.
4. Abre `descarte/Pantalla_1_Lectura_1a1.txt` → selecciona todo (**Ctrl+A**) → **Ctrl+C**.
5. En Power Apps, clic derecho en la lista de pantallas → **Pegar**.
6. Repite los pasos 4 y 5 con `descarte/Pantalla_2_Lectura_Masiva.txt`.
7. Presiona **Guardar**.
8. (Opcional) Agrega la cámara: `descarte/Paso_Camara.md`.

### Usar la lectura masiva

1. Mueve el interruptor a **Lectura masiva**.
2. Elige Biblioteca, Inventario, Criterio y Justificación.
3. Pega los códigos en el cuadro (desde Excel, Word o como sea) o escanéalos.
4. Presiona **1 · BUSCAR EN FOLIO** y espera (puede tardar unos minutos).
5. Revisa la lista de la derecha.
6. Presiona **2 · GUARDAR EN LA FICHA**.

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
