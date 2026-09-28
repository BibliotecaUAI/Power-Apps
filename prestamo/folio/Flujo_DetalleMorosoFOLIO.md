# Flujo "DetalleMorosoFOLIO" (detalle de morosidad de una persona)

Copia de **BuscarUsuarioFOLIO**: **Guardar como** → `DetalleMorosoFOLIO`.

1. **ConsultaPBI:** borrar y pegar la consulta de `DAX_detalle_moroso_una_linea.txt`.
   Reemplazar las letras `RUT_AQUI` (dejando las comillas) por el contenido dinámico **codigo**.
2. **Respond:** igual que en los otros flujos (no se toca).
3. **Guardar** → probar con un RUT moroso → en la app: **Power Automate → Agregar flujo → DetalleMorosoFOLIO**.

Devuelve: rut, nombre, apellido, correo, tipo y la lista de libros vencidos
(título, código, biblioteca, fecha de vencimiento, días de atraso), ordenada por días de atraso.
