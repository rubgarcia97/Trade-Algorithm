import threading

from datetime import datetime
from scripts.gui import GUI
from scripts.strategy import Strategies

stop = None

def cerrar_ventana():
    global stop
    stop = "exit"

    print(f"Repliegue de las tropas a las: {datetime.now()}")
    GUI.root.quit()

def iniciar_estrategia():
    global stop
    stop = None
    print("Estrategia seleccionada:",GUI.choice)
    print(f'El general Trajano ha desplegado sus tropas a las {datetime.now()}\n-----------------------------------')

    threading.Thread(target=getattr(Strategies(),GUI.choice)).start()

def iniciar_test():
    global stop
    stop = None
    print("Funcionalidad por el momento en fase de desarrollo")



GUI().gui(inicio=iniciar_estrategia,detener=cerrar_ventana, test=iniciar_test)