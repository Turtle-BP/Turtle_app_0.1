#Importando as bibliotecas padrão 
import os
import tkinter as tk
from tkinter import *
import sqlite3
import tkinter
from tkinter.constants import W
from typing import Text
import pandas as pd

#Funções 
#Função para pegar as marcas dentro do Database
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

def Start_Spiders(Amazon, Americanas, Carrefour, Extra, Kabum, Magazine, Mercado):
    print("Amazon:" + Amazon.get())
    print("Americanas:" + Americanas.get())
    print("Carrefour:" + Carrefour.get())
    print("Extra:" + Extra.get())
    print("Kabum:" + Kabum.get())
    print("Magazine:" + Magazine.get())
    print("Mercado L:" + Mercado.get())



#Criando a função da página 
def Spiders_Search_page():
    new_page = tk.Tk()
    new_page.title("Spiders")
    new_page.geometry("300x500")  

    # CRIAÇÃO PARA SELEÇÃO DE MARCAS #
    Text_Brand = tk.Label(new_page, text="Escolha a Marca")
    Text_Brand.grid(row=1, column=1, padx=10, pady=3, sticky="W")

    Marcas = list(getting_brands())
    Value_inside = tkinter.StringVar(new_page)
    Value_inside.set(Marcas[0])

    Choice_Brand = OptionMenu(new_page, Value_inside, *Marcas)
    Choice_Brand.grid(row=2, column=1, padx=3, pady=3, sticky="W")

    # CRIAÇÃO PARA SELEÇÃO DE MARKETPLACES # 
    #Texto explicativo 
    Text_Marketplaces = tk.Label(new_page, text="Escolha os Marketplaces", anchor='e', width=20)
    Text_Marketplaces.grid(row=1, column=6)

    #Criando os botões para a seleção 
    AmazonVar = StringVar(new_page, value="Desligado")
    Amazon_button = Checkbutton(new_page, text='Amazon',variable=AmazonVar, onvalue='Ligado', offvalue="Desligado", width=20, anchor="w")
    Amazon_button.grid(row=2, column=6)

    AmericanasVar = StringVar(new_page, value="Desligado")
    Americanas_button = Checkbutton(new_page, text='Americanas',variable=AmericanasVar, onvalue='Ligado', offvalue="Desligado", width=20, anchor="w")
    Americanas_button.grid(row=3, column=6)

    CarrefourVar = StringVar(new_page, value="Desligado")
    Carrefour_button = Checkbutton(new_page, text='Carrefour',variable=CarrefourVar, onvalue='Ligado', offvalue="Desligado", width=20, anchor="w")
    Carrefour_button.grid(row=4, column=6)

    ExtraVar = StringVar(new_page, value="Desligado")
    Extra_button = Checkbutton(new_page, text='Extra', variable=ExtraVar, onvalue='Ligado', offvalue="Desligado", width=20, anchor="w")
    Extra_button.grid(row=5, column=6)

    KabumVar = StringVar(new_page, value="Desligado")
    Kabum_button = Checkbutton(new_page, text='Kabum',variable=KabumVar, onvalue='Ligado', offvalue="Desligado", width=20, anchor="w")
    Kabum_button.grid(row=6, column=6)

    MagazineVar = StringVar(new_page, value="Desligado")
    Magazine_button = Checkbutton(new_page, text='Magazine',variable=MagazineVar, onvalue='Ligado', offvalue="Desligado", width=20, anchor="w")
    Magazine_button.grid(row=7, column=6)

    MercadoVar = StringVar(new_page, value="Desligado")
    Mercado_button = Checkbutton(new_page, text='Mercado L',variable=MercadoVar, onvalue='Ligado', offvalue="Desligado", width=20, anchor="w")
    Mercado_button.grid(row=8, column=6)

    #Botão para realizar a pesquisa
    Search_Button = Button(new_page, text='Fazer Pesquisa', command=lambda: Start_Spiders(AmazonVar, AmericanasVar, CarrefourVar, ExtraVar, KabumVar, MagazineVar, MercadoVar))
    Search_Button.grid(row=9, column=1, padx=20, pady=20, sticky="W")

    new_page.mainloop()