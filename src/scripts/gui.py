from tkinter import *

import customtkinter


class GUI:

    root = customtkinter.CTk()

    def __init__(self):
        pass


    def gui(self,inicio,detener):

        """
        Funcion que instancia una ventana emergente con dos comandos basicos:

        :param inicio: Define la funcion que se ejecutara al dar el boton de inicio en la interfaz de usuario
        :param detener: Define la funcion que se ejecutara al dar el boton de Detener en la interfaz de usuario
        """

        self.root.geometry("300x100")
        self.root.title("Trajano")

        boton_iniciar = customtkinter.CTkButton(master=self.root,text="Iniciar",command=inicio)
        boton_iniciar.place(relx=0.25, rely=0.5, anchor = CENTER)

        boton_detener = customtkinter.CTkButton(master=self.root,text="Detener",command=detener)
        boton_detener.place(relx=0.75, rely=0.5, anchor = CENTER)

        self.root.mainloop()