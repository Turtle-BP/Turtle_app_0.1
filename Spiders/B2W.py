#IMPORTANDO BIBLIOTECAS
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import sqlite3
import time
from tqdm import tqdm
import os
import random

#Configurando Header
User_agents_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.60',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36']

#GUARDANDO LISTAS
Links_Americanas = []
Urls_Americanas = []
Sellers_Americanas = []
Country_Americanas = []
Price_Americanas = []
SKU_Americanas = []
Title_Americanas = []
Installment_Americanas_quantidade = []
Installment_Americanas_valor_parcela = []
Installment_Americanas_valor_total = []
More_offers_americanas = []


def Random_User_Agents():
    Choice_User_Agent = random.choice(User_agents_list)

    #Configurando Header
    headers = {'authority':'www.americanas.com.br','scheme':'https','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'accept-encoding':'gzip, deflate, br','referer':'https://www.americanas.com.br/', 'user-agent':Choice_User_Agent}


    return headers



def getting_n_creating_americanas_urls(brand):
    # Pegando caminho do database
    current_dir = os.getcwd()

    Database_path = current_dir + "\Data\\" + brand + "\\" + brand + ".db"

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
    df['Product_Name'] = df['Product_Name'].str.replace(" ", "-")

    # Criando uma nova coluna no database com a formatação certa
    df['Urls'] = df['Brand'] + "-" + df['Product_Name']

    # Criando a nova coluna que são as urls de pesquisa
    df['Urls_search'] = "https://www.americanas.com.br/busca/" + df['Urls']

    return df


def search_links(url):
    global Links_Americanas

    time.sleep(10)

    Headers_Choice = Random_User_Agents()

    response = requests.get(url, headers=Headers_Choice)

    if response.status_code != 200:
        Headers_Choice = Random_User_Agents()
        response = requests.get(url, headers=Headers_Choice)

    else:
        pass

    html = response.text

    bs = BeautifulSoup(html, 'html.parser')

    for link in bs.find_all("a", href=True):
        Links_Americanas.append("https://www.americanas.com.br" + link['href'])

    Links_Americanas = [s for s in Links_Americanas if 'produto' in s]


def get_atributes(url):
    time.sleep(30)

    Headers_Choice = Random_User_Agents()

    response = requests.get(url, headers=Headers_Choice)

    if response.status_code != 200:

        Headers_Choice = Random_User_Agents()
        response = requests.get(url, headers=Headers_Choice)

    else:
        pass

    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    #Title
    try:
        Title_Americanas.append(soup.find(class_='product-title__Title-sc-1hlrxcw-0 jyetLr').text)
    except:
        Title_Americanas.append("Erro")

    #Preço
    try:
        Price_Americanas.append(soup.find(class_='styles__PriceText-sc-x06r9i-0 dUTOlD priceSales').text)
    except:
        Price_Americanas.append('Erro')

    #Installment
    try:
        Installment_Americanas_valor_parcela.append(soup.find(class_='payment-installment-text__Text-sc-12txe9z-0 bfFyfi').text)
    except:
        Installment_Americanas_valor_parcela.append("Erro")

    #Seller
    try:
        Sellers_Americanas.append(soup.find(class_='offers-box__Wrapper-sc-189v1x3-0 kegaFO').text)
    except:
        Sellers_Americanas.append("Erro")


    #More offers
    try:
        More_offers_americanas.append(soup.find(class_='more-offers__Touchable-sc-15yqej3-2 hYfNEd').text)
    except:
        More_offers_americanas.append("Erro")


def create_dataframe(url, sellers, price, installment, title):
        df_raw = pd.DataFrame()

        Hoje = pd.to_datetime('today', errors='ignore').date()

        df_raw['URL'] = url

        df_raw['DATE'] = Hoje

        df_raw['MARKETPLACE'] = 'Americanas'

        df_raw['SELLER'] = sellers
        df_raw['SELLER'] = df_raw['SELLER'].str.replace("Este produto é vendido por", "")
        df_raw['SELLER'] = df_raw['SELLER'].str.partition(" e")[0]

        df_raw['PRICE'] = price
        df_raw['PRICE'] = df_raw['PRICE'].str.replace("R$ ", "", regex=False)
        df_raw['PRICE'] = df_raw['PRICE'].str.replace(".", "")
        df_raw['PRICE'] = df_raw['PRICE'].str.replace(",", ".")

        df_raw['Installment_full'] = installment
        df_raw['PARCEL'] = df_raw['Installment_full'].str.partition('x')[0].str.partition("até ")[2]

        df_raw['INSTALLMENT'] = df_raw['Installment_full'].str.partition("x")[2].str.partition("R$ ")[2]
        df_raw['INSTALLMENT'] = df_raw['INSTALLMENT'].str.replace(",", ".")

        df_raw['PRODUCT'] = title

        df_raw['MORE'] = More_offers_americanas

        df_raw['ID'] = df_raw['URL'].str.partition("produto/")[2].str.partition('?')[0]

        df_raw = df_raw[['DATE', 'URL', 'MARKETPLACE', 'SELLER', 'PRICE', 'PARCEL', 'INSTALLMENT', 'ID', 'PRODUCT', 'MORE']]

        return df_raw

#Função final
def americanas_final(path, brand):
    df = getting_n_creating_americanas_urls(brand)

    for url in tqdm(df['Urls_search']):
        search_links(url)

    for url in tqdm(Links_Americanas):
        get_atributes(url)

    Dataset_Americanas = create_dataframe(Links_Americanas, Sellers_Americanas, Price_Americanas, Installment_Americanas_valor_parcela, Title_Americanas)

    current_dir = os.getcwd()

    path_download = current_dir + '\Data\\' + brand + "\Files\\" + 'B2W_' + brand + ".xlsx"

    Dataset_Americanas.to_excel(path_download, index=False)




































