#Importando as bibliotecas padrão 
import os
import tkinter as tk
from tkinter import *
import sqlite3
import tkinter
from tkinter.constants import W
from typing import Text
import pandas as pd

#Função para deletar os warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#Importando função de outras páginas 
from Pages.Spiders_Search import Spiders_Search_page
from Pages.Upload_Data import Upload_Data

#Criando a página principal
root = tk.Tk()
root.geometry("350x100")
root.title("Turtle Brand Protection")




#Criando os botões para abrir outras páginas do aplicativo 

#Adicionar Marca nova 
botao_New_Brands = tk.Button(root, text='Adicionar marca')
botao_New_Brands.grid(row=1, column=1, padx=10, pady=10, sticky="W")

#Adicionar Itens novos a Marcas antigas
botao_New_Itens = tk.Button(root, text='Adicionar Itens')
botao_New_Itens.grid(row=1, column=2, padx=10, pady=10, sticky="W")

#Subir dados para o database
botao_Add_Data = tk.Button(root, text='Subir dados', command=Upload_Data)
botao_Add_Data.grid(row=1, column=3, padx=10, pady=10, sticky="W")

#Pegar o estoque / Verificação
botao_Estoque = tk.Button(root, text='Estoque')
botao_Estoque.grid(row=3, column=2, padx=10, pady=10, sticky="W")

#Spiders para busca de itens da marca
botao_Spiders = tk.Button(root, text='Spiders', command=Spiders_Search_page)
botao_Spiders.grid(row=3, column=3, padx=10, pady=10, sticky="W")

#Envio de E-mail para Motorola
botao_email = tk.Button(root, text='E-mail')
botao_email.grid(row=3, column=1, padx=10, pady=10, sticky="W")




root.mainloop()