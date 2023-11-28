from scripts.gui import GUI

stop = None

def cerrar_ventana():
    global stop
    stop = "exit"

    print(f"Repliegue de las tropas")
    GUI.root.quit()

def iniciar_estrategia():
    global stop
    stop = None
    print(f"El general Trajano ha desplegado sus legiones")

def iniciar_test():
    global stop
    stop = None
    print("Iniciamos Test...")



GUI().gui(inicio=iniciar_estrategia,detener=cerrar_ventana, test=iniciar_test)