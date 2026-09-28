# Flujo "BuscarLoteFOLIO" (busca hasta 200 códigos en una sola consulta)

1. Power Automate → flujo **Copiade:BuscarLibroFOLIO** → **⋯ → Guardar como** → nombre exacto: `BuscarLoteFOLIO`.
2. Abrir el flujo nuevo → acción **ConsultaPBI** → borrar la consulta → pegar `DAX_BuscarLoteFOLIO.txt`.
3. Borrar las letras `CODIGOS_AQUI` (dejar las comillas) y poner el contenido dinámico del desencadenador (**codigo**).
4. La acción **Responder a PowerApps** queda igual. **Guardar**.
5. En la app: **Power Automate → Agregar flujo → BuscarLoteFOLIO**.

La app le manda 200 códigos separados por coma y el flujo devuelve todos sus datos de una vez.
