# Esto procesa la tabla CSV del SIGA descargada por Selenium
# Usa Pandas y Matplotlib para generar el resumne y mostrar el dashboard

import glob
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import config

def get_climate_summary_text(df, col_date, col_precip, col_temp):
    """Genera el texto de resumen estadístico"""
    total_precip = df[col_precip].sum()
    max_precip_day = df.loc[df[col_precip].idxmax()]
    
    mean_temp = df[col_temp].mean()
    max_temp_row = df.loc[df[col_temp].idxmax()]
    min_temp_row = df.loc[df[col_temp].idxmin()]
    
    summary = (
        f"========================================\n"
        f"[{config.STATION}] RESUMEN DEL ANÁLISIS CLIMÁTICO\n"
        f"========================================\n"
        f"• Precipitación Total Acumulada: {total_precip:.1f} mm\n"
        f"• Día más lluvioso: {max_precip_day[col_date].strftime('%d/%m/%Y')} con {max_precip_day[col_precip]:.1f} mm\n"
        f"• Temperatura Media Anual: {mean_temp:.1f} °C\n"
        f"• Temperatura Máxima Absoluta: {max_temp_row[col_temp]:.1f} °C ({max_temp_row[col_date].strftime('%d/%m/%Y')})\n"
        f"• Temperatura Mínima Absoluta: {min_temp_row[col_temp]:.1f} °C ({min_temp_row[col_date].strftime('%d/%m/%Y')})\n"
        f"========================================"
    )
    return summary

def show_dashboard(df, col_date, col_precip, col_temp):
    """Crea la interfaz gráfica con el gráfico y las estadísticas"""
    root = tk.Tk()
    root.title(f"Dashboard Climático - Estación {config.STATION}")
    root.geometry("1350x680")

    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    #=================================================================================== Matplotlib
    fig, ax1 = plt.subplots(figsize=(9, 5.5))
    color_precip = "#2b5c8f"
    ax1.set_xlabel("Fecha del Período", fontsize=11, fontweight='bold', labelpad=8)
    ax1.set_ylabel("Precipitación Acumulada (mm)", color=color_precip, fontsize=11, fontweight='bold')
    ax1.bar(df[col_date], df[col_precip], color=color_precip, alpha=0.8, width=1.0, label="Precipitación [mm]")
    ax1.tick_params(axis="y", labelcolor=color_precip)
    
    ax2 = ax1.twinx()
    color_temp = "#d9534f"
    ax2.set_ylabel("Temperatura Media (°C)", color=color_temp, fontsize=11, fontweight='bold')
    ax2.plot(df[col_date], df[col_temp], color=color_temp, linewidth=1.5, alpha=0.9, label="Temp. Media [°C]")
    ax2.tick_params(axis="y", labelcolor=color_temp)
    
    plt.title(f"Comportamiento Climático — Estación: {config.STATION}", fontsize=13, fontweight='bold', pad=15)
    ax1.grid(True, linestyle=":", alpha=0.6, color="gray")
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    #=================================================================================== Resumen de texo
    right_frame = ttk.Frame(main_frame, padding=10)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=5, pady=5)

    text_box = tk.Text(right_frame, wrap=tk.WORD, width=45, height=18, font=("Courier New", 10))
    text_box.insert("1.0", get_climate_summary_text(df, col_date, col_precip, col_temp))
    text_box.config(state=tk.DISABLED)
    text_box.pack(fill=tk.BOTH, expand=True)

    output_image = f"climate_chart_{config.STATION.lower()}_annual.png"
    plt.savefig(output_image, dpi=300)
    
    root.mainloop()

def process_and_plot():
    """Busca el archivo descargado, lo limpia y lanza el dashboard"""
    time.sleep(3)  
    csv_files = glob.glob(os.path.join(config.DOWNLOAD_DIR, "*.csv"))
    
    if not csv_files:
        print("[WARNING] No se encontró archivo CSV para procesar.")
        return

    latest_file = max(csv_files, key=os.path.getctime)
    
    #=================================================================================== Renombramiento ordenado 
    nombre_limpio = f"datos_{config.STATION.lower().replace(' ', '_')}_{config.START_DATE.replace('/', '-')}.csv"
    nuevo_path = os.path.join(config.DOWNLOAD_DIR, nombre_limpio)
    
    try:
        if os.path.exists(nuevo_path): os.remove(nuevo_path)
        os.rename(latest_file, nuevo_path)
        latest_file = nuevo_path
    except Exception as e:
        print(f"[WARNING] No se pudo renombrar: {e}")



    #=================================================================================== Pandas
    try:
        df = pd.read_csv(latest_file, sep=";", decimal=",", encoding="latin1", low_memory=False)
        df.columns = [str(c).strip() for c in df.columns]

        col_date = next((c for c in df.columns if "fecha" in c.lower()), None)
        col_precip = next((c for c in df.columns if "precip" in c.lower()), None)
        col_temp = next((c for c in df.columns if "tmed" in c.lower() or "temperatura" in c.lower()), None)

        df[col_date] = pd.to_datetime(df[col_date], format="%d/%m/%Y", errors="coerce")
        df = df.dropna(subset=[col_date]).sort_values(by=col_date)
        df[col_precip] = pd.to_numeric(df[col_precip], errors="coerce").fillna(0)
        df[col_temp] = pd.to_numeric(df[col_temp], errors="coerce")

        show_dashboard(df, col_date, col_precip, col_temp)
    except Exception as e:
        print(f"[ERROR] Error procesando datos: {e}")