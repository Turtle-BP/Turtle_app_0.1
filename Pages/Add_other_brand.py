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

    def Upload_n_reading_file_page(brand_name):
        #Procurando o arquivo no computador
        filename = filedialog.askopenfilename()

        #Criando a página de lista para visualização dos itens
        Viz_page = tk.Tk()
        Viz_page.geometry("500x500")

        #Lendo o arquivo para DataFrame
        df_raw = pd.read_excel(filename)

        #Criando o frame dos dados
        LabelFrame_dados_db = ttk.LabelFrame(Viz_page, text="Propriedades")
        LabelFrame_dados_db.grid(row=0, column=0, padx=10, pady=10, sticky="NW")

        #Colocando o nome do banco que será criada
        Label_db_name = ttk.Label(LabelFrame_dados_db)
        Label_db_name.config(text="O nome do Banco é: " + str(brand_name))
        Label_db_name.grid(row=0, column=0, pady=5, padx=5, sticky="NW")

        #Colocando o nome da tabela que será criada
        Label_table_name = ttk.Label(LabelFrame_dados_db)
        Label_table_name.config(text="O nome da tabela é: " + str(brand_name) + "_products")
        Label_table_name.grid(row=1, column=0, pady=5, padx=5, sticky="NW")

        #Criando frame para funções
        LabelFrame_func_db = ttk.LabelFrame(Viz_page, text="Ações")
        LabelFrame_func_db.grid(row=1, column=0, padx=5, pady=5, sticky="N")

        #Botão para subir os dados
        Upload_button = tk.Button(LabelFrame_func_db, text="Subir dados")
        Upload_button.grid(row=0, column=0, padx=3, pady=10,sticky="N")

        #Botão para cancelar a operação
        Back_button = tk.Button(LabelFrame_func_db, text="Cancelar")
        Back_button.grid(row=0, column=1, padx=3, pady=10, sticky="N")

        #Criando Label para a lista
        #Criando frame para funções
        LabelFrame_list = ttk.LabelFrame(Viz_page, text="Dados")
        LabelFrame_list.grid(row=0, column=1, padx=10, pady=10, sticky="N")

        # Criando a lista para mostrar esses valores
        List_of_itens = tk.Listbox(LabelFrame_list)
        List_of_itens.grid(row=0, column=0,padx=3, pady=10, sticky="N")

        #Fazendo o loop para mostar os itens
        x = 1
        for data in df_raw['Product_Name']:
            List_of_itens.insert(x, data)
            x = x + 1






        Viz_page.mainloop()




    #Criando a página
    new_page = tk.Tk()
    new_page.title("Adicionar marca")
    new_page.geometry("300x70")

    #Criando o campo do nome da marca
    New_Brand_Name = ttk.Label(new_page, text="Coloque o nome da marca:")
    New_Brand_Name.grid(row=1, column=1, pady=10, padx=10, sticky="W")

    #Criando o espaço para colocar o nome da marca
    Entry_New_Brand = ttk.Entry(new_page)
    Entry_New_Brand.grid(row=1, column=2)

    Search_file = ttk.Button(new_page, text="Pesquisar arquivo", command=lambda: Upload_n_reading_file_page(Entry_New_Brand.get()))
    Search_file.grid(row=3, column=2, sticky="W")



    new_page.mainloop()
