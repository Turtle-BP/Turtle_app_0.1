#Importando as bibliotecas
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from requests_html import HTML
from bs4 import BeautifulSoup
from tqdm import tqdm
import sqlite3
import datetime
import os

#Congiruando o driver
options = Options()
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
options.add_argument('--no-sandbox')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-logging'])

current_driver = os.getcwd()
selenium_path = current_driver + "\Data\Selenium\Selenium_101"

driver = webdriver.Chrome(executable_path=selenium_path, options=options)

#Criando listas
Urls_amazon = []
Urls_amazon_more = []
Products_Links = []
Amazon_price = []
Amazon_seller = []
Amazon_title = []
Amazon_installment_price_full = []
Amazon_seller_more = []
Amazon_price_more = []
Amazon_title_more = []
internacional_list = []
more_offers_list = []
Amazon_ID_More = []


#Função para criar os links de busca
def getting_n_creating_amazon(brand):
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

    # Criando uma nova coluna no database com a formatação certa
    df['Urls'] = df['Brand'] + "+" + df['Product_Name']

    # Criando a nova coluna que são as urls de pesquisa
    df['Urls_search'] = "https://www.amazon.com.br/s?k=" + df['Urls']

    return df

def search_links(url,df):
    global Urls_amazon

    time.sleep(3)

    driver.get(url)
    body_el = driver.find_element(By.CSS_SELECTOR, 'body')
    html_str = body_el.get_attribute('innerHTML')
    html_obj = HTML(html=html_str)

    Links = [x for x in html_obj.links]
    products_links = [f'https://www.amazon.com.br{x}' for x in Links]

    for link in products_links:
        Urls_amazon.append(link)

    Urls_amazon = [s for s in Urls_amazon if '/dp/' in s]
    Urls_amazon = [s for s in Urls_amazon if not '#customerReviews' in s]

def clean_link(brand, urls):
    #Pegando o diretório inicial
    current_dir = os.getcwd()

    #Criando o path para o banco
    Database_path = current_dir + "\Data\\" + brand + "\\" + brand + ".db"

    table = brand + "_exclusao"

    #Criando a Query
    query = "SELECT * FROM " + table

    connection = sqlite3.connect(Database_path)

    #Criando o dataset em brando
    df_itens = pd.read_sql_query(query, connection)

    clean_urls = pd.DataFrame()

    clean_urls['Urls_Completas'] = urls
    clean_urls['Urls_limpas'] = clean_urls['Urls_Completas'].str.partition("ref")[0]

    Urls_limpas = clean_urls['Urls_limpas'].tolist()

    for word in df_itens['Words']:
         Urls_limpas = [s for s in Urls_limpas if not word in s]

    clean_urls = pd.DataFrame()

    clean_urls['Urls_finais'] = Urls_limpas

    clean_urls['ASIN'] = clean_urls['Urls_finais'].str.partition("/dp/")[2].str.partition("/")[0]

    clean_urls.drop_duplicates(subset='ASIN',inplace=True)
    clean_urls.reset_index(inplace=True, drop=True)
    return clean_urls

