#Importando bibliotecas
import os
import time
import tkinter as tk
from tkinter import ttk

import sqlite3 as sql

import tkinter
import winsound
from PIL import ImageTk, Image


def Get_Brands(root,Frame):

    def getting_brands():
        # Pegando caminho do database
        current_dir = os.getcwd()

        Database_path = current_dir + "\Data\Brands.db"

        # Criando a conexão com o banco de dados
        Database = sql.connect(Database_path)

        # Criando cursor
        c = Database.cursor()

        # Executando script para pegar os dados
        c.execute("SELECT Brand FROM Brands")
        result = c.fetchall()
        c.close()
        result = [x[0] for x in result]

        return result

    #Pegando as marcas
    Marcas = list(getting_brands())
    Value_inside = tkinter.StringVar(root)
    Value_inside.set(Marcas[0])

    return ttk.OptionMenu(Frame, Value_inside, *Marcas)