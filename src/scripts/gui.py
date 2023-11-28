from tkinter import *

import customtkinter
import tkinter as tk
import yaml
import os
import sys

class ConsoleRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # Auto-scroll to the bottom


class GUI:

    root = customtkinter.CTk()
    
    with open("./config/strategies.yaml","r") as file:
        estrategias_data = yaml.safe_load(file)

    strategies = [estrategia["nombre"] for estrategia in estrategias_data["estrategias"]]
    

    def __init__(self):
        pass


    def gui(self,inicio,detener,test):

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


        frame = customtkinter.CTkFrame(master=self.root)
        frame.pack(side="bottom",fill=BOTH,expand=False)

        console_text = customtkinter.CTkTextbox(frame, wrap=tk.WORD, width=500, height=180)
        console_text.pack(anchor="center", pady=10, padx=10) #Anchor the console box to the middle of the screen and add some padding
        console_text.configure(scrollbar_button_color="", scrollbar_button_hover_color="") #Make scroll-bar invisible
        font_spec = ("Cascadia Code", 12)  # Font family and size


        boton_test = customtkinter.CTkButton(height=20,width=70,master=self.root,text="Test",command=test)
        boton_test.place(relx=0.1, rely=0.6, anchor = CENTER)

        boton_iniciar = customtkinter.CTkButton(height=20,width=70,master=self.root,text="Iniciar",command=inicio)
        boton_iniciar.place(relx=0.68, rely=0.6, anchor = CENTER)

        boton_detener = customtkinter.CTkButton(height=20,width=70,master=self.root,text="Detener",command=detener)
        boton_detener.place(relx=0.88, rely=0.6, anchor = CENTER)


        sys.stdout = ConsoleRedirector(console_text)
        sys.stderr = ConsoleRedirector(console_text)

        self.root.mainloop()