#IMPORTANDO BIBLIOTECAS
import requests
import json
import pandas as pd
import sqlite3
import time
from tqdm import tqdm
import datetime
import os

#GUARDANDO LISTAS
Urls_Magalu = []
Sellers_Magalu = []
Country_Magalu = []
Price_Magalu = []
SKU_Magalu = []
Title_Magalu = []
Installment_Magalu_quantidade = []
Installment_Magalu_valor_parcela = []
Installment_Magalu_valor_total = []

#Headers da Magazine
headers_magalu = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.59"}

#Função para criar os links de busca
def getting_n_creating_magazine_urls(brand):
    # Pegando caminho do database
    current_dir = os.getcwd()

    Database_path = current_dir + "\Data\\" + brand + "\\" + brand + ".db"

    table = brand + "_products"

    #Criando a Query
    query = "SELECT * FROM " + table

    print(Database_path)

    #Entrando dentro do databse
    connection = sqlite3.connect(Database_path)

    #Criando o dataset em brando
    df = pd.read_sql_query(query, connection)

    #Passando todo o Dataframe para LowerCase
    df = df.apply(lambda x: x.astype(str).str.lower())

    #Arrumando espaços vazios
    # Arrumano os espaços vazios
    df['Product_Name'] = df['Product_Name'].str.replace(" ", "%2B")
    df['Product_Name'] = df['Product_Name'].str.replace("-", "%2B")

    # Criando uma nova coluna no database com a formatação certa
    df['Urls'] = df['Brand'] + "+" + df['Product_Name']

    # Criando a nova coluna que são as urls de pesquisa
    df['Urls_search'] = "https://www.magazineluiza.com.br/_next/data/SJCtTE8TVyZNMypTAB7uE/busca/" + \
    df['Brand'][0] + "%2B" + df['Product_Name'] + ".json?slug=busca&slug=" + \
    df['Brand'][0] + "%2B" + df['Product_Name']

    return df

def creating_dataframe(urls, sellers, price, installment, parcel, installment_total, sku, title, brand):
    Dataframe = pd.DataFrame()

    Hoje = pd.to_datetime('today', errors='ignore').date()

    Dataframe['Urls_2'] = urls

    Dataframe['DATE'] = Hoje

    Dataframe['URL'] = "https://www.magazineluiza.com.br/" + Dataframe['Urls_2']
    Dataframe['MARKETPLACE'] = 'MAGAZINE LUIZA'
    Dataframe['SELLER'] = sellers

    Dataframe['PRICE'] = price
    Dataframe['PRICE'] = Dataframe['PRICE'].astype('float')


    Dataframe['INSTALLMENT'] = installment

    Dataframe['PARCEL'] = parcel


    Dataframe['INSTALLMENT_PAYMENT'] = installment_total
    #Dataframe['INSTALLMENT_PAYMENT'] = Dataframe['INSTALLMENT_PAYMENT'].astype('float')

    Dataframe['ID'] = sku
    Dataframe['PRODUCT'] = title

    if brand == "GoPro":
        Dataframe = Dataframe[Dataframe['PRICE'] > 1000]
    elif brand == 'Motorola':
        Dataframe = Dataframe[Dataframe['PRICE'] > 100]
    elif brand == 'Wacom':
        Dataframe = Dataframe[Dataframe['PRICE'] > 100]

    #Colocando na ordem correta
    Dataframe = Dataframe[['DATE', 'URL', 'MARKETPLACE', 'SELLER', 'PRICE', 'PARCEL', 'INSTALLMENT', 'INSTALLMENT_PAYMENT', 'ID', 'PRODUCT']]

    Dataframe['INSTALLMENT'] = Dataframe['INSTALLMENT'].astype('float')
    Dataframe['PARCEL'] = Dataframe['PARCEL'].astype('int')
    Dataframe['INSTALLMENT_PAYMENT'] = Dataframe['INSTALLMENT_PAYMENT'].astype('float')

    return Dataframe

