#IMPORTANDO AS BIBLIOTECAS
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from tqdm import tqdm
import sqlite3
import json
import os

#Congiruando o driver
options = Options()
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
options.add_argument('--no-sandbox')
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.52")

#driver = webdriver.Chrome(executable_path=r"C:\Users\pedro\Documents\Turte Brand Protection\Turtle_Thinker_Alpha_0.1\Data\Selenium\Selenium_99", options=options)

#CRIANDO A LISTA DE VALORES
Urls_Extra = []
Sellers_Extra = []
Country_Extra = []
Price_Extra = []
SKU_Extra = []
Title_Extra = []
Installment_Extra_quantidade = []
Installment_Extra_valor_parcela = []
Installment_Extra_valor_total = []
Prox_pag = []

#Função para criar os links de busca
def getting_n_creating_viavarejo_urls(brand):
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
    df['Product_Name'] = df['Product_Name'].str.replace(" ", "%2B")
    df['Product_Name'] = df['Product_Name'].str.replace("-", "%2B")

    # Criando uma nova coluna no database com a formatação certa
    df['Urls'] = df['Brand'] + "+" + df['Product_Name']

    # Criando a nova coluna que são as urls de pesquisa
    df['Urls_search'] = "https://prd-api-partner.viavarejo.com.br/api/search?resultsPerPage=20&terms=" + df['Brand'][0] + "%2B" + df['Product_Name'] + "&page=1&apiKey=extra&"

    return df

def get_attributes(url):
    time.sleep(5)
    driver.get(url)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    elemento = soup.find('body')

    dic = json.loads(elemento.text)

    # ID
    number_id = 0
    for i in dic['products']:
        try:
            SKU_Extra.append(dic['products'][number_id]['url'])
        except:
            SKU_Extra.append("ERRO")

        number_id = number_id + 1

    # NOME
    number_name = 0
    for i in dic['products']:
        try:
            Title_Extra.append(dic['products'][number_name]['name'])
        except:
            Title_Extra.append("ERRO")

        number_name = number_name + 1

    # SELLER NUMBER
    number_seller = 0
    for i in dic['products']:
        try:
            Sellers_Extra.append(dic['products'][number_seller]['details']['IdLojista'])
        except:
            Sellers_Extra.append("ERRO")

        number_seller = number_seller + 1

    # INTERNACIONAL
    number_internacional = 0
    for i in dic['products']:
        try:
            Country_Extra.append(dic['products'][number_internacional]['details']['categoryName'])
        except:
            Country_Extra.append("ERRO")

        number_internacional = number_internacional + 1

    # PRICE
    number_price = 0
    for i in dic['products']:
        try:
            Price_Extra.append(dic['products'][number_price]['price'])
        except:
            Price_Extra.append("ERRO")

        number_price = number_price + 1

    # INSTALLMENT PARCELA
    number_parcela = 0
    for i in dic['products']:
        try:
            Installment_Extra_quantidade.append(dic['products'][number_parcela]['installment']['count'])
        except:
            Installment_Extra_quantidade.append("ERRO")

        number_parcela = number_parcela + 1

    # INSTALLMENT VALOR PARCELA
    number_valor = 0
    for i in dic['products']:
        try:
            Installment_Extra_valor_parcela.append(dic['products'][number_valor]['installment']['price'])
        except:
            Installment_Extra_valor_parcela.append("ERRO")

        number_valor = number_valor + 1

    # try da próxima página
    try:
        Prox_pag.append(dic['pagination']['next'])
    except:
        pass

def creating_dataframe(Sellers,Country,Price,Quantidade,SKU,Title,Parcela):
    Dataframe = pd.DataFrame()

    Dataframe['URL'] = SKU
    Dataframe['Loja'] = 'EXTRA'
    Dataframe['Sellers'] = Sellers
    Dataframe['Price'] = Price
    Dataframe['Quantidade'] = Quantidade
    Dataframe['Parcela'] = Parcela
    Dataframe['SKU'] = Dataframe['URL'].str.partition("IdSku=")[2]
    Dataframe['Title'] = Title
    Dataframe['Country'] = Country

    #Dataframe['Country'] = Dataframe['Country'].str.replace("['Produtos Importados']","Internacional")

    Dataframe = Dataframe[~Dataframe['Title'].str.contains("película")]
    Dataframe = Dataframe[~Dataframe['Title'].str.contains("Película")]
    Dataframe = Dataframe[~Dataframe['Title'].str.contains("Capa")]
    Dataframe = Dataframe[~Dataframe['Title'].str.contains("Hydrogel")]
    Dataframe = Dataframe[~Dataframe['Title'].str.contains("Fibra")]
    Dataframe = Dataframe[~Dataframe['Title'].str.contains("Fullmosa")]
    Dataframe = Dataframe[~Dataframe['Title'].str.contains("Estojo")]
    Dataframe = Dataframe[~Dataframe['Title'].str.contains("MoKo")]


    return Dataframe

def ViaVarejo_final(brand):
    global Prox_pag

    df = getting_n_creating_viavarejo_urls(brand)

    for url in tqdm(df['Urls_search']):
        get_attributes(url)

    #Prox_pag = [s for s in Prox_pag if s is not None]

    #Prox_pag = [s.replace("/engage/search/v3/search?", "https://prd-api-partner.viavarejo.com.br/api/search?") for s in Prox_pag]

    #for url in tqdm(Prox_pag):
        #try:
            #get_attributes(url)
        #except:
            #pass

    dataset_viavarejo = creating_dataframe(Sellers_Extra,Country_Extra,Price_Extra,Installment_Extra_quantidade,SKU_Extra,Title_Extra,Installment_Extra_valor_parcela)

    dataset_viavarejo.to_excel(r"C:\Users\pedro\Documents\Turte Brand Protection\Turtle_Thinker_Alpha_0.1\Via_Varejo.xlsx", index=False)



