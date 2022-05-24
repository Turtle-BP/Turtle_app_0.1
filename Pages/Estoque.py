#importando as bibliotecas
import pandas as pd
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
from tqdm import tqdm
import tkinter as tk
from tkinter import ttk

#Função para o popup
def Estoque():
    from tkinter import filedialog

    def Get_Dataset():
        # Criando o database/fazendo a conexão
        dataset = pd.read_excel("G:/.shortcut-targets-by-id/18Jh1Gsq2qXY5AFF7QJQLuQhj88DlX8-R/Turtle BP/Sales Inventory ML.xlsx", sheet_name="ML")

        return dataset

    def Get_New_itens():
        file = filedialog.askopenfilename()

        #Criando página para subir ou cancelar os novos dados
        Popup_page = tk.Tk()
        Popup_page.geometry("230x140")
        Popup_page.title("!!!!")

        #Criando lista para vizualização dos itens na página
        Itens_List = tk.Listbox(Popup_page, height=6)
        Itens_List.grid(row=0, column=0, pady=10, padx=10, sticky="NW", rowspan=2)

        data = pd.read_excel(file)

        x = 1
        for url in data['Urls']:
            Itens_List.insert(x, url)
            x = x + 1


        #Criando o botão para adicionar
        Upload_Button = ttk.Button(Popup_page, text="Subir Urls")
        Upload_Button.grid(row=0, column=1)

        #Criando botão para cancelar
        Cancel_Button = ttk.Button(Popup_page, text="Cancelar", command=Popup_page.destroy)
        Cancel_Button.grid(row=1, column=1, sticky="N")

    def Estoque_search():
        #Abrindo a janela PopUp para notificação
        Popup_Estoque = tk.Tk()
        Popup_Estoque.geometry("300x100")
        Popup_Estoque.title("!!!!")

        #Colocando o texto
        Label = ttk.Label(Popup_Estoque, text="O estoque foi iniciado\nEstá página irá ser fechada assim que o estoque for enviado por e-mail")
        Label.pack()

        estoque = []

        dataset = Get_Dataset()

        # --- DATABASE -----
        # Criando o database/fazendo a conexão
        for url in tqdm(dataset['Hiperlink']):
            time.sleep(1.5)
            try:
                response = urlopen(url)
            except:
                pass

            html = response.read()

            bs = BeautifulSoup(html, 'html.parser')

            try:
                ultimo = bs.find(class_='ui-pdp-color--BLACK ui-pdp-size--MEDIUM ui-pdp-family--SEMIBOLD').text
                estoque.append("1")
            except:
                try:
                    quant = bs.find(class_='ui-pdp-buybox__quantity__available').text
                    estoque.append(quant)
                except:
                    estoque.append("-")

        dataset_estoque = pd.DataFrame()

        dataset_estoque['Estoque'] = estoque

        # Arrumando os valores de estoque
        dataset_estoque['Estoque'] = dataset_estoque['Estoque'].str.replace("(", "")
        dataset_estoque["Estoque"] = dataset_estoque["Estoque"].str.replace(" disponíveis", "")
        dataset_estoque["Estoque"] = dataset_estoque["Estoque"].str.replace(")", "")

        dataset_estoque.to_excel(r"C:\Users\pedro\Documents\Turte Brand Protection\Turtle_Thinker_Alpha_0.1\estoque_ml.xlsx",index=False)

        email_path = "C:/Users/pedro/Documents/Turte Brand Protection/Turtle_Thinker_Alpha_0.1/estoque_ml.xlsx"

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        server.login('brandprotection.03@turtlebp.com', 'Five@316712')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Estoque Mercado Livre de Hoje'
        msg['From'] = 'brandprotection01@fivec.com.br'
        msg['body'] = 'Linha 1 \n Linha 2 \n Linha 3'
        recipients = ['kcavalcante@turtlebp.com', 'hfernandes@turtlebp.com']
        msg['To'] = ", ".join(recipients)

        part1 = MIMEBase('application', 'octet-stream')
        part1.set_payload(open(email_path, 'rb').read())
        encoders.encode_base64(part1)
        part1.add_header('Content-Disposition', 'attachment;filename="Motorola_monitoramento.xlsx"')

        msg.attach(part1)
        server.sendmail('brandprotection01@fivec.com.br', recipients, msg.as_string())

        Popup_Estoque.mainloop()

        Popup_Estoque.destroy()



    #Criando página
    Estoque_page = tk.Tk()
    Estoque_page.title("Estoque")
    Estoque_page.geometry("180x180")

    #Criando a Label
    Shape_var = "O Estoque está com: " + str(Get_Dataset().shape[0])

    #Colocando a Label
    Shape_Text = ttk.Label(Estoque_page, text=Shape_var)
    Shape_Text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    #Colocando o botão para iniciar
    Search_Button = ttk.Button(Estoque_page, text="Iniciar Busca", command=Estoque_search)
    Search_Button.grid(row=1, column=0, pady=5, padx=5, sticky="W")

    #Colocando botão para inserir mais urls
    Add_Button = ttk.Button(Estoque_page, text="Adicionar", command=lambda: Get_New_itens())
    Add_Button.grid(row=1, column=1, padx=5, pady=5)

    #Criando a lista onde vai ter os logs
    Log_list = tk.Listbox(Estoque_page, width=25, height=5)
    Log_list.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky="W")




    Estoque_page.mainloop()
