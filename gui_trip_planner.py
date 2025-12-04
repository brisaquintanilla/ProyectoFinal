import tkinter as tk
from tkinter import messagebox
from datetime import date
import webbrowser
from urllib.parse import quote_plus

try:
    from tkcalendar import DateEntry  # optional; pip install tkcalendar
    TKCAL_AVAILABLE = True
except Exception:
    TKCAL_AVAILABLE = False

from trip_planner import parse_date, days_inclusive, suggest_activities


class TripPlannerGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Planificador de Viajes")
        master.configure(bg="#2B6CB0")

        # Colores: azul de fondo, blanco para texto y amarillo para botones/accentos
        self.bg = "#2B6CB0"
        self.fg = "#FFFFFF"
        self.accent = "#FFDD57"

        self._build_ui()

    def _build_ui(self):
        pad = 10

        header = tk.Label(self.master, text="Planificador de Viajes", bg=self.bg, fg=self.fg, font=(None, 16, "bold"))
        header.grid(row=0, column=0, columnspan=2, pady=(pad, 0), padx=pad)

        lbl_start = tk.Label(self.master, text="Fecha inicio:", bg=self.bg, fg=self.fg)
        lbl_start.grid(row=1, column=0, sticky="e", padx=(pad, 4), pady=6)
        if TKCAL_AVAILABLE:
            self.entry_start = DateEntry(self.master, date_pattern='y-mm-dd')
        else:
            self.entry_start = tk.Entry(self.master)
        self.entry_start.grid(row=1, column=1, sticky="w", padx=(4, pad), pady=6)

        lbl_end = tk.Label(self.master, text="Fecha fin:", bg=self.bg, fg=self.fg)
        lbl_end.grid(row=2, column=0, sticky="e", padx=(pad, 4), pady=6)
        if TKCAL_AVAILABLE:
            self.entry_end = DateEntry(self.master, date_pattern='y-mm-dd')
        else:
            self.entry_end = tk.Entry(self.master)
        self.entry_end.grid(row=2, column=1, sticky="w", padx=(4, pad), pady=6)

        if not TKCAL_AVAILABLE:
            hint = tk.Label(self.master, text="(Para selector de fecha instala: pip3 install tkcalendar)", bg=self.bg, fg=self.fg, font=(None, 8))
            hint.grid(row=3, column=0, columnspan=2, pady=(0,6))
            loc_row = 4
        else:
            loc_row = 3

        lbl_location = tk.Label(self.master, text="Destino / Ciudad:", bg=self.bg, fg=self.fg)
        lbl_location.grid(row=loc_row, column=0, sticky="e", padx=(pad, 4), pady=6)
        self.entry_location = tk.Entry(self.master)
        self.entry_location.grid(row=loc_row, column=1, sticky="w", padx=(4, pad), pady=6)

        self.btn_generate = tk.Button(self.master, text="Generar plan", bg=self.accent, command=self.on_generate)
        self.btn_generate.grid(row=loc_row+1, column=0, columnspan=2, pady=(6, pad))

        lbl_result = tk.Label(self.master, text="Plan sugerido:", bg=self.bg, fg=self.fg)
        lbl_result.grid(row=5, column=0, columnspan=2, sticky="w", padx=pad)

        # Frame donde mostraremos el plan con botones clicables
        self.frame_plan = tk.Frame(self.master, bg=self.bg)
        self.frame_plan.grid(row=6, column=0, columnspan=2, padx=pad, pady=(0, pad), sticky="nsew")

        # Ajustes de tamaño
        self.frame_plan.grid_columnconfigure(0, weight=1)
        for i in range(2):
            self.master.grid_columnconfigure(i, weight=1)

    def on_generate(self):
        start_s = self.entry_start.get().strip()
        end_s = self.entry_end.get().strip()
        location = self.entry_location.get().strip()
        try:
            start = parse_date(start_s)
            end = parse_date(end_s)
        except ValueError as e:
            messagebox.showerror("Fecha inválida", str(e))
            return

        if end < start:
            messagebox.showerror("Fechas", "La fecha de fin es anterior a la fecha de inicio.")
            return

        days = days_inclusive(start, end)
        plan = suggest_activities(days)

        # Limpiar frame
        for child in self.frame_plan.winfo_children():
            child.destroy()

        header = tk.Label(self.frame_plan, text=f"Has planeado {days} día(s) en {location} (desde {start} hasta {end}).", bg=self.bg, fg=self.fg)
        header.grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Mapeo de lugares específicos para combinaciones ciudad+actividad
        # Las claves usan lower() tal como se calcula arriba
        special_places = {
            ("astana", "monumentos"): "Baiterek, Astana",
            ("paris", "cafés"): "Café de Flore, Paris",
            ("paris", "museos"): "Louvre, Paris",
            ("paris", "monumentos"): "Tour Eiffel, Paris",
            ("tokyo", "museos"): "Tokyo National Museum",
            ("new york", "cafés"): "Blue Bottle Coffee, New York",
            ("london", "monumentos"): "Big Ben, London",
        }

        row = 1
        for day, acts in plan.items():
            lbl_day = tk.Label(self.frame_plan, text=f"Día {day}:", bg=self.bg, fg=self.fg)
            lbl_day.grid(row=row, column=0, sticky="w", pady=2)
            col = 1
            for act in acts:
                # determinar destino específico o búsqueda genérica
                key = (location.lower(), act.lower())
                if key in special_places:
                    query = special_places[key]
                else:
                    query = f"{act} in {location}" if location else act

                url = f"https://www.google.com/maps/search/{quote_plus(query)}"
                btn = tk.Button(self.frame_plan, text=act, bg=self.accent, command=lambda u=url: webbrowser.open(u))
                btn.grid(row=row, column=col, padx=6, sticky="w")
                col += 1
            row += 1


def main():
    root = tk.Tk()
    app = TripPlannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
