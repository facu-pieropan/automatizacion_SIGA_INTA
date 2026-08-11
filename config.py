# Aca configuramos variables globales y ruta

import os

STATION = "Sombrerito"
START_DATE = "01/01/2025"
END_DATE = "31/12/2025"
DOWNLOAD_TIMEOUT = 20
HEADLESS_MODE = False

DOWNLOAD_DIR = os.path.abspath("data")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)