# SIGA INTA Data Automator

Este proyecto es una herramienta de automatización diseñada para la consulta, descarga y análisis de datos agrometeorológicos desde el sistema [SIGA INTA](https://siga.inta.gob.ar/).

> **⚠️ Estado del Proyecto: En Desarrollo**
> Actualmente el proyecto se encuentra en una fase activa de desarrollo. Si bien el flujo principal funciona, algunas características están siendo refinadas para mejorar la estabilidad y la experiencia de usuario.

---

## Descripción

El sistema automatiza la extracción de datos mediante **Selenium**, permitiendo al usuario configurar una estación meteorológica específica y un rango de fechas. Una vez descargados, los archivos CSV son procesados con **Pandas** y visualizados mediante **Matplotlib** para generar un dashboard interactivo que incluye:

*   **Gráfico combinado:** Visualización de Precipitación vs. Temperatura.
*   **Resumen estadístico:** Cálculos de totales acumulados, temperaturas extremas y otros indicadores climáticos.

## Roadmap / Próximos pasos

Estamos trabajando en las siguientes mejoras:

*   [ ] **Gestión de Estaciones:** Implementar un selector con una lista predefinida de estaciones para evitar errores de escritura y facilitar la selección.
*   [ ] **Optimización de Selenium:** Mejorar la gestión de esperas (*waits*) para hacer la descarga más robusta ante posibles lentitudes del servidor.
*   [ ] **Validación de errores:** Ampliar el manejo de excepciones en la interfaz gráfica.

---

## Estructura del Proyecto

*   `config.py`: Configuración global y rutas de directorios.
*   `interfaz.py`: Interfaz gráfica (Tkinter) para la configuración inicial.
*   `auto.py`: Lógica de automatización con Selenium.
*   `procesamiento.py`: Limpieza de datos, cálculos y generación del dashboard.
*   `main.py`: Punto de entrada principal para ejecutar el flujo completo.

---

## Requisitos

*   Python 3.x
*   Navegador Microsoft Edge (con Edge WebDriver instalado).
*   Bibliotecas necesarias:
    ```bash
    pip install pandas matplotlib selenium
    ```
