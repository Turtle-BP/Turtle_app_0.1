#Importando as bibliotecas
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from requests_html import HTML
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
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

driver = webdriver.Chrome(executable_path=r"C:\Users\pedro\Documents\Turte Brand Protection\Turtle_Thinker_Alpha_0.1\Data\Selenium\Selenium_101", options=options)

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

#Função para criar os links de busca
def getting_n_creating_amazon(brand):
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

    Soup = BeautifulSoup(html_str,'html.parser')

    for link in products_links:
        Urls_amazon.append(link)

    Urls_amazon = [s for s in Urls_amazon if '/dp/' in s]
    Urls_amazon = [s for s in Urls_amazon if not '#customerReviews' in s]

def clean_link(url):
    clean_urls = pd.DataFrame()

    clean_urls['Urls'] = url
    clean_urls['Urls'] = clean_urls['Urls'].str.partition("ref")[0]

    clean_urls['ASIN'] = clean_urls['Urls'].str.partition("/dp/")[2].str.partition("/")[0]

    return clean_urls

def search_atributes(url):
    #Tempo para não haver o bloqueio
    time.sleep(5)

    #Entrando dentro do site com o driver
    driver.get(url)

    time.sleep(5)

    body_el = driver.find_element(By.CSS_SELECTOR, 'body')
    html_str = body_el.get_attribute('innerHTML')

    #Criando o Soup
    soup = BeautifulSoup(html_str, 'html.parser')

    #Fazendo o try do nome do vendedor
    try:
        seller = soup.find(id='sellerProfileTriggerId').text
        Amazon_seller.append(seller)
    except:
        Amazon_seller.append("Erro")

    #Fazendo o try do preço do produto a vista
    try:
        price = soup.find(class_='a-offscreen').text
        Amazon_price.append(price)
    except:
        Amazon_price.append("Erro")

    #Pegando o título do produto
    try:
        title = soup.find(id='productTitle').text
        Amazon_title.append(title)
    except:
        Amazon_title.append('Erro')

    #Pegando o internacional
    try:
        soup.find('image', attrs={'data-a-hires':'https://images-na.ssl-images-amazon.com/images/G/32/foreignseller/Foreign_Seller_Badge_v2._CB403622375_.png'})
        internacional_list.append("Internacional")
    except:
        internacional_list.append("Nacional")

    #Fazendo o try para pegar o preço da parcela
    try:
        installment = soup.find(class_='best-offer-name a-text-bold').text
        Amazon_installment_price_full.append(installment)
    except:
        Amazon_installment_price_full.append("0")

    #Fazendo o try para ver se tem mais ofertas
    try:
        # Fazendo o link de mais ofertas do mesmo produto
        more_offers = 'https://www.amazon.com.br' + soup.find(class_='a-touch-link a-box olp-touch-link')['href']

        more_offers_list.append(more_offers)
    except:
        more_offers_list.append("SEM URL")

def more_offers_attributes_singular(url):

    # Criando a nova url para AJAX REQUEST
    nova_url = "https://www.amazon.com.br/gp/product/ajax/?asin=" + url.split("/")[5] + "&pageno=1&experienceId=aodAjaxMain"

    # Inicializando o driver
    driver.get(nova_url)
    body_el = driver.find_element(By.CSS_SELECTOR, 'body')
    html_str = body_el.get_attribute('innerHTML')

    # Criando o BeautifulSoup
    soup = BeautifulSoup(html_str, 'html.parser')

    seller_correct = []

    # Pegando todos os sellers
    for seller in soup.find_all(class_="a-size-small a-color-base")[3:]:
        seller_correct.append(seller.text)

    # Limpando os sellers
    seller_correct = [s for s in seller_correct if not "avaliações" in s]
    seller_correct = [s for s in seller_correct if not "avaliação" in s]
    seller_correct = [s for s in seller_correct if not " A" in s]
    seller_correct = [s for s in seller_correct if not "Recém" in s]

    # Fazendo o append do seller correto
    for seller in seller_correct:
        Urls_amazon_more.append(url)
        Amazon_seller_more.append(seller)

    # Pegando preço sujo
    for price in soup.find_all(class_="a-offscreen")[2:]:
        Amazon_price_more.append(price.text)

    if len(Amazon_seller_more) != len(Amazon_price_more):
        print("DIFERENÇA ERRADA")
        print(url)
    else:
        pass

def more_offers_attributes_plural(url):

    nova_url = "https://www.amazon.com.br/gp/product/ajax/?asin=" + url.split("/")[5] + "&pageno=2&experienceId=aodAjaxMain"

    #Inicializando o driver
    driver.get(nova_url)
    body_el = driver.find_element(By.CSS_SELECTOR, 'body')
    html_str = body_el.get_attribute('innerHTML')

    # Criando o BeautifulSoup
    soup = BeautifulSoup(html_str, 'html.parser')

    seller_correct = []

    # Pegando todos os sellers
    for seller in soup.find_all(class_="a-size-small a-color-base"):
        seller_correct.append(seller.text)

    # Limpando os sellers
    seller_correct = [s for s in seller_correct if not "avaliações" in s]
    seller_correct = [s for s in seller_correct if not "avaliação" in s]
    seller_correct = [s for s in seller_correct if not " A" in s]
    seller_correct = [s for s in seller_correct if not "Recém" in s]

    # Criando a lista correta de sellers
    # eller_correct = seller_correct[2:]

    # Fazendo o append do seller correto
    for seller in seller_correct:
        Urls_amazon_more.append(url)
        Amazon_seller_more.append(seller)

    # Pegando preço sujo
    for price in soup.find_all(class_="a-offscreen"):
        Amazon_price_more.append(price.text)

    if len(Amazon_seller_more) != len(Amazon_price_more):
        print("DIFERENÇA ERRADA")
        print(url)
    else:
        pass

def offers_full_seach(url):
    # Pegando o tempo
    time.sleep(3)

    # Pegando as páginas
    try:
        driver.get(url)

        time.sleep(10)

        body_el = driver.find_element(By.CSS_SELECTOR, 'body')
        html_str = body_el.get_attribute('innerHTML')

        # Criando o soup
        BS = BeautifulSoup(html_str, 'html.parser')

        # Pegando o número de sellers
        try:
            n_offers = BS.find(id="aod-filter-offer-count-string").text
            n_offers = n_offers.partition(" ")[0]

            if int(n_offers) < 10:

                more_offers_attributes_singular(url)

            else:

                more_offers_attributes_singular(url)
                more_offers_attributes_plural(url)

        except:
            #print(url)
            pass

    except:
        Urls_amazon_more.append(url)
        Amazon_seller_more.append("ERRO")
        Amazon_price_more.append("ERRO")

def offers_dataset(url,seller,price):
    Dataset_more = pd.DataFrame()

    Dataset_more['Urls'] = url
    Dataset_more['Seller'] = seller
    Dataset_more['Price'] = price

    return Dataset_more

def dataset_amazon(url, sellers, preco, titulo, more_url):
    # Criando o DataFrame
    Dataset_amazon = pd.DataFrame()

    # Pegando os dias de hoje
    today = datetime.date.today()

    # Colocando os dados
    Dataset_amazon['Data'] = today
    Dataset_amazon['Urls'] = url
    Dataset_amazon['Data'] = today
    Dataset_amazon['Loja'] = "AMAZON"
    Dataset_amazon['Sellers'] = sellers
    Dataset_amazon['preco'] = preco
    Dataset_amazon['INSTALLMENT FULL'] = Amazon_installment_price_full
    Dataset_amazon['Installment'] = Dataset_amazon['INSTALLMENT FULL'].str.extract('(\d+)')
    Dataset_amazon['Installment'] = Dataset_amazon['Installment'].astype("int")
    Dataset_amazon['parcel_price_bruto'] = \
    Dataset_amazon['INSTALLMENT FULL'].str.partition("R$")[2].str.partition(" ")[2].str.partition(" ")[0]
    Dataset_amazon['Installment3'] = Dataset_amazon['parcel_price_bruto'].str.extract('(\d+)')
    Dataset_amazon['parcel_price_bruto'] = \
    Dataset_amazon['INSTALLMENT FULL'].str.partition("R$")[2].str.partition(" ")[2].str.partition(" ")[0].str.partition(",")[2]
    Dataset_amazon['Installment4'] = Dataset_amazon['parcel_price_bruto'].str.extract('(\d+)')
    Dataset_amazon['parcelprice'] = Dataset_amazon['Installment3'] + "." + Dataset_amazon['Installment4']
    Dataset_amazon['parcelprice'] = Dataset_amazon['parcelprice'].astype("float")
    Dataset_amazon['preco a prazo'] = Dataset_amazon['Installment'] * Dataset_amazon['parcelprice']
    Dataset_amazon['ASIN'] = Dataset_amazon['Urls'].str.partition('/dp/')[2].str.partition('/')[0]
    Dataset_amazon['Título'] = titulo
    Dataset_amazon['More'] = more_url

    Dataset_amazon = Dataset_amazon.drop(columns=["INSTALLMENT FULL", "Installment3", "Installment4", "parcel_price_bruto"])

    #Limpando os dados
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("Mesh")]
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("Onu")]
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("D-link")]
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("D-Link")]
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("TP-link")]
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("TP link")]
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("TP Link")]
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("TP-Link")]
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("ONEPLUS")]
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("Razer")]
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("Headset")]
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("Y30")]
    Dataset_amazon = Dataset_amazon[~Dataset_amazon['Título'].str.contains("JBL")]

    return Dataset_amazon

def amazon_final(brand):

    database = getting_n_creating_amazon(brand)

    for url in tqdm(database['Urls_search']):
        search_links(url,database)

    dataset_correct = clean_link(Urls_amazon)

    for url in tqdm(dataset_correct['Urls']):
        search_atributes(url)

    Dataset_final = dataset_amazon(dataset_correct['Urls'], Amazon_seller, Amazon_price, Amazon_title, more_offers_list)

    Dataset_final.to_excel(r"C:\Users\pedro\Documents\Turte Brand Protection\Turtle_Thinker_Alpha_0.1\Amazon.xlsx", index=False)

    for url in tqdm(Dataset_final['More']):
        offers_full_seach(url)

    Dataset_final_more = offers_dataset(Urls_amazon_more, Amazon_seller_more, Amazon_price_more)


    Dataset_final_more.to_excel(r"C:\Users\pedro\Documents\Turte Brand Protection\Turtle_Thinker_Alpha_0.1\Amazon_More.xlsx", index=False)










































































