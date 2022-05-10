#Importando as bibliotecas padrão
import os
import time
import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter
from tkinter.constants import W
from typing import Text
import pandas as pd
import datetime


#Função Motorola
def Motorola_email():

    #Função para pegar os dados de Motorola
    def Get_Motorola_data():
        global size_df, cash_df, installment_df

        #Pegando os dados
        data = pd.read_excel(r"G:\.shortcut-targets-by-id\1VAK5JIWTmtamcYtBHQGeL7FVwcki0pRp\BRAND PROTECTION\Brand Protection - Daily Report.xlsb",engine='pyxlsb', header=1, convert_float=True)

        #Arrumando a coluna da data
        data['Date'] = pd.TimedeltaIndex(data['Date'], unit='d') + datetime.datetime(1899, 12, 30)

        #Limpando a primeira linha que é nula
        data = data[1:]

        #Filtrando os dados
        data_filtrada = data[data['Brand'] == "Motorola"]
        data_filtrada = data_filtrada[data_filtrada['Status Ad'] == 'Incorrect Ad']
        data_filtrada = data_filtrada[data_filtrada['Part'] == 'Morning']
        data_filtrada = data_filtrada[(data_filtrada['Action'] == 'Adjust Cash Price') | (data_filtrada['Action'] == 'Adjust Installment Price') ]
        data_filtrada = data_filtrada[['Date', 'Part', 'Store', 'Seller', '1P X 3P', 'Suggested Price', 'Difference', 'Porcentage', 'Cash Price','Installment Price', 'Hiperlink', 'Item', 'Action']]

        size_df = data_filtrada.shape[0]
        data_groupby = data_filtrada.groupby(['Action'])['Date'].count().reset_index()
        cash_df = data_groupby.loc[data_groupby['Action'] == "Adjust Cash Price"]['Date'][0]
        installment_df = data_groupby.loc[data_groupby['Action'] == 'Adjust Installment Price']['Date'][1]

    #Criando a nova página
    new_root = tk.Tk()
    new_root.geometry("300x300")
    new_root.title("Confirmação E-mail")

    #Criando o frame para os dados
    LabelFrame_Dados = ttk.LabelFrame(new_root, text="Dados")
    LabelFrame_Dados. grid(row=0, column=0, pady=10, padx=10, sticky="N")

    Get_Motorola_data()

    Shape_Text = ttk.Label(LabelFrame_Dados, text='O tamanho da planilha: ' + str(size_df))
    Shape_Text.grid(row=0, column=0, pady=5, padx=5, sticky="W")

    Cash_Text = ttk.Label(LabelFrame_Dados, text='Adjust Cash Price: ' + str(cash_df))
    Cash_Text.grid(row=1, column=0, pady=5, padx=5, sticky="W")

    Installment_Text = ttk.Label(LabelFrame_Dados, text='Adjust Installment Price: ' + str(installment_df))
    Installment_Text.grid(row=2, column=0, pady=5, padx=5, sticky="W")



    new_root.mainloop()
