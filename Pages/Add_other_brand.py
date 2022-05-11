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


def create_database(brand_name, brand_table, dataframe):
    current_dir = os.getcwd()

    database_path = current_dir + "\Data\\" + brand_name
    database_path_file = database_path + "\\" + brand_table + ".db"


    #Creation dir for database
    database_folder = os.mkdir(database_path)

    #Creating the database
    database = sqlite3.connect(database_path_file)

    #Iniciando o cursor
    cursor = database.cursor()

    #Criando a tabela da marca
    cursor.execute("CREATE TABLE '{}' (Brand VARCHAR,  Product_Name VARCHAR,  Product_Description VARCHAR)".format(brand_table))

    sql_script = "INSERT INTO " + brand_table + "(Brand, Product_Name, Product_Description) VALUES (?, ?, ?)"

    #Inserindo os dados
    for index, row in dataframe.iterrows():
        cursor.execute(sql_script,([row['Brand'],row['Product_Name'],row['Description']]))

    database.commit()
    cursor.close()
    database.close()

    #Atualizando o banco de brands com o nome da marca inserida
    database_brands = sqlite3.connect("Data/Brands.db")

    cursor_brands = database_brands.cursor()

    #Inserindo o dado
    cursor_brands.execute("INSERT INTO Brands(Brand) VALUES ('{}')".format(brand_name))

    database_brands.commit()
    cursor_brands.close()
    database_brands.close()

    popup()


def popup():
    #Mensagem de confirmação
    Confirmation_Popup = tk.Tk()
    Confirmation_Popup.title("!!!!!")
    Confirmation_Popup.geometry("100x100")

    #Texto
    Confirmation_Text = tk.Label(Confirmation_Popup, text="Os dados estão salvos")
    Confirmation_Text.pack()

    Confirmation_Button = tk.Button(Confirmation_Popup, text="Ok", command=lambda: destroy(Confirmation_Popup))
    Confirmation_Button.pack()

    Confirmation_Popup.mainloop()

def destroy(root):
    root.destroy()


def add_brands():

    def Upload_n_reading_file_page(brand_name):
        #Procurando o arquivo no computador
        filename = filedialog.askopenfilename()

        #Criando a página de lista para visualização dos itens
        Viz_page = tk.Tk()
        Viz_page.geometry("500x500")
        Viz_page.title("Adicionar nova marca")

        #Trabalhando as variáveis
        brand = str(brand_name)
        brand_file = str(brand_name) + "_products"

        #Lendo o arquivo para DataFrame
        df_raw = pd.read_excel(filename)

        #Criando o frame dos dados
        LabelFrame_dados_db = ttk.LabelFrame(Viz_page, text="Propriedades")
        LabelFrame_dados_db.grid(row=0, column=0, padx=10, pady=10, sticky="N")

        #Colocando o nome do banco que será criada
        Label_db_name = ttk.Label(LabelFrame_dados_db)
        Label_db_name.config(text="O nome do Banco é: " + brand)
        Label_db_name.grid(row=0, column=0, pady=5, padx=5, sticky="N")

        #Colocando o nome da tabela que será criada
        Label_table_name = ttk.Label(LabelFrame_dados_db)
        Label_table_name.config(text="O nome da tabela é: " + brand_file)
        Label_table_name.grid(row=1, column=0, pady=5, padx=5, sticky="N")

        #Criando frame para funções
        LabelFrame_func_db = ttk.LabelFrame(Viz_page, text="Ações")
        LabelFrame_func_db.grid(row=0, column=1, padx=10, pady=10, sticky="N")

        #Botão para subir os dados
        Upload_button = tk.Button(LabelFrame_func_db, text="Subir dados", command=lambda: create_database(brand_name,brand_file,df_raw))
        Upload_button.grid(row=0, column=0, padx=5, pady=5,sticky="N")

        #Botão para cancelar a operação
        Back_button = tk.Button(LabelFrame_func_db, text="Cancelar", command=lambda: destroy(Viz_page))
        Back_button.grid(row=0, column=1, padx=5, pady=5, sticky="N")

        #Criando Label para a lista
        #Criando frame para funções
        LabelFrame_list = ttk.LabelFrame(Viz_page, text="Dados")
        LabelFrame_list.grid(row=1, column=0, padx=10, pady=10, sticky="W")

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
