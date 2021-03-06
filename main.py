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
import winsound

#Função para deletar os warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#Importando função de outras páginas
from Pages.Upload_Data import Upload_Data
from Pages.Add_other_brand import add_brands
from Pages.Add_itens import add_itens
from Pages.Motorola_Email import Motorola_email
from Pages.Estoque import Estoque

#Importando função de Spiders
from Spiders.Magazine import magalu_final
from Spiders.Carrefour import carrefour_final
from Spiders.Via_Varejo import ViaVarejo_final
from Spiders.Kabum import Kabum_final
from Spiders.Mercado_Livre import Mercado_livre_final
from Spiders.Amazon import amazon_final
from Spiders.B2W import americanas_final

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

def Start_Amazon(Amazon, brand):
    if Amazon.get() == "Ligado":
        Text_Status_Amazon.config(foreground="orange", text="Buscando")

        Text_Status_Amazon.update_idletasks()

        time.sleep(5)

        amazon_final(brand)

        # Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Amazon.config(foreground="green", text="Finalizado")
    else:
        Text_Status_Amazon.config(foreground="red", text="Desativado")

def Start_Americanas(Americanas, brand):
    if Americanas.get() == "Ligado":
        Text_Status_Americanas.config(foreground="orange", text="Buscando")

        Text_Status_Americanas.update_idletasks()

        time.sleep(5)

        americanas_final(brand)

        #Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Americanas.config(foreground="green", text="Finalizado")
    else:
        Text_Status_Americanas.config(foreground="red", text="Desativado")

def Start_Carrefour(Carrefour, brand):
    if Carrefour.get() == "Ligado":
        Text_Status_Carrefour.config(foreground="orange", text="Buscando")

        Text_Status_Carrefour.update_idletasks()

        time.sleep(5)

        carrefour_final(brand)

        # Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Carrefour.config(foreground="green", text="Finalizado")
    else:
        Text_Status_Carrefour.config(foreground="red", text="Desativado")

def Start_Extra(Extra, brand):
    if Extra.get() == "Ligado":

        Text_Status_Extra.config(foreground="orange", text="Buscando")

        Text_Status_Extra.update_idletasks()

        time.sleep(5)

        ViaVarejo_final(brand)

        #Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Extra.config(foreground="green", text="Finalizado")
    else:
        Text_Status_Extra.config(foreground="red", text="Desativado")

def Start_Kabum(Kabum, brand):
    if Kabum.get() == "Ligado":

        Text_Status_Kabum.config(foreground="orange", text="Buscando")

        Text_Status_Kabum.update_idletasks()

        time.sleep(5)

        Kabum_final(brand)

        #Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Kabum.config(foreground="green", text="Finalizado")
    else:
        Text_Status_Kabum.config(foreground="red", text="Desativado")

def Start_Magazine(Magazine, brand):
    if Magazine.get() == "Ligado":

        Text_Status_Magazine.config(foreground="orange", text="Buscando")

        Text_Status_Magazine.update_idletasks()

        time.sleep(5)

        magalu_final(brand)

        #Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Magazine.config(foreground="green", text="Finalizado")
    else:
        Text_Status_Magazine.config(foreground="red", text="Desativado")

def Start_Mercado(Mercado, brand):
    if Mercado.get() == "Ligado":

        Text_Status_Mercado.config(foreground="orange", text="Buscando")

        Text_Status_Mercado.update_idletasks()

        time.sleep(5)

        Mercado_livre_final(brand)

        #Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Mercado.config(foreground="green", text="Finalizado")
    else:
        Text_Status_Mercado.config(foreground="red", text="Desativado")

def Start_Spiders(Amazon, Americanas, Carrefour, Extra, Kabum, Magazine, Mercado, brand_name):
    Start_Magazine(Magazine, brand_name)
    Start_Extra(Extra, brand_name)
    Start_Carrefour(Carrefour, brand_name)
    Start_Kabum(Kabum, brand_name)
    Start_Mercado(Mercado, brand_name)
    Start_Amazon(Amazon, brand_name)
    Start_Americanas(Americanas, brand_name)



