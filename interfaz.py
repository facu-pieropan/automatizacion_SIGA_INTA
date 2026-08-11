# Esto solo maneja la parte visual de entrada

import tkinter as tk
from tkinter import ttk, messagebox
import config

def solicitar_parametros():
    root = tk.Tk()
    root.title("Configuración - SIGA INTA")
    root.geometry("400x300")

    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)

    #=================================================================================== Entrada Simplificada
    campos = {"Estación": config.STATION, "Inicio": config.START_DATE, "Fin": config.END_DATE}
    entradas = {}

    for label, val in campos.items():
        ttk.Label(frame, text=f"{label}:").pack(anchor="w")
        e = ttk.Entry(frame, width=35)
        e.pack(fill=tk.X, pady=(0, 10))
        e.insert(0, val)
        entradas[label] = e

    def confirmar():
        config.STATION = entradas["Estación"].get().strip()
        config.START_DATE = entradas["Inicio"].get().strip()
        config.END_DATE = entradas["Fin"].get().strip()
        root.destroy()

    ttk.Button(frame, text="Iniciar", command=confirmar).pack(fill=tk.X, ipady=5)
    root.mainloop()