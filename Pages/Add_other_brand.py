#Importando as bibliotecas padrão
import os
import time
import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter
from tkinter.constants import W
from typing import Text
import pandas as pd







def add_brands():
    #Criando a página
    new_page = tk.Tk()
    new_page.title("Adicionar marca")
    new_page.geometry("300x300")

    #Criando o campo do nome da marca
    New_Brand_Name = ttk.Label(new_page, text="Coloque o nome da marca:")
    New_Brand_Name.grid(row=1, column=1, pady=10, padx=10, sticky="W")

    #Criando o espaço para colocar o nome da marca
    Entry_New_Brand = ttk.Entry(new_page)
    Entry_New_Brand.grid(row=2, column=1)

    new_page.mainloop()