#Criando a página principal
root = tk.Tk()
root.geometry("600x350")
root.title("Turtle Brand Protection - V1.0")

#Criando os botões para abrir outras páginas do aplicativo

# -------------------------------------- FUNÇÕES PRINCIPAIS ----------------------------------------------------- #
#Criando o LabelFrame para armazenar as funçoes
Label_frame_spiders = ttk.LabelFrame(root, text="Funções")
Label_frame_spiders.grid(row=0,column=0,padx=10, pady=10, sticky="W")

#Adicionar Marca nova 
botao_New_Brands = ttk.Button(Label_frame_spiders, text='Adicionar marca', command=add_brands)
botao_New_Brands.grid(row=1, column=1, padx=10, pady=10, sticky="W")

#Adicionar Itens novos a Marcas antigas
botao_New_Itens = ttk.Button(Label_frame_spiders, text='Adicionar Itens', command=add_itens)
botao_New_Itens.grid(row=1, column=2, padx=10, pady=10, sticky="W")

#Subir dados para o database
botao_Add_Data = ttk.Button(Label_frame_spiders, text='Subir dados', command=Upload_Data)
botao_Add_Data.grid(row=1, column=3, padx=10, pady=10, sticky="W")

#Pegar o estoque / Verificação
botao_Estoque = ttk.Button(Label_frame_spiders, text='Estoque', command=Estoque)
botao_Estoque.grid(row=3, column=2, padx=10, pady=10, sticky="W")

#Spiders para busca de itens da marca
botao_Spiders = ttk.Button(Label_frame_spiders, text='Busca urls')
botao_Spiders.grid(row=3, column=3, padx=10, pady=10, sticky="W")

#Envio de E-mail para Motorola
botao_email = ttk.Button(Label_frame_spiders, text='Motorola', command=Motorola_email)
botao_email.grid(row=3, column=1, padx=10, pady=10, sticky="W")

# ------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------- CONEXÃO COM OS BANCOS DE DADOS --------------------------------- #

# -------------------------------------------------- SPIDERS -------------------------------------------------------- #

#Criação de quadro para as atividades dos Spiders/Buscadores
Spiders_Frame = ttk.LabelFrame(root, text="Spiders")
Spiders_Frame.grid(row=7,column=0,padx=10, pady=10, sticky="W")

Marcas = list(getting_brands())
Value_inside = tkinter.StringVar(root)
Value_inside.set(Marcas[0])

Choice_Brand = ttk.OptionMenu(Spiders_Frame, Value_inside, *Marcas)
Choice_Brand.grid(row=8, column=1, padx=3, pady=3, sticky="W")

#Adicionando os nomes dos Spiders no Frame
AmazonVar = tk.StringVar(Spiders_Frame, value="Desligado")
Amazon_button = tk.Checkbutton(Spiders_Frame, text='Amazon', variable=AmazonVar, onvalue='Ligado', offvalue="Desligado", anchor="w")
Amazon_button.grid(row=8, column=2, padx=30, pady=0,ipady=0,sticky="W")
#Fazendo função
Text_Status_Amazon = ttk.Label(Spiders_Frame, text="Desativado")
Text_Status_Amazon.config(foreground='red')
Text_Status_Amazon.grid(row=9, column=2,  padx=0, pady=0)

#Adicionando os nomes dos Spiders no Frame
AmericanasVar = tk.StringVar(Spiders_Frame, value="Desligado")
Americanas_button = tk.Checkbutton(Spiders_Frame, text='Americanas', variable=AmericanasVar, onvalue='Ligado', offvalue="Desligado", anchor="w")
Americanas_button.grid(row=8, column=3, padx=30, pady=0,ipady=0,sticky="W")
Text_Status_Americanas = ttk.Label(Spiders_Frame, text="Desativado")
Text_Status_Americanas.config(foreground='red')
Text_Status_Americanas.grid(row=9, column=3,  padx=0, pady=0)

