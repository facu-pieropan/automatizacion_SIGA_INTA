# La lógica de Selenium (Importante)

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import config

def init_driver():
    """Inicializa el WebDriver de Edge con las preferencias de descarga configuradas en interfaz"""
    prefs = {
        "download.default_directory": config.DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_settings.popups": 0,
        "profile.default_content_setting_values.automatic_downloads": 1,
    }

    options = webdriver.EdgeOptions()
    options.add_experimental_option("prefs", prefs)
    
    if config.HEADLESS_MODE:
        options.add_argument("--headless")

    return webdriver.Edge(options=options)


def wait_for_download(timeout=config.DOWNLOAD_TIMEOUT):
    """Monitorea el directorio de descargas hasta detectar un archivo CSV completo"""
    for _ in range(timeout):
        if os.path.exists(config.DOWNLOAD_DIR):
            files = os.listdir(config.DOWNLOAD_DIR)
            if any(f.endswith(".csv") and not f.endswith(".crdownload") for f in files):
                return True
        time.sleep(1)
    return False


def ejecutar_descarga():
    """Controla todo el flujo de navegación con Selenium para extraer los datos de SIGA INTA"""
    driver = init_driver()
    wait = WebDriverWait(driver, 25)

    try:
        print(f"[INFO] Accediendo a SIGA INTA para la estación: {config.STATION}")
        driver.get("https://siga.inta.gob.ar/")
        driver.maximize_window()

        data_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'DATOS') or contains(@href, 'data')]")))
        data_tab.click()

        print("[INFO] Buscando la estación objetivo...")
        station_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Nombre de estación')]")))
        station_input.click()
        station_input.clear()
        station_input.send_keys(config.STATION)
        time.sleep(1.5)
        station_input.send_keys(Keys.ENTER)

        print("[INFO] Configurando filtros de fechas...")
        period_radio = wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@type='radio'])[2]")))
        driver.execute_script("arguments[0].click();", period_radio)

        date_inputs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[contains(@placeholder, 'Ej. 01/01/2017') or contains(@placeholder, 'Fecha')]")))
        
        date_inputs[0].click()
        date_inputs[0].clear()
        date_inputs[0].send_keys(config.START_DATE)

        date_inputs[1].click()
        date_inputs[1].clear()
        date_inputs[1].send_keys(config.END_DATE)

        print("[INFO] Ejecutando consulta tabular...")
        query_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-info') and contains(text(), 'Consultar')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", query_btn)
        time.sleep(0.8)
        driver.execute_script("arguments[0].click();", query_btn)

        print("[INFO] Esperando a que se rendericen los registros...")
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'registros')]")))
        time.sleep(5)

        print("[INFO] Iniciando la exportación del CSV mediante AngularJS...")
        csv_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='exportDatosDiarios(false)']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", csv_btn)
        time.sleep(1)
        driver.execute_script("angular.element(arguments[0]).scope().exportDatosDiarios(false);", csv_btn)

        print("[INFO] Verificando la descarga del archivo...")
        if wait_for_download():
            print("\n[SUCCESS] Archivo CSV descargado con éxito.")
            return True
        else:
            print("\n[WARNING] Tiempo de espera agotado para la descarga.")
            return False

    except Exception as exc:
        print(f"\n[ERROR] El proceso de automatización falló: {exc}")
        return False

    finally:
        time.sleep(2)
        print("[INFO] Cerrando sesión del navegador.")
        driver.quit()