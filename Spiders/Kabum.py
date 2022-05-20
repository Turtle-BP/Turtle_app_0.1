#Importando as bibliotecas
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sqlite3
from tqdm import tqdm
import os

headers = {'authority':'www.kabum.com.br',
           'method':'GET',
           'scheme':'https',
           'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'accept-encoding':'gzip, deflate, br',
           'accept-language':'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
           'referer':'https://www.kabum.com.br/',
           'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.75'}

Links_Kabum = []
Urls_Kabum = []
Sellers_Kabum = []
Country_Kabum = []
Price_Kabum = []
SKU_Kabum = []
Title_Kabum = []
Installment_Kabum_quantidade = []
Installment_Kabum_valor_parcela = []
Installment_Kabum_valor_total = []

#Função para criar os links de busca
def getting_n_creating_kabum(brand):
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
    df['Product_Name'] = df['Product_Name'].str.replace(" ", "+")
    df['Product_Name'] = df['Product_Name'].str.replace("-", "+")

    # Criando uma nova coluna no database com a formatação certa
    df['Urls'] = df['Brand'] + "+" + df['Product_Name']

    # Criando a nova coluna que são as urls de pesquisa
    df['Urls_search'] = "https://www.kabum.com.br/busca?query=" + df['Urls']

    return df

def search_links(url):
    global Links_Kabum

    time.sleep(20)

    response = requests.get(url, headers=headers)
    html = response.text

    Soup = BeautifulSoup(html, 'html.parser')

    for a in Soup.find_all("a", href=True):
        Links_Kabum.append("https://www.kabum.com.br" + a['href'])

    Links_Kabum = [s for s in Links_Kabum if 'produto' in s]


def get_attributes(url):
    time.sleep(30)

    response = requests.get(url, headers=headers)
    html = response.text

    Soup = BeautifulSoup(html, 'html.parser')

    #Titulo
    try:
        Title_Kabum.append(Soup.find("h1", attrs={'itemprop':'name'}).text)
    except:
        Title_Kabum.append("Erro")

    #Preço
    try:
        Price_Kabum.append(Soup.find("h4", attrs={'itemprop':'price'}).text)
    except:
        Price_Kabum.append("Erro")

    #Seller
    try:
        Sellers_Kabum.append(Soup.find('div', attrs={'id':'blocoValores'}).text)
    except:
        Sellers_Kabum.append("Erro")

    #Installment
    try:
        Installment_Kabum_quantidade.append(Soup.find(class_='cardParcels').text)
    except:
        Installment_Kabum_quantidade.append("Erro")


def dataset_creation(urls, sellers, prices, installments, titles):
    df_raw = pd.DataFrame()

    Hoje = pd.to_datetime('today', errors='ignore').date()

    df_raw['URL'] = urls

    df_raw['DATE'] = Hoje

    df_raw['MARKETPLACE'] = 'Kabum'

    df_raw['SELLER'] = sellers
    df_raw['SELLER'] = df_raw['SELLER'].str.partition("Vendido e entregue por: ")[2].str.partition(" |")[0]

    df_raw['Installment_lixo'] = installments

    df_raw['PARCEL'] = df_raw['Installment_lixo'].str.partition("x")[0].str.extract('(\d+)')

    df_raw['INSTALLMENT'] = df_raw['Installment_lixo'].str.partition("R$")[2]
    df_raw['INSTALLMENT'] = df_raw['INSTALLMENT'].str.partition(" ")[0]
    df_raw['INSTALLMENT'] = df_raw['INSTALLMENT'].str.replace(",",".", regex=True)
    df_raw['INSTALLMENT'] = df_raw['INSTALLMENT'].str.replace("\xa0","", regex=False)

    #df_raw['INSTALLMENT'] = df_raw['INSTALLMENT'].astype('float')

    df_raw['PRODUCT'] = titles

    df_raw['PRICE'] = prices

    df_raw = df_raw[df_raw['PRICE'] != "Erro"]

    df_raw['PRICE'] = df_raw['PRICE'].str.replace("R$","", regex=False)
    df_raw['PRICE'] = df_raw['PRICE'].str.replace(".","", regex=False)
    df_raw['PRICE'] = df_raw['PRICE'].str.replace(",",".", regex=False)
    df_raw['PRICE'] = df_raw['PRICE'].str.replace("\xa0","", regex=False)
    df_raw['PRICE'] = df_raw['PRICE'].astype('float')

    df_raw['ID'] = df_raw['URL'].str.partition("produto/")[2].str.partition("/")[0]

    df_raw = df_raw[['DATE', 'URL', 'MARKETPLACE', 'SELLER', 'PRICE', 'PARCEL','INSTALLMENT','ID','PRODUCT']]


    return df_raw

def Kabum_final(brand):
    df = getting_n_creating_kabum(brand)

    for url in tqdm(df['Urls_search']):
        search_links(url)

    for url in tqdm(Links_Kabum):
        get_attributes(url)

    Dataset_Kabum = dataset_creation(Links_Kabum, Sellers_Kabum, Price_Kabum, Installment_Kabum_quantidade, Title_Kabum)

    current_dir = os.getcwd()

    path_download = current_dir + '\Data\\' + brand + "\Files\\" + 'Kabum_' + brand + ".xlsx"

    Dataset_Kabum.to_excel(path_download, index=False)