#Adicionando os nomes dos Spiders no Frame
CarrefourVar = tk.StringVar(Spiders_Frame, value="Desligado")
Carrefour_button = tk.Checkbutton(Spiders_Frame, text='Carrefour', variable=CarrefourVar, onvalue='Ligado', offvalue="Desligado", anchor="w")
Carrefour_button.grid(row=8, column=4, padx=30, pady=0,ipady=0,sticky="W")
Text_Status_Carrefour = ttk.Label(Spiders_Frame, text="Desativado")
Text_Status_Carrefour.config(foreground='red')
Text_Status_Carrefour.grid(row=9, column=4,  padx=0, pady=0)

#Adicionando os nomes dos Spiders no Frame
ExtraVar = tk.StringVar(Spiders_Frame, value="Desligado")
Extra_button = tk.Checkbutton(Spiders_Frame, text='Extra', variable=ExtraVar, onvalue='Ligado', offvalue="Desligado", anchor="w")
Extra_button.grid(row=11, column=1, padx=30, pady=0,ipady=0,sticky="W")
Text_Status_Extra = ttk.Label(Spiders_Frame, text="Desativado")
Text_Status_Extra.config(foreground='red')
Text_Status_Extra.grid(row=12, column=1,  padx=0, pady=0)

#Adicionando os nomes dos Spiders no Frame
KabumVar = tk.StringVar(Spiders_Frame, value="Desligado")
Kabum_button = tk.Checkbutton(Spiders_Frame, text='Kabum', variable=KabumVar, onvalue='Ligado', offvalue="Desligado", anchor="w")
Kabum_button.grid(row=11, column=2, padx=30, pady=0,ipady=0,sticky="W")
Text_Status_Kabum = ttk.Label(Spiders_Frame, text="Desativado")
Text_Status_Kabum.config(foreground='red')
Text_Status_Kabum.grid(row=12, column=2,  padx=0, pady=0)

#Adicionando os nomes dos Spiders no Frame
MagazineVar = tk.StringVar(Spiders_Frame, value="Desligado")
Magazine_button = tk.Checkbutton(Spiders_Frame, text='Magazine', variable=MagazineVar, onvalue='Ligado', offvalue="Desligado", anchor="w")
Magazine_button.grid(row=11, column=3, padx=30, pady=0,ipady=0,sticky="W")
Text_Status_Magazine = ttk.Label(Spiders_Frame, text="Desativado")
Text_Status_Magazine.config(foreground='red')
Text_Status_Magazine.grid(row=12, column=3,  padx=0, pady=0)

#Adicionando os nomes dos Spiders no Frame
MercadoVar = tk.StringVar(Spiders_Frame, value="Desligado")
Mercado_button = tk.Checkbutton(Spiders_Frame, text='Mercado L', variable=MercadoVar, onvalue='Ligado', offvalue="Desligado", anchor="w")
Mercado_button.grid(row=11, column=4, padx=30, pady=0,ipady=0,sticky="W")
Text_Status_Mercado = ttk.Label(Spiders_Frame, text="Desativado")
Text_Status_Mercado.config(foreground='red')
Text_Status_Mercado.grid(row=12, column=4,  padx=0, pady=0)

#Criando o botão para dar Start nos Spiders
StartSpiders_Button = ttk.Button(Spiders_Frame, text="Inicar Busca", command=lambda: Start_Spiders(AmazonVar, AmericanasVar, CarrefourVar, ExtraVar, KabumVar, MagazineVar, MercadoVar, Value_inside.get()))
StartSpiders_Button.grid(row=15, column=1, padx=20, pady=20, sticky="W")

# ------------------------------------------------------------------------------------------------------------------- #


root.mainloop()