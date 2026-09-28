# Cámara — las dos pantallas de Descarte

El lector de cámara **no se puede pegar desde el texto** (Power Apps lo rechaza),
por eso se inserta a mano, una vez por pantalla. Queda dentro del mismo cuadro
de búsqueda, a la derecha, como en el boceto.

En cada pantalla: **Insertar → Medios → Lector de código de barras**, renombrarlo y
poner estas propiedades en la barra de fórmulas (con `;` y `;;`, porque la app está en español).

## Pantalla 1 · Lectura 1 a 1 → `barCamara_1`

| Propiedad    | Valor |
|--------------|-------|
| X / Y        | `388` / `366` |
| Width / Height | `48` / `44` |
| Text         | `"📷"` |
| Fill         | `ColorValue("#111111")` |
| Color        | `ColorValue("#FFFFFF")` |
| DisplayMode  | `If(varBuscando; DisplayMode.Disabled; DisplayMode.Edit)` |
| OnScan       | `If(!IsBlank(First(Self.Barcodes).Value); Set(varEntrada; Trim(First(Self.Barcodes).Value));; Select(btnProcesarEscaneo))` |

## Pantalla 2 · Lectura masiva → `barCamara_2`

Cada lectura agrega el código como una línea nueva en el cuadro de la tanda.

| Propiedad    | Valor |
|--------------|-------|
| X / Y        | `524` / `354` |
| Width / Height | `48` / `44` |
| Text         | `"📷"` |
| Fill         | `ColorValue("#111111")` |
| Color        | `ColorValue("#FFFFFF")` |
| DisplayMode  | `If(varBuscandoTanda || varGuardandoTanda; DisplayMode.Disabled; DisplayMode.Edit)` |
| OnScan       | `If(!IsBlank(First(Self.Barcodes).Value); Set(varTandaTexto; txtTanda_2.Text & If(IsBlank(txtTanda_2.Text) || EndsWith(txtTanda_2.Text; Char(10)); ""; Char(10)) & Trim(First(Self.Barcodes).Value) & Char(10));; Reset(txtTanda_2))` |

Bordes redondeados (Radius…) en `0`. Luego clic derecho sobre el control →
**Traer al frente**, para que quede encima del cuadro de texto.

## Para no repetir esto a mano

Clic derecho sobre `barCamara_1` → **Copiar** → pegar en el Bloc de notas y enviármelo.
Ahí aparece el nombre exacto del control y lo dejo dentro de los archivos.
