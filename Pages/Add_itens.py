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

def getting_itens(brand, root):
    current_dir = os.getcwd()
    database = current_dir + "\Data\\" + str(brand) + "\\" +str(brand) + "_products.db"
    database_table = str(brand) + "_products"

    database_conec = sqlite3.connect(database)
    cursor = database_conec.cursor()
    sql_script = "SELECT Product_Name FROM " + database_table

    cursor.execute(sql_script)
    result = cursor.fetchall()
    cursor.close()

    result = [x[0] for x in result]


    x = 1
    for product in result:
        List_of_itens.insert(x, product)
        x = x + 1

def destroy(root):
    root.destroy()

def add_itens():
    global List_of_itens

    #Criando a página
    new_root = tk.Tk()
    new_root.geometry("300x300")
    new_root.title("Adidionar Itens")

    #Texto
    Text_Brand = ttk.Label(new_root, text="Escolha a Marca:")
    Text_Brand.grid(row=1, column=1, padx=3, pady=3,sticky="NW")

    #Função para pegar brands
    Marcas = list(getting_brands())
    Value_inside = tkinter.StringVar(new_root)
    Value_inside.set(Marcas[0])

    #Criando lista de marcas
    Choice_Brand = ttk.OptionMenu(new_root, Value_inside, *Marcas)
    Choice_Brand.grid(row=1, column=2, padx=3, pady=3, sticky="NW")

    #Botão para visualizar já os produtos inside
    Inside_itens_button = ttk.Button(new_root, text="Veja os itens", command=lambda: getting_itens(Value_inside.get(),new_root))
    Inside_itens_button.grid(row=2, column=2, sticky="NW")

    FrameList = ttk.LabelFrame(new_root, text="Produtos")
    FrameList.grid(row=3, column=1, padx=10, pady=10, sticky="W")

    List_of_itens = tk.Listbox(FrameList)
    List_of_itens.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    FuncLabel = ttk.LabelFrame(new_root, text="Funções")
    FuncLabel.grid(row=3, column=2, pady=10, padx=10, sticky="N")

    Upload_itens = ttk.Button(FuncLabel, text="Subir itens")
    Upload_itens.grid(row=0, column=0, padx=10, pady=10, sticky="NW")

    delete_itens = ttk.Button(FuncLabel, text="Deletar produto")
    delete_itens.grid(row=1, column=0, padx=10, pady=10, sticky="NW")

    Cancel_itens = ttk.Button(FuncLabel, text="Cancelar", command=lambda: destroy(new_root))
    Cancel_itens.grid(row=2, column=0, padx=10, pady=10, sticky="NW")

    new_root.mainloop()