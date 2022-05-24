#Importando bibliotecas
import os
from tkinter import ttk

import sqlite3 as sql

import tkinter


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
