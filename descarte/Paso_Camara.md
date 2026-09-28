# Cámara en el buscador — Descarte

La pantalla `Pantalla_Descarte_Camara.txt` ya trae la búsqueda en un solo lugar:
el botón oculto **`btnProcesarEscaneo`** busca lo que haya en **`varEntrada`**.
La pistola / digitado (`txtEscaneo_1`) ya lo usa. Falta solo poner la cámara en
el hueco que quedó entre el buscador y el botón ESCÁNER.

El lector de cámara **no se puede pegar desde el texto** (Power Apps lo rechaza),
por eso se inserta a mano, una sola vez.

## Pasos

1. Abrir la app en **Editar** → seleccionar la pantalla `scrDescarteB`.
2. **Insertar → Medios → Lector de código de barras**.
3. Renombrarlo **`barCamara_1`** (doble clic en el árbol).
4. Con el control seleccionado, en la barra de fórmulas poner cada propiedad
   (se escribe con `;` y `;;` porque la app está en español):

| Propiedad    | Valor |
|--------------|-------|
| X            | `378` |
| Y            | `322` |
| Width        | `66` |
| Height       | `52` |
| Text         | `"📷"` |
| Fill         | `ColorValue("#111111")` |
| Color        | `ColorValue("#FFFFFF")` |
| HoverFill    | `ColorValue("#3F4247")` |
| DisplayMode  | `If(varBuscando; DisplayMode.Disabled; DisplayMode.Edit)` |
| OnScan       | `If(!IsBlank(First(Self.Barcodes).Value); Set(varEntrada; Trim(First(Self.Barcodes).Value));; Select(btnProcesarEscaneo))` |

   Los bordes redondeados (Radius…) dejarlos en `0` para que calce con el buscador.

5. **Guardar** y probar en el celular / tablet: tocar 📷 → apuntar al código →
   la ficha se llena sola, igual que con la pistola.

## Para no repetir esto a mano

Después de insertarlo, clic derecho sobre `barCamara_1` → **Copiar** → pegar en el
Bloc de notas y enviarme ese texto. Ahí aparece el nombre exacto del control
(p. ej. `BarcodeReader@x.y.z`) y lo dejo dentro del archivo de la pantalla para que
la próxima vez se pegue todo junto.
