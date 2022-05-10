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

#Função para o popup
def Estoque():

    def Estoque_search():
        estoque = []

        # --- DATABASE -----
        # Criando o database/fazendo a conexão
        dataset = pd.read_excel("G:/.shortcut-targets-by-id/18Jh1Gsq2qXY5AFF7QJQLuQhj88DlX8-R/Turtle BP/Sales Inventory ML.xlsx", sheet_name="ML")

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



    Estoque_page = tk.Tk()
    Estoque_page.title("!!!")
    Estoque_page.geometry("100x100")

    Label_Estoque = tk.Label(Estoque_page, text="O estoque está sendo feito")
    Label_Estoque.grid(row=0, column=0, pady=10, padx=10, sticky="N")

    Label_button = tk.Button(Estoque_page, text="Ok", command=Estoque_search)
    Label_button.grid(row=1, column=0, padx=10, pady=10, sticky="N")

    Label_Estoque.config(text="O estoque feito")

    Estoque_page.mainloop()