#IMPORTANDO AS BIBLIOTECAS
#IMPORTANDO AS BIBLIOTECAS
import pandas as pd
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.request import urlopen
import requests
import sqlite3
import json
import sqlite3
import os

#GUARDANDO LISTAS
Urls_Carrefour = []
Sellers_Carrefour = []
Country_Carrefour = []
Price_Carrefour = []
Price_Carrefour_2 = []
SKU_Carrefour = []
Title_Carrefour = []
Installment_Carrefour_quantidade = []
Installment_Carrefour_valor_parcela = []
Installment_Carrefour_valor_total = []

header = {'authority':'www.carrefour.com.br', 'scheme':'https', 'accept':'application/json','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

#Função para criar os links de busca
def getting_n_creating_carrefour_urls(brand):
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
    df['Product_Name'] = df['Product_Name'].str.replace(" ", "%20")
    df['Product_Name'] = df['Product_Name'].str.replace("-", "%20")

    # Criando uma nova coluna no database com a formatação certa
    df['Urls'] = df['Brand'] + "%20" + df['Product_Name']

    # Criando a nova coluna que são as urls de pesquisa
    df['Urls_search'] = "https://www.carrefour.com.br/busca/" + df['Urls']

    return df

def get_atributes(url):
    time.sleep(5)

    response = requests.get(url, headers=header)
    html = response.text

    bs = BeautifulSoup(html, 'html.parser')

    template = bs.find('template', attrs={'data-type':'json','data-varname':'__STATE__'})

    text = template.contents[1].string

    data = json.loads(text)

    principal_key = list(data.keys())

    keys_principal = []

    for key in principal_key:
        keys_principal.append(key)

    keys_principal = [s for s in keys_principal if 'Product' in s]
    keys_principal = [s for s in keys_principal if not '$' in s]

    Data_json = pd.DataFrame()
    Data_json['Keys'] = keys_principal
    Data_json['Code'] = Data_json['Keys'].str.partition(":")[2].str.partition(".")[0]
    Data_json = Data_json.drop_duplicates(subset=['Code'])
    Data_json['Price_id'] = "$" + Data_json['Keys'] + '.items({\"filter\":\"ALL_AVAILABLE\"}).0.sellers.0.commertialOffer'
    Data_json['Sellers_id'] = Data_json['Keys'] + '.items({\"filter\":\"ALL_AVAILABLE\"}).0.sellers.0'

    #Pegando title
    for key in Data_json['Keys']:
        try:
            Title_Carrefour.append(data[key]['productName'])
        except:
            Title_Carrefour.append("Erro")

    #Pegando SKU
    for key in Data_json['Keys']:
        try:
            SKU_Carrefour.append(data[key]['productReference'])
        except:
            SKU_Carrefour.append("Erro")

    #Pegando Url
    for key in Data_json['Keys']:
        try:
            Urls_Carrefour.append("www.carrefour.com.br" + data[key]['link'])
        except:
            Urls_Carrefour.append("Erro")

    #Pegando Price
    for key in Data_json['Price_id']:
        try:
            Price_Carrefour.append(data[key]['Price'])
        except:
            Price_Carrefour.append("Erro")

    #Pegando Price 2
    for key in Data_json['Price_id']:
        try:
            Price_Carrefour_2.append(data[key]['spotPrice'])
        except:
            Price_Carrefour_2.append("Erro")

    #Pegando Seller
    for key in Data_json['Sellers_id']:
        try:
            Sellers_Carrefour.append(data[key]['sellerName'])
        except:
            Sellers_Carrefour.append("Erro")

def creating_dataframe(urls, loja, title, price, price_2, sellers, sku):
    Dataset = pd.DataFrame()

    Dataset['Urls'] = urls
    Dataset['Loja'] = loja
    Dataset['Title'] = title
    Dataset['Price'] = price
    Dataset['Price_2'] = price_2
    Dataset['Sellers'] = sellers
    Dataset['SKU'] = sku

    return Dataset

def carrefour_final(brand):

    df = getting_n_creating_carrefour_urls(brand)

    for url in tqdm(df['Urls_search']):
        get_atributes(url)

    Dataset_Carrefour = creating_dataframe(Urls_Carrefour,"CARREFOUR",Title_Carrefour,Price_Carrefour,Price_Carrefour_2,Sellers_Carrefour,SKU_Carrefour)
    Dataset_Carrefour.to_excel(r"C:\Users\pedro\Documents\Turte Brand Protection\Turtle_Thinker_Alpha_0.1\Carrefour.xlsx", index=False)

    #with open("sample.json", "w") as outfile:
        #json.dump(data, outfile)
































































