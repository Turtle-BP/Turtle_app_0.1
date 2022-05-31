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
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#Pegando o caminho do Selenium
current_driver = os.getcwd()
selenium_path = current_driver + "\Data\Selenium\Selenium_101"

#Criando o driver
driver = webdriver.Chrome(executable_path=selenium_path, options=options)

#########  CRIANDO A LISTA DE VALORES #######################
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


#Listas Sellers
sellers_name_correct = []
internacional_name_correct = []
sellers_name = []
internacional_list = []

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

#Função para pegar os atributos
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

#Função para criar o dataframe original
def creating_dataframe(Sellers,Price,Quantidade,SKU,Title,Parcela):
    Dataframe = pd.DataFrame()

    #Colocando Url
    Dataframe['URL'] = SKU

    #Colocando Data
    Dataframe['DATE'] = pd.to_datetime('today', errors='ignore').date()

    Dataframe['MARKETPLACE'] = 'EXTRA'

    #Criando a condicional para pegar os valores dentro da lista de sellers que busca em JSON original
    correct_seller = []
    for seller in Sellers_Extra:
        correct_seller.append(seller[0])

    #Colocar o nome dos vendedores
    Dataframe['SELLER'] = correct_seller

    Dataframe['PRICE'] = Price

    Dataframe['PARCEL'] = Quantidade
    Dataframe['INSTALLMENT'] = Parcela

    #Criando coluna de Installment_payment
    Dataframe['INSTALLMENT_PAYMENT'] = Dataframe['PARCEL'] * Dataframe['INSTALLMENT']

    Dataframe['ID'] = Dataframe['URL'].str.partition("IdSku=")[2]
    Dataframe['PRODUCT'] = Title

    #Colocando em ordem
    Dataframe = Dataframe[['DATE','URL','MARKETPLACE','SELLER','PRICE','PARCEL','INSTALLMENT','INSTALLMENT_PAYMENT','ID','PRODUCT']]

    return Dataframe

#Função para criar o dataframe dos sellers
def sellers_dataframe(url, sellers):
    #Criando o dataframe com as urls e sellers
    df_sellers = pd.DataFrame()

    #Colocando os dados
    df_sellers['URL'] = url
    df_sellers['SELLER'] = sellers

    #Retirando as duplicadas
    df_sellers.drop_duplicates(subset=['SELLER'], inplace=True)

    return df_sellers

#Função para os atributos dos sellers
def sellers_data(url):
    #Tempo
    time.sleep(3)

    #Abrindo o driver
    driver = webdriver.Chrome(executable_path=selenium_path, options=options)

    #Entrando na url
    driver.get(url)

    #tempo
    time.sleep(5)

    #Pegando o html
    html = driver.page_source

    #Fechando o driver
    driver.close()

    #Criando o soup
    Soup = BeautifulSoup(html, 'html.parser')

    #Try dos dados sellers
    try:
        sellers_name.append(Soup.find(class_='e1vg858b0 css-1kq6ah1 e1g7zzz30').text)
        try:
            internacional_list.append(Soup.find('img', attrs={'data-testid': 'stamps'})['alt'])
        except:
            internacional_list.append("NACIONAL")
    except:
        sellers_name.append("ERRO")
        internacional_list.append("ERRO")

#Função para arrumar o dataframe dos sellers
def sellers_final_dataframe(name, internacional, dataframe):
    #Colocando as novas colunas do dataframe
    dataframe['Name'] = name
    dataframe['INTERNACIONAL'] = internacional

    #Mudando o nome dos sellers
    dataframe['Name'] = dataframe['Name'].str.partition("por")[2]

    #Return
    return dataframe

#Função para o último dataframe
def final_dataframe(dataframe_final, dataframe_seller):
    #Criando a lista para colocar na coluna de forma correta
    for code in dataframe_final['SELLER']:
        sellers_name_correct.append(dataframe_seller.loc[dataframe_seller['SELLER'] == code,'Name'].values[0])

    #Criando a lista para colocar na coluna de internacional
    for code in dataframe_final['SELLER']:
        internacional_name_correct.append(dataframe_seller.loc[dataframe_seller['SELLER'] == code,'INTERNACIONAL'].values[0])

    #Colocando isso no dataframe_final
    dataframe_final['Seller_Name'] = sellers_name_correct
    dataframe_final['INTERNACIONAL'] = internacional_name_correct

    return dataframe_final

#Função FINAL
def ViaVarejo_final(brand):
    global Prox_pag

    #Pegando as urls
    df = getting_n_creating_viavarejo_urls(brand)

    #Pegando os atributos
    for url in tqdm(df['Urls_search']):
        get_attributes(url)

    #Criando o dataset
    dataset_viavarejo = creating_dataframe(Sellers_Extra,Price_Extra,Installment_Extra_quantidade,SKU_Extra,Title_Extra,Installment_Extra_valor_parcela)

    #Criando o dataframe dos sellers
    sellers_df = sellers_dataframe(dataset_viavarejo['URL'], dataset_viavarejo['SELLER'])

    #Pegando os atributos dos sellers
    for url in tqdm(sellers_df['URL']):
        sellers_data(url)

    #Colocando os atributos dentro do dataframe
    final_sellers_df = sellers_final_dataframe(sellers_name, internacional_list, sellers_df)

    #Fazendo o dataset final
    Final_DataFrame = final_dataframe(dataset_viavarejo, final_sellers_df)

    #Pegando o dir atual
    current_dir = os.getcwd()

    #Mudando o caminho do download do arquivo
    path_download = current_dir + '\Data\\' + brand + "\Files\\" + 'ViaVarejo_' + brand + ".xlsx"

    Final_DataFrame.to_excel(path_download, index=False)
