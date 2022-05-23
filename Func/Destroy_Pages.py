#Importando bibliotecas
import os
from tkinter import ttk

import sqlite3 as sql

import tkinter


#Criando a função para deletar múltiplas janelas
def destroy_multiple_pages(page1=None, page2=None):

    #Criando uma lista das páginas
    List_pages = [page1, page2]

    for page in List_pages:
        page.destroy()