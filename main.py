# Esto debes ejecutar :)

import interfaz
import auto
import procesamiento

def main():
    interfaz.solicitar_parametros()

    if auto.ejecutar_descarga():
        procesamiento.process_and_plot()

if __name__ == "__main__":
    main()