def get_attributes(url):
    time.sleep(20)

    response = requests.get(url, headers=headers_magalu)
    text_json = response.json()

    # URL
    id_url = 0
    for i in text_json['pageProps']['data']['search']['products']:
        try:
            Urls_Magalu.append(text_json['pageProps']['data']['search']['products'][id_url]['url'])
        except:
            Urls_Magalu.append("ERRO")

        id_url = id_url + 1

    # ID
    id_number = 0
    for i in text_json['pageProps']['data']['search']['products']:
        try:
            SKU_Magalu.append(text_json['pageProps']['data']['search']['products'][id_number]['variationId'])
        except:
            SKU_Magalu.append("ERRO")

        id_number = id_number + 1

    # SELLER
    id_seller = 0
    for i in text_json['pageProps']['data']['search']['products']:
        try:
            Sellers_Magalu.append(
                text_json['pageProps']['data']['search']['products'][id_seller]['seller']['description'])
        except:
            Sellers_Magalu.append("ERRO")

        id_seller = id_seller + 1

    # COUNTRY
    id_country = 0
    for i in text_json['pageProps']['data']['search']['products']:
        try:
            Country_Magalu.append(
                text_json['pageProps']['data']['search']['products'][id_country]['seller']['details']['address'][
                    'country'])
        except:
            Country_Magalu.append("ERRO")

        id_country = id_country + 1

    # PREÇO
    id_price = 0
    for i in text_json['pageProps']['data']['search']['products']:
        try:
            Price_Magalu.append(text_json['pageProps']['data']['search']['products'][id_price]['price']['bestPrice'])
        except:
            Price_Magalu.append("ERRO")

        id_price = id_price + 1

    # TITULO
    id_title = 0
    for i in text_json['pageProps']['data']['search']['products']:
        try:
            Title_Magalu.append(text_json['pageProps']['data']['search']['products'][id_title]['title'])
        except:
            Title_Magalu.append("ERRO")

        id_title = id_title + 1

    # INSTALLMENT QUANTIDADE
    id_installment_quantidade = 0
    for i in text_json['pageProps']['data']['search']['products']:
        try:
            Installment_Magalu_quantidade.append(
                text_json['pageProps']['data']['search']['products'][id_installment_quantidade]['installment'][
                    'quantity'])
        except:
            Installment_Magalu_quantidade.append("ERRO")

        id_installment_quantidade = id_installment_quantidade + 1

    # INSTALLMENT VALOR POR PARCELA
    id_installment_valor_parcela = 0
    for i in text_json['pageProps']['data']['search']['products']:
        try:
            Installment_Magalu_valor_parcela.append(
                text_json['pageProps']['data']['search']['products'][id_installment_valor_parcela]['installment'][
                    'amount'])
        except:
            Installment_Magalu_valor_parcela.append("ERRO")

        id_installment_valor_parcela = id_installment_valor_parcela + 1

    # INSTALLMENT VALOR TOTAL
    id_installment_valor_total = 0
    for i in text_json['pageProps']['data']['search']['products']:
        try:
            Installment_Magalu_valor_total.append(
                text_json['pageProps']['data']['search']['products'][id_installment_valor_total]['installment'][
                    'totalAmount'])
        except:
            Installment_Magalu_valor_total.append("ERRO")

        id_installment_valor_total = id_installment_valor_total + 1

def magalu_final(brand):
    df = getting_n_creating_magazine_urls(brand)

    for url in tqdm(df['Urls_search']):
        get_attributes(url)

    dataset_magalu = creating_dataframe(Urls_Magalu, Sellers_Magalu, Price_Magalu, Installment_Magalu_valor_parcela, Installment_Magalu_quantidade, Installment_Magalu_valor_total, SKU_Magalu, Title_Magalu, brand)

    current_dir = os.getcwd()

    path_download = current_dir + '\Data\\' + brand + "\Files\\" + 'Magazine_' + brand + ".xlsx"

    dataset_magalu.to_excel(path_download, index=False)

