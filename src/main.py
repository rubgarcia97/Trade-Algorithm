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



GUI().gui(inicio=iniciar_estrategia,detener=cerrar_ventana)