def search_atributes(url):
    # Tempo para não haver o bloqueio
    time.sleep(10)

    # Entrando dentro do site com o driver
    driver.get(url)

    body_el = driver.find_element(By.CSS_SELECTOR, 'body')
    html_str = body_el.get_attribute('innerHTML')

    # Criando o Soup
    soup = BeautifulSoup(html_str, 'html.parser')

    # Fazendo o try do nome do vendedor
    try:
        seller = soup.find("a", attrs={"id": 'sellerProfileTriggerId'}).text
        Amazon_seller.append(seller)
    except:
        Amazon_seller.append("Erro")

    # Fazendo o try do preço do produto a vista
    try:
        Div_Price = soup.find('div', attrs={"data-feature-name": "corePrice"})
        price = Div_Price.find(class_='a-offscreen').text
        Amazon_price.append(price)
    except:
        Amazon_price.append("Erro")

    # Pegando o título do produto
    try:
        title = soup.find(id='productTitle').text
        Amazon_title.append(title)
    except:
        Amazon_title.append('Erro')

    # Pegando o internacional
    try:
        soup.find('img', attrs={'data-a-hires': 'https://images-na.ssl-images-amazon.com/images/G/32/foreignseller/Foreign_Seller_Badge_v2._CB403622375_.png'})
        internacional_list.append("Internacional")
    except:
        internacional_list.append("Nacional")

    # Fazendo o try para pegar o preço da parcela
    try:
        installment = soup.find(class_='best-offer-name a-text-bold').text
        Amazon_installment_price_full.append(installment)
    except:
        Amazon_installment_price_full.append("0")

    # Fazendo o try para ver se tem mais ofertas
    try:
        Main_Div_More_offers = soup.find('div', attrs={"id": "olpLinkWidget_feature_div"})
        Div_More_offers = Main_Div_More_offers.find('div', attrs={'class': 'a-section olp-link-widget'})
        Div_More_offers_text = Div_More_offers.find('div', attrs={'class': 'olp-text-box'}).text
        more_offers_list.append(Div_More_offers_text)
    except:
        more_offers_list.append("Comparar outras 0 ofertas")

def dataset_amazon(url, sellers, preco, titulo, more_url, brand):
    # Criando o DataFrame
    Dataset_amazon = pd.DataFrame()

    # Colocando os dados
    Dataset_amazon['URL'] = url

    Dataset_amazon['DATE'] = pd.to_datetime('today', errors='ignore').date()

    Dataset_amazon['MARKETPLACE'] = "AMAZON"

    # Arrumando a coluna de sellers
    Dataset_amazon['SELLER'] = sellers
    Dataset_amazon['SELLER'] = Dataset_amazon['SELLER'].str.replace("Erro", "Amazon", regex=False)

    # Arrumando o preço
    Dataset_amazon['PRICE'] = preco
    Dataset_amazon['PRICE'] = Dataset_amazon['PRICE'].str.replace(".", "", regex=True)
    Dataset_amazon['PRICE'] = Dataset_amazon['PRICE'].str.replace("R$", "", regex=False)
    Dataset_amazon['PRICE'] = Dataset_amazon['PRICE'].str.replace(",", ".", regex=True)

    # Arrumando os valores de installment
    Dataset_amazon['INSTALLMENT FULL'] = Amazon_installment_price_full
    Dataset_amazon['PARCEL'] = Dataset_amazon['INSTALLMENT FULL'].str.extract('(\d+)')
    Dataset_amazon['PARCEL'] = Dataset_amazon['PARCEL'].astype("int")
    Dataset_amazon['parcel_price_bruto'] = Dataset_amazon['INSTALLMENT FULL'].str.partition("R$")[2].str.partition(" ")[2].str.partition(" ")[0]
    Dataset_amazon['Installment3'] = Dataset_amazon['parcel_price_bruto'].str.extract('(\d+)')
    Dataset_amazon['parcel_price_bruto'] = Dataset_amazon['INSTALLMENT FULL'].str.partition("R$")[2].str.partition(" ")[2].str.partition(" ")[0].str.partition(",")[2]
    Dataset_amazon['Installment4'] = Dataset_amazon['parcel_price_bruto'].str.extract('(\d+)')
    Dataset_amazon['INSTALLMENT'] = Dataset_amazon['Installment3'] + "." + Dataset_amazon['Installment4']
    Dataset_amazon['INSTALLMENT'] = Dataset_amazon['INSTALLMENT'].astype("float")
    Dataset_amazon['INSTALLMENT'] = Dataset_amazon['INSTALLMENT'].fillna(0)
    Dataset_amazon['INSTALLMENT_PAYMENT'] = Dataset_amazon['PARCEL'] * Dataset_amazon['INSTALLMENT']

    Dataset_amazon['ID'] = Dataset_amazon['URL'].str.partition('/dp/')[2].str.partition('/')[0]
    Dataset_amazon['PRODUCT'] = titulo
    Dataset_amazon['INTERNACIONAL'] = internacional_list

    # Arrumando valores de mais sellers
    Dataset_amazon['MORE'] = more_url
    Dataset_amazon['MORE'] = Dataset_amazon['MORE'].str.partition("outras ")[2].str.partition(" ofertas")[0]

    Dataset_amazon['MORE'] = Dataset_amazon['MORE'].astype('int')

    Dataset_amazon = Dataset_amazon.drop(columns=["INSTALLMENT FULL", "Installment3", "Installment4", "parcel_price_bruto"])

    # Pegando os itens certos
    Dataset_amazon = Dataset_amazon[Dataset_amazon["PRICE"] != "Erro"]
    Dataset_amazon['PRICE'] = Dataset_amazon['PRICE'].astype('float')

    # Colocando na ordem correta
    Dataset_amazon = Dataset_amazon[['DATE', 'URL', 'MARKETPLACE', 'SELLER', 'PRICE', 'PARCEL', 'INSTALLMENT', 'INSTALLMENT_PAYMENT', 'ID','PRODUCT', 'INTERNACIONAL', 'MORE']]

    if brand == "GoPro":
        Dataset_amazon = Dataset_amazon[Dataset_amazon['PRICE'] > 900]
    elif brand == 'Motorola':
        Dataset_amazon = Dataset_amazon[Dataset_amazon['PRICE'] > 70]
    elif brand == 'Wacom':
        Dataset_amazon = Dataset_amazon[Dataset_amazon['PRICE'] > 100]

    return Dataset_amazon

