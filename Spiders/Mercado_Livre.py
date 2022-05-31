#IMPORTANDO AS BIBLIOTECAS
import pandas as pd
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.request import urlopen
import sqlite3
import os

#Criando as listas para armazenar os dados
ml_url_base = []
ml_urls = []
ml_price = []
ml_seller = []
ml_installment = []
ml_catalog_id = []
ml_catalog_db = []
ml_idetifaction = []
lista_identification_url = []

#Função para criar os links de busca
def getting_n_creating_mercadolivre_urls(brand):
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
    df['Urls_search'] = "https://lista.mercadolivre.com.br/" + df['Urls'] + "_ITEM*CONDITION_2230284_NoIndex_True?#applied_value_name%3DNovo%"

    return df

def search_links(url,df):
    # Colocando URL commo Global
    global ml_urls

    # Colocando um tempo mínimo de 3 segundos
    time.sleep(3)

    # Fazendo o response
    response = urlopen(url)
    html = response.read()

    # Criando o BeautifulSoup
    BS = BeautifulSoup(html, 'html.parser')

    # Pegando todos os links da página
    for link in BS.find_all("a", href=True):
        ml_urls.append(link['href'])

    # Pegando as próximas páginas
    try:
        next_page_link = BS.find_all(class_='andes-pagination__arrow-title')[-1].text

        # Vendo se na seta está escrito 'Seguinte'
        if next_page_link == 'Seguinte':
            next_url = BS.find_all(class_='andes-pagination__link ui-search-link')[-1]['href']

            # Realizando o loop da função com o link da próxima página
            search_links(next_url)
    except:
        pass

    # Limpando as urls
    ml_urls = [s for s in ml_urls if 'tracking_id' in s]
    ml_urls = [s for s in ml_urls if 'produto' in s]
    ml_urls = [s for s in ml_urls if df['Brand'][0] in s]

    # Tirando as duplicadas
    ml_urls = list(dict.fromkeys(ml_urls))

def search_attributes(url):
    #Criando tempo
    time.sleep(2)

    #Fazendo o response jh
    response = urlopen(url)
    html = response.read()

    #Criando o soup
    BS = BeautifulSoup(html, 'html.parser')

        #Buscando o preço
    try:
        price = BS.find(class_='andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact').text
        ml_price.append(price)
    except:
        ml_price.append("ERRO")

    #Buscando o installment
    try:
        installment = BS.find(class_='ui-pdp-color--GREEN ui-pdp-size--MEDIUM ui-pdp-family--REGULAR').text
        ml_installment.append(installment)
    except:
        installment = BS.find(class_='ui-pdp-color--BLACK ui-pdp-size--MEDIUM ui-pdp-family--REGULAR').text
        ml_installment.append(installment)

    #Catalog
    try:
        catalog = BS.find(class_='ui-pdp-other-sellers mt-24')
        ml_catalog_db.append(catalog)
    except:
        ml_catalog_id.append("NORMAL")

    #Vendedor
    try:
        seller_link = BS.find(class_='ui-pdp-media__action ui-box-component__action')['href']
    except:
        seller_link = "Erro"

    try:
        #Entrando na página do vendedor
        response = urlopen(seller_link)
        html = response.read()

        #Criando o soup
        BS = BeautifulSoup(html, 'html.parser')

        #Achando o nome do seller
        seller_name = BS.find(class_='store-info__name').text

        #Append do nome do seller
        ml_seller.append(seller_name)
    except:
        ml_seller.append(seller_link)

