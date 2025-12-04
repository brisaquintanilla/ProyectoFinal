Proyecto Final: Planificador de viajes (simple)

Descripción
-----------
Proyecto sencillo en Python para ayudar a planificar viajes. Permite registrar fechas de inicio y fin, calcular la cantidad de días que estarás en un destino y generar sugerencias genéricas de actividades por día (p. ej. "museos", "cafés", "monumentos").

Uso
---
Ejecuta el script con Python 3:

```bash
python3 trip_planner.py --start 2025-12-01 --end 2025-12-05
```

Si no pasas las fechas como argumentos, el programa pedirá las fechas por teclado en formato `YYYY-MM-DD`.

Ejemplo (interactivo):

```
Fecha inicio (YYYY-MM-DD): 2025-12-01
Fecha fin (YYYY-MM-DD): 2025-12-03
Has planeado 3 día(s) en el destino (desde 2025-12-01 hasta 2025-12-03).

Plan sugerido:
Día 1: Museos, Cafés
Día 2: Monumentos, Parques
Día 3: Mercados, Teatros
```

Requisitos
---------
- Python 3.7+

Notas
-----
Este proyecto es intencionalmente simple. Puedo ampliarlo para incluir preferencias del usuario, una base de datos de actividades por ciudad, horarios o integración con APIs públicas si quieres.

Interfaz de escritorio (Tkinter)
-------------------------------
También se incluye una interfaz de escritorio simple basada en `tkinter`.

Ejecutar la GUI:

```bash
python3 gui_trip_planner.py
```

La ventana permite introducir las fechas de inicio y fin en formato `YYYY-MM-DD` y muestra un plan sugerido en un cuadro de texto. La paleta de colores está pensada para una estética de viaje (azul de fondo, texto blanco y acentos en amarillo).
