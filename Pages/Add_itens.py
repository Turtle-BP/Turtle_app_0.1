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

#Pegando marcas
def getting_brands():
    #Pegando caminho do database
    current_dir = os.getcwd()

    Database_path = current_dir + "\Data\Brands.db"

    #Criando a conexão com o banco de dados
    Database = sqlite3.connect(Database_path)

    #Criando cursor
    c = Database.cursor()

    #Executando script para pegar os dados
    c.execute("SELECT Brand FROM Brands")
    result = c.fetchall()
    c.close()

    result = [x[0] for x in result]

    return result


def add_itens():

    #Criando a página
    new_root = tk.Tk()
    new_root.geometry("300x300")

    #Texto
    Text_Brand = ttk.Label(new_root, text="Escolha a Marca:")
    Text_Brand.grid(row=1, column=1, padx=3, pady=3,sticky="W")

    #Função para pegar brands
    Marcas = list(getting_brands())
    Value_inside = tkinter.StringVar(new_root)
    Value_inside.set(Marcas[0])

    #Criando lista de marcas
    Choice_Brand = ttk.OptionMenu(new_root, Value_inside, *Marcas)
    Choice_Brand.grid(row=1, column=2, padx=3, pady=3, sticky="W")

    #Botão para visualizar já os produtos inside
    Inside_itens_button = ttk.Button(new_root, text="Veja os itens")
    Inside_itens_button.grid(row=2, column=2)

    new_root.mainloop()