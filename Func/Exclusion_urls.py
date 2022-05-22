#Importando as bibliotecas
import pandas as pd
import sqlite3 as sq
import os


def Clean_Urls(brand, lista):

    #Pegando o diretório inicial
    current_dir = os.getcwd()

    #Criando o path para o banco
    Database_path = current_dir + "\Data\\" + brand + "\\" + brand + ".db"

    #Criando o nome da table
    Table_name = brand + '_exclusao'

    #Criando a Query para pegar a tabela dentro do banco de dados
    Query = "SELECT * FROM " + Table_name

    #Criando a conexão
    Connection = sq.Connection(Database_path)

    #Criando o dataset com a tabela dentro do banco de dados
    Df_exclusao = pd.read_sql_query(Query, Connection)

    #Criando o DataFrame com os links sujos
    Clean_urls = pd.DataFrame()
    Clean_urls['Urls_sujo'] = lista


