# Arreglo: los flujos nuevos no devuelven datos

Las consultas nuevas devuelven **una sola columna llamada `datos`**. La caja **Respond** tiene que sacar
exactamente esa columna. Hacer esto en **BuscarUsuarioFOLIO** y en **ListaMorososFOLIO**:

1. Abrir el flujo → **Editar**.
2. Clic en la última caja (**Respond** / *Responder a una aplicación o flujo de Power App*).
3. En la salida **datos**: borrar lo que tenga.
4. Clic en **fx** (Expresión) y pegar:

```
first(body('ConsultaPBI')?['firstTableRows'])?['[datos]']
```

5. **Aceptar / Agregar** → **Guardar**.

Si la caja del medio NO se llama `ConsultaPBI`, cambiar ese nombre en la expresión por el que tenga.

## Probar sin la app
En el flujo: **Probar** → **Manualmente** → escribir en `codigo`:
- BuscarUsuarioFOLIO: un RUT, ej. `10891774-1`
- ListaMorososFOLIO: `todos`

Si termina en verde, abrir la caja **Respond** y ver la salida: debe empezar con `{"encontrado":...` o `{"total":...`.
Si una caja queda en rojo, esa captura dice exactamente qué falla.
