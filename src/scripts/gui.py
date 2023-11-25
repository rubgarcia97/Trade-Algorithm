from tkinter import *

import customtkinter
import yaml


class GUI:

    root = customtkinter.CTk()
    
    with open("./config/strategies.yaml","r") as file:
        estrategias_data = yaml.safe_load(file)

    strategies = [estrategia["nombre"] for estrategia in estrategias_data["estrategias"]]
    

    def __init__(self):
        pass


    def gui(self,inicio,detener):

        """
        Funcion que instancia una ventana emergente con dos comandos basicos:

        :param inicio: Define la funcion que se ejecutara al dar el boton de inicio en la interfaz de usuario
        :param detener: Define la funcion que se ejecutara al dar el boton de Detener en la interfaz de usuario
        """

        self.root.geometry("375x568")
        self.root.title("Trajano")

        def combobox_callback(choice):
            print("combobox dropdown clicked:",choice)

        combobox = customtkinter.CTkComboBox(self.root,width=200,values=self.strategies, command=combobox_callback)
        combobox.place(relx=0.1,rely=0.05)

        boton_iniciar = customtkinter.CTkButton(height=20,width=70,master=self.root,text="Iniciar",command=inicio)
        boton_iniciar.place(relx=0.68, rely=0.6, anchor = CENTER)

        boton_detener = customtkinter.CTkButton(height=20,width=70,master=self.root,text="Detener",command=detener)
        boton_detener.place(relx=0.88, rely=0.6, anchor = CENTER)

        self.root.mainloop()