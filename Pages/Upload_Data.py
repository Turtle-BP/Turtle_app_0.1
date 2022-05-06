#Importando as bibliotecas padrão 
import os
import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter
from tkinter.constants import W
from typing import Text
import pandas as pd
import datetime
from tqdm import tqdm

#Pegando marcas
def getting_brands():
    #Pegando caminho do database
    current_dir = os.getcwd()

    Database_path = current_dir + "\Data\Brands.db"

    #Criando a conexão com o banco de dados
    Database = sqlite3.connect(Database_path)

    #Criando cursor
    c = Database.cursor()

    #Executando script para pegar os dados 
    c.execute("SELECT Brand FROM Brands")
    result = c.fetchall()
    c.close()

    result = [x[0] for x in result]

    return result
        
#Inspeção dos dados antes de subir para o Database
def Inspec(brand_name):
    #Abrindo os dados 
    data = pd.read_excel(r"G:\.shortcut-targets-by-id\1VAK5JIWTmtamcYtBHQGeL7FVwcki0pRp\BRAND PROTECTION\Brand Protection - Daily Report.xlsb", engine='pyxlsb', header=1,convert_float=True)
    
    #Arrumando a coluna da data 
    data['Date'] = pd.TimedeltaIndex(data['Date'], unit='d') + datetime.datetime(1899,12,30)

    #Limpando a primeira linha que é nula 
    data = data[1:]

    #Filtrando os dados 
    data_filtrada = data[data['Brand'] == brand_name]

    #Pegando apenas as colunas que irei utilizar para a construlão dos dados 
    data_filtrada = data_filtrada[['Store - Seller','Week','Date','Part','Seller','Suggested Price','Cash Price','Installment Price','Hiperlink','Item','Store Status','Store Group','From_To - Sellers','1P X 3P','Store Official?','Seller Official?','Cash Price Status','Installment Price Status','Action','Status Ad','Brand','Ad','Officiality','Item Classification','CUSTOMER CLASSIFICATION','CHANNEL']]

    #Mudando as colunas de Action para corrigir sozinha 
    data_filtrada['Action'] = data_filtrada['Action'].str.replace(r'(^.*In Progress.*$)', 'Mercado Livre - Take Down')
    data_filtrada['Action'] = data_filtrada['Action'].str.replace('Send Extrajudicial', 'Extrajudicial Sent')

    data_filtrada.loc[(data_filtrada['Ad'] == 'Catalog')&(data_filtrada['Action'] == 'Mercado Livre - Take Down'),'Action'] = "ML Catalog - Take Down"

    #Limpando os dados
    data_filtrada['Store - Seller'] = data_filtrada['Store - Seller'].str.replace("'","")

    data_filtrada['Seller'] = data_filtrada['Seller'].str.replace("'","")
    data_filtrada['From_To - Sellers'] = data_filtrada['From_To - Sellers'].str.replace("'","")
    data_filtrada['Item Classification'] = data_filtrada['Item Classification'].str.replace("'","")

    #Mostrando os dados 
    Shape_data.config(text="Quantidade de linhas: {}".format(int(data_filtrada.shape[0])))
    Min_data.config(text="Data mais antiga: {}".format(data_filtrada['Date'].min()))
    Max_data.config(text="Data mais recente: {}".format(data_filtrada['Date'].max()))

    #Atualizando botão 
    Start_button.config(text='Subir Dados', command=lambda: upload_data_into_database(brand_name, data_filtrada))

def upload_data_into_database(brand_name, data_correct):
    
    #Criando conexão com o banco de dados 
    database_name = brand_name + "/" + brand_name + ".db"

    database = sqlite3.connect("H:/.shortcut-targets-by-id/18Jh1Gsq2qXY5AFF7QJQLuQhj88DlX8-R/Turtle BP/Databases/{}".format(database_name))

    c = database.cursor()

    for index, row in data_correct.iterrows():
       c.execute('''INSERT INTO Motorola_historic (Store_Seller,
                                            Week,
                                            Date,
                                            Part,
                                            Seller,
                                            Suggested_price,
                                            Cash_price,
                                            Installment_price,
                                            Hiperlink,
                                            Item,
                                            Store_status,
                                            Store_group,
                                            From_to_sellers,
                                            PXP,
                                            Store_official,
                                            Seller_oficial,
                                            Cash_price_status,
                                            Installment_price_status,
                                            Action,
                                            Status_ad,
                                            Brand,
                                            Ad,
                                            Officiality,
                                            Item_classification,
                                            Customer_classification,
                                            Channel) 
                                values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');'''.format(row['Store - Seller'],
                                                                                                                                                                                row['Week'],
                                                                                                                                                                                row['Date'],
                                                                                                                                                                                row['Part'],
                                                                                                                                                                                row['Seller'],
                                                                                                                                                                                row['Suggested Price'],
                                                                                                                                                                                row['Cash Price'],
                                                                                                                                                                                row['Installment Price'],
                                                                                                                                                                                row['Hiperlink'],
                                                                                                                                                                                row['Item'],
                                                                                                                                                                                row['Store Status'],
                                                                                                                                                                                row['Store Group'],
                                                                                                                                                                                row['From_To - Sellers'],
                                                                                                                                                                                row['1P X 3P'],
                                                                                                                                                                                row['Store Official?'],
                                                                                                                                                                                row['Seller Official?'],
                                                                                                                                                                                row['Cash Price Status'],
                                                                                                                                                                                row['Installment Price Status'],
                                                                                                                                                                                row['Action'],
                                                                                                                                                                                row['Status Ad'],
                                                                                                                                                                                row['Brand'],
                                                                                                                                                                                row['Ad'],
                                                                                                                                                                                row['Officiality'],
                                                                                                                                                                                row['Item Classification'],
                                                                                                                                                                                row['CUSTOMER CLASSIFICATION'],
                                                                                                                                                                                row['CHANNEL']))

    #Dando commit no databse 
    database.commit()

    c.close()

    database.close()

    #Criando o pop-up de notificação 
    popup = tk.Tk()
    popup.title("!!!!")
    popup.geometry("200x80")

    Popup_text = ttk.Label(popup, text='Os dados estão dentro do banco')
    Popup_text.pack()

    Popup_button = ttk.Button(popup, text='Ok', command=popup.destroy)
    Popup_button.pack()

    popup.mainloop()



#Criando a nova página
def Upload_Data():
    global Shape_data, Min_data, Max_data, Start_button
    
    page_upload = tk.Tk()
    page_upload.title("Input de Dados")
    page_upload.geometry('300x300')

    #Texto 
    Text_Brand = ttk.Label(page_upload, text="Escolha a Marca:")
    Text_Brand.grid(row=1, column=1, padx=3, pady=3,sticky="W")

    #Função para pegar brands
    Marcas = list(getting_brands())
    Value_inside = tkinter.StringVar(page_upload)
    Value_inside.set(Marcas[0])

    #Criando lista de marcas
    Choice_Brand = ttk.OptionMenu(page_upload, Value_inside, *Marcas)
    Choice_Brand.grid(row=1, column=2, padx=3, pady=3, sticky="W")

    #Mostrando as datas 
    Shape_data = ttk.Label(page_upload, text="Quantidade de linhas: XXX")
    Shape_data.grid(row=2, column=1)

    Min_data = ttk.Label(page_upload, text="Data mais antiga: 00/00/00")
    Min_data.grid(row=3, column=1)

    Max_data = ttk.Label(page_upload, text="Data mais recente: 00/00/00")
    Max_data.grid(row=4, column=1)

    #Criando botão para iniciar o processo 
    Start_button = ttk.Button(page_upload, text="Inspecionar Dados", command=lambda: Inspec(Value_inside.get()))
    Start_button.grid(row=5, column=1, padx=3, pady=3, sticky="W")



    #Loop principal
    page_upload.mainloop()