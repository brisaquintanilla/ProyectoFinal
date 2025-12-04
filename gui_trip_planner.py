import tkinter as tk
from tkinter import messagebox
from datetime import date

from trip_planner import parse_date, days_inclusive, suggest_activities, format_plan


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

        lbl_start = tk.Label(self.master, text="Fecha inicio (YYYY-MM-DD):", bg=self.bg, fg=self.fg)
        lbl_start.grid(row=1, column=0, sticky="e", padx=(pad, 4), pady=6)
        self.entry_start = tk.Entry(self.master)
        self.entry_start.grid(row=1, column=1, sticky="w", padx=(4, pad), pady=6)

        lbl_end = tk.Label(self.master, text="Fecha fin (YYYY-MM-DD):", bg=self.bg, fg=self.fg)
        lbl_end.grid(row=2, column=0, sticky="e", padx=(pad, 4), pady=6)
        self.entry_end = tk.Entry(self.master)
        self.entry_end.grid(row=2, column=1, sticky="w", padx=(4, pad), pady=6)

        self.btn_generate = tk.Button(self.master, text="Generar plan", bg=self.accent, command=self.on_generate)
        self.btn_generate.grid(row=3, column=0, columnspan=2, pady=(6, pad))

        lbl_result = tk.Label(self.master, text="Plan sugerido:", bg=self.bg, fg=self.fg)
        lbl_result.grid(row=4, column=0, columnspan=2, sticky="w", padx=pad)

        self.text = tk.Text(self.master, width=40, height=10)
        self.text.grid(row=5, column=0, columnspan=2, padx=pad, pady=(0, pad))
        self.text.configure(state="disabled")

        # Ajustes de grid para que se vea mejor
        for i in range(2):
            self.master.grid_columnconfigure(i, weight=1)

    def on_generate(self):
        start_s = self.entry_start.get().strip()
        end_s = self.entry_end.get().strip()
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
        text = f"Has planeado {days} día(s) en el destino (desde {start} hasta {end}).\n\n"
        text += format_plan(plan)

        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, text)
        self.text.configure(state="disabled")


def main():
    root = tk.Tk()
    app = TripPlannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