def Search_Less_then_10(ASIN):
    global Amazon_seller_more

    #Fazendo o time
    time.sleep(5)

    #Criando a nova url
    new_url = "https://www.amazon.com.br/gp/product/ajax/?asin=" + ASIN + "&pageno=1&experienceId=aodAjaxMain"

    #Pegando driver
    driver.get(new_url)

    #Pegando o html
    body_el = driver.find_element(By.CSS_SELECTOR, 'body')
    html_str = body_el.get_attribute('innerHTML')

    #Criando o Soup
    Soup = BeautifulSoup(html_str, 'html.parser')

    #Fazendo o loop para pegar todos os sellers
    for seller in Soup.find_all(class_='a-size-small a-link-normal')[4:]:
        Amazon_seller_more.append(seller.text)

    #Limpando os sellers
    Amazon_seller_more =  [s for s in Amazon_seller_more if not 'Política de devolução' in s]
    Amazon_seller_more =  [s for s in Amazon_seller_more if not 'Apagar tudo' in s]
    Amazon_seller_more =  [s for s in Amazon_seller_more if len(s) > 1]

    #Fazendo o loop para pegar os preços
    for price in Soup.find_all(class_='a-offscreen')[2:]:
        Amazon_price_more.append(price.text)
        Amazon_ID_More.append(ASIN)

def Search_Less_then_20(ASIN):
    global Amazon_seller_more

    #Fazendo o time
    time.sleep(5)

    #Criando a nova url
    new_url = "https://www.amazon.com.br/gp/product/ajax/?asin=" + ASIN + "&pageno=2&experienceId=aodAjaxMain"

    #Pegando driver
    driver.get(new_url)

    #Pegando o html
    body_el = driver.find_element(By.CSS_SELECTOR, 'body')
    html_str = body_el.get_attribute('innerHTML')

    #Criando o Soup
    Soup = BeautifulSoup(html_str, 'html.parser')

    #Fazendo o loop para pegar todos os sellers
    for seller in Soup.find_all(class_='a-size-small a-link-normal'):
        Amazon_seller_more.append(seller.text)

    #Limpando os sellers
    Amazon_seller_more =  [s for s in Amazon_seller_more if not 'Política de devolução' in s]
    Amazon_seller_more =  [s for s in Amazon_seller_more if not 'Apagar tudo' in s]
    Amazon_seller_more =  [s for s in Amazon_seller_more if len(s) > 1]

    #Fazendo o loop para pegar os preços
    for price in Soup.find_all(class_='a-offscreen'):
        Amazon_price_more.append(price.text)
        Amazon_ID_More.append(ASIN)

