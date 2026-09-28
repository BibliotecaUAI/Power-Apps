# Generador de las pantallas

Scripts que producen `pantallas/*.txt`. Se ejecutan desde esta carpeta:

    python3 build_all.py

(las rutas de salida apuntan a `/home/user/Power-Apps/pantallas`; `build.py` lee `base.txt`).
- `nav.py`: menú, encabezado, Inicio, transiciones, marcadores.
- `tema.py`: modo claro/oscuro, letra, tamaños, vidrio (post-proceso de todas las pantallas).
- `prestamo.py`, `devolucion.py`, `morosos.py`: pantallas de préstamos.
