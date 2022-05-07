#Importando as bibliotecas padrão
import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sqlite3
import tkinter
from tkinter.constants import W
from typing import Text
import pandas as pd






def add_brands():

    def uploadfile():
        filename = filedialog.askopenfilename()
        print(filename)


    #Criando a página
    new_page = tk.Tk()
    new_page.title("Adicionar marca")
    new_page.geometry("300x300")

    #Criando o campo do nome da marca
    New_Brand_Name = ttk.Label(new_page, text="Coloque o nome da marca:")
    New_Brand_Name.grid(row=1, column=1, pady=10, padx=10, sticky="W")

    #Criando o espaço para colocar o nome da marca
    Entry_New_Brand = ttk.Entry(new_page)
    Entry_New_Brand.grid(row=1, column=2)

    #Colocando o texto para os itens
    Lists_entrys = ttk.Label(new_page, text="Coloque o nome dos itens")
    Lists_entrys.grid(row=3, column=1, pady=10, padx=10, sticky="W")

    Product_1 = ttk.Entry(new_page)
    Product_1.grid(row=4, column=1)

    Product_2 = ttk.Entry(new_page)
    Product_2.grid(row=5, column=1)

    Product_3 = ttk.Entry(new_page)
    Product_3.grid(row=6, column=1)

    Product_4 = ttk.Entry(new_page)
    Product_4.grid(row=7, column=1)

    Product_5 = ttk.Entry(new_page)
    Product_5.grid(row=8, column=1)

    bota_teste = ttk.Button(new_page, text="Teste", command=uploadfile)
    bota_teste.grid(row=10, column=1)

    new_page.mainloop()