def Search_Less_then30(ASIN):
    global Amazon_seller_more

    #Fazendo o time
    time.sleep(5)

    #Criando a nova url
    new_url = "https://www.amazon.com.br/gp/product/ajax/?asin=" + ASIN + "&pageno=3&experienceId=aodAjaxMain"

    #Pegando driver
    driver.get(new_url)

    #Pegando o html
    body_el = driver.find_element(By.CSS_SELECTOR, 'body')
    html_str = body_el.get_attribute('innerHTML')

    #Criando o Soup
    Soup = BeautifulSoup(html_str, 'html.parser')

    #Fazendo o loop para pegar todos os sellers
    for seller in Soup.find_all(class_='a-size-small a-link-normal'):
        Amazon_seller_more.append(seller.text)

    #Limpando os sellers
    Amazon_seller_more =  [s for s in Amazon_seller_more if not 'Política de devolução' in s]
    Amazon_seller_more =  [s for s in Amazon_seller_more if not 'Apagar tudo' in s]
    Amazon_seller_more =  [s for s in Amazon_seller_more if len(s) > 1]

    #Fazendo o loop para pegar os preços
    for price in Soup.find_all(class_='a-offscreen'):
        Amazon_price_more.append(price.text)
        Amazon_ID_More.append(ASIN)



def dataset_more_amazon(ID, Sellers, Price):
    Dataframe_More = pd.DataFrame()
    Dataframe_More['ID'] = ID

    Dataframe_More['DATE'] = pd.to_datetime('today', errors='ignore').date()

    Dataframe_More['MARKETPLACE'] = 'AMAZON'

    Dataframe_More['SELLER'] = Sellers

    Dataframe_More['PRICE'] = Price
    Dataframe_More['PRICE'] = Dataframe_More['PRICE'].str.replace(".", "", regex=True)
    Dataframe_More['PRICE'] = Dataframe_More['PRICE'].str.replace("R$", "", regex=False)
    Dataframe_More['PRICE'] = Dataframe_More['PRICE'].str.replace(",", ".", regex=True)
    Dataframe_More['PRICE'] = Dataframe_More['PRICE'].astype('float')

    Dataframe_More['PARCEL'] = 10

    Dataframe_More['INSTALLMENT'] = Dataframe_More['PRICE'] / Dataframe_More['PARCEL']

    Dataframe_More['INSTALLMENT_PAYMENT'] = Dataframe_More['PRICE'] * Dataframe_More['PARCEL']

    Dataframe_More['INTERNACIONAL'] = 'ERRO'

    url_names = []
    for id in Dataframe_More['ID']:
        url_names.append(Df_Product_without_More.loc[Df_Product_without_More['ID'] == id, 'URL'].values[0])

    products_names = []
    for id in Dataframe_More['ID']:
        products_names.append(Df_Product_without_More.loc[Df_Product_without_More['ID'] == id, 'PRODUCT'].values[0])

    Dataframe_More['URL'] = url_names
    Dataframe_More['PRODUCT'] = products_names

    return Dataframe_More


def amazon_final(brand):
    global Df_Product_without_More

    database = getting_n_creating_amazon(brand)

    for url in tqdm(database['Urls_search']):
        search_links(url,database)

    dataset_correct = clean_link(brand, Urls_amazon)

    for url in tqdm(dataset_correct['Urls_finais']):
        search_atributes(url)

    Df_Product_without_More = dataset_amazon(dataset_correct['Urls_finais'], Amazon_seller, Amazon_price, Amazon_title, more_offers_list, brand)

    Df_Product_without_More.to_excel(r"C:\Users\pedro\Documents\Turte Brand Protection\Turtle_Thinker_Alpha_0.1\Amazon.xlsx", index=False)

    Df_More = Df_Product_without_More[Df_Product_without_More['MORE'] != 0]

    for id in tqdm(Df_More['ID']):
        Search_Less_then_10(id)

    Df_More_with_values = dataset_more_amazon(Amazon_ID_More,Amazon_seller_more,Amazon_price_more)

    Final_Df = pd.concat([Df_Product_without_More, Df_More_with_values])


    Final_Df.to_excel(r"C:\Users\pedro\Documents\Turte Brand Protection\Turtle_Thinker_Alpha_0.1\Amazon_Final.xlsx", index=False)










































































