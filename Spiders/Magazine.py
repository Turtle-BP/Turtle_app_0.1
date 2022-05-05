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

#Função para criar os links de busca
def getting_n_creating_magazine_urls(brand):
    # Pegando caminho do database
    current_dir = os.getcwd()

    Database_path = current_dir + "\Data\\" + brand + "\\" + brand + "_products.db"

    table = brand + "_products"

    #Criando a Query
    query = "SELECT * FROM " + table

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
    df['Urls_search'] = "https://www.magazineluiza.com.br/_next/data/LRgWvdBfwbrMLsKPe8bQb/busca/" + \
    df['Brand'][0] + "%2B" + df['Product_Name'] + ".json?slug=busca&slug=" + \
    df['Brand'][0] + "%2B" + df['Product_Name']

    return df

def creating_dataframe(urls, sellers, price, sku, title, quantidade, parcela, total):
    Dataframe = pd.DataFrame()

    date = datetime.datetime.now().date()
    today = pd.to_datetime(date)

    Dataframe['Data'] = today
    Dataframe['Data'] = today
    Dataframe['Urls_2'] = urls
    Dataframe['Urls'] = "https://www.magazineluiza.com.br/" + Dataframe['Urls_2']
    Dataframe['Loja'] = 'MAGAZINE LUIZA'
    Dataframe['Sellers'] = sellers
    Dataframe['Price'] = price
    Dataframe['Parcela'] = quantidade
    Dataframe['Installment'] = parcela
    Dataframe['Installment-valor'] = total
    Dataframe['SKU'] = sku
    Dataframe['Title'] = title

    Dataframe = Dataframe[Dataframe['Title'].str.contains("Wacom")]

    Dataframe.drop(['Urls_2'], axis=1, inplace=True)

    Dataframe = Dataframe[~Dataframe['Urls'].str.contains("capa")]
    Dataframe = Dataframe[~Dataframe['Urls'].str.contains("pelicula")]
    Dataframe = Dataframe[~Dataframe['Urls'].str.contains("Pulseira")]
    Dataframe = Dataframe[~Dataframe['Urls'].str.contains("Case")]
    Dataframe = Dataframe[~Dataframe['Urls'].str.contains("Usb")]

    return Dataframe

def get_attributes(url):
    time.sleep(20)

    response = requests.get(url)
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
            Price_Magalu.append(text_json['pageProps']['data']['search']['products'][id_price]['price']['price'])
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

    dataset_magalu = creating_dataframe(Urls_Magalu,Sellers_Magalu,Price_Magalu,SKU_Magalu,Title_Magalu,Installment_Magalu_quantidade,Installment_Magalu_valor_parcela,Installment_Magalu_valor_total)

    dataset_magalu.to_excel(r"C:\Users\pedro\Documents\Turte Brand Protection\Turtle_Thinker_Alpha_0.1\Magazine.xlsx", index=False)