def create_dataframe(url,seller,price,installment):
    Dataset = pd.DataFrame()

    Dataset['Url'] = url
    Dataset['Loja'] = 'MERCADO LIVRE'
    Dataset['Seller'] = seller
    Dataset['Price'] = price
    Dataset['Installment'] = installment

    # Arrumando a coluna de installment
    Dataset['Parcela'] = Dataset['Installment'].str.partition("x")[0]
    Dataset['Parcela'] = Dataset['Parcela'].str.extract("(\d+)").astype(int)
    Dataset["reais"] = Dataset["Installment"].str.partition("reales")[0].str.partition("x")[2]
    Dataset["moedas"] = Dataset["Installment"].str.partition(" con")[2].str.partition("centavos")[0].str.partition(" ")[2]
    # Dataset['Installment'] = Dataset['reais'] + "." + Dataset['moedas']

    #Dataset['Catalog'] = catalogo

    Dataset['ASIN'] = Dataset['Url'].str.partition("/")[2].str.partition("/")[2].str.partition("/")[2].str.partition("-")[0]
    Dataset['ASIN_2'] = Dataset['Url'].str.partition("/")[2].str.partition("/")[2].str.partition("/")[2].str.partition("-")[2].str.partition("-")[0]

    Dataset['ASIN_CORRETO'] = Dataset['ASIN'] + Dataset['ASIN_2']

    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/HUAWEIOFICIAL?brandId=3562",'HUAWEI LOJA OFICIAL')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/MPCEL+MOBILE?brandId=3430",'Mpcel Loja Oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/MPCEL+MOBILE?brandId=3562",'MPCEL MOBILE')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/ONOFREELETROSERRA?brandId=2156",'Onofre Loja Oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/ZOOM_STORE?brandId=3598",'Zoom Store Loja Oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/FASTSHOP+OFICIAL?brandId=942",'Fast Shop Loja oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/MERCADOLIVRE+ELETRONICOS?brandId=2707",'Mercado Livre Loja oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/MERCADOLIVRE+ELETRONICOS?brandId=2707", 'Olist Loja oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://www.mercadolivre.com.br/perfil/OLIST?brandId=866", 'Olist Loja oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://www.mercadolivre.com.br/perfil/OLIST-STORE+PREMIUM?brandId=866",'Olist Loja oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://www.mercadolivre.com.br/perfil/OLIST-STORE+SP?brandId=866", 'Olist Loja oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://www.mercadolivre.com.br/perfil/SUNTEKSTOREBR?brandId=2203",'Suntek Loja oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/SUNTEKSTOREBR?brandId=2203",'Suntek Loja oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/OLIST?brandId=866",'Olist Loja oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/OLIST-STORE+PREMIUM?brandId=866",'Olist Loja oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/OLIST-STORE+SP?brandId=866",'Olist Loja oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/E-SPOT?brandId=4166",'Wacom Loja Oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/IBYTE.?brandId=3979",'Ibyte Loja Oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/INPOWER+INFO?brandId=1655",'INPOWER Loja Oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/PICHAUINFORMATICA?brandId=1436",'Pichau Loja Oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/PRIMETEK+COMPUTADORES?brandId=2255",'Primetek Loja Oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/VLSTORE+INFORMATICA?brandId=3629", 'Leva Digital Loja Oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://www.mercadolivre.com.br/perfil/MIMI2231343?brandId=3396", 'Miranda Loja Oficial')
    Dataset['Seller'] = Dataset['Seller'].replace("https://perfil.mercadolivre.com.br/MIMI2231343?brandId=3396",'Miranda Loja Oficial')

    Dataset.drop(['ASIN','ASIN_2'], axis=1, inplace=True)

    return Dataset

#APLICATIVO
def Mercado_livre_final(brand):
    df = getting_n_creating_mercadolivre_urls(brand)

    for url in tqdm(df['Urls_search']):
        search_links(url,df)

    for url in tqdm(ml_urls):
        search_attributes(url)

    dataset_mercadolivre = create_dataframe(ml_urls,ml_seller,ml_price,ml_installment)

    current_dir = os.getcwd()

    path_download = current_dir + '\Data\\' + brand + "\Files\\" + 'MercadoL_' + brand + ".xlsx"

    dataset_mercadolivre.to_excel(path_download, index=False)




















































































