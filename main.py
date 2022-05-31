#IMPORTANDO AS BIBLIOTECAS
import os
import time
import tkinter as tk
from tkinter import ttk
import tkinter
import sqlite3 as sql


import winsound
from PIL import ImageTk, Image

#Importando warnings para ignorar Future Warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#Importando função de outras páginas
from Pages.Upload_Data import Upload_Data
#from Pages.Add_other_brand import add_brands
#from Pages.Add_itens import add_itens
#from Pages.Motorola_Email import Motorola_email
from Pages.Estoque import Estoque

#Importando função de Spiders



def Start_Amazon(Amazon, brand):
    #Importando a função de Amazon
    from Spiders.Amazon import amazon_final

    if Amazon.get() == "Ligado":
        Text_Status_Amazon.config(foreground="orange", text="Buscando")

        Text_Status_Amazon.update_idletasks()

        time.sleep(5)

        amazon_final(brand)

        # Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Amazon.config(foreground="green", text="Finalizado")

        Text_Status_Amazon.update_idletasks()
    else:
        Text_Status_Amazon.config(foreground="red", text="Desativado")

def Start_Americanas(Americanas, brand):
    #Importando a função
    from Spiders.B2W import americanas_final

    if Americanas.get() == "Ligado":
        Text_Status_Americanas.config(foreground="orange", text="Buscando")
        Text_Status_Americanas.update_idletasks()

        time.sleep(5)

        americanas_final(brand)

        #Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Americanas.config(foreground="green", text="Finalizado")
        Text_Status_Americanas.update_idletasks()
    else:
        Text_Status_Americanas.config(foreground="red", text="Desativado")

def Start_Carrefour(Carrefour, brand):
    #Importando a função
    from Spiders.Carrefour import carrefour_final

    if Carrefour.get() == "Ligado":
        Text_Status_Carrefour.config(foreground="orange", text="Buscando")
        Text_Status_Carrefour.update_idletasks()

        time.sleep(5)

        carrefour_final(brand)

        # Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Carrefour.config(foreground="green", text="Finalizado")
        Text_Status_Carrefour.update_idletasks()
    else:
        Text_Status_Carrefour.config(foreground="red", text="Desativado")

def Start_Extra(Extra, brand):
    #Importando a funçaõ
    from Spiders.Via_Varejo import ViaVarejo_final

    if Extra.get() == "Ligado":

        Text_Status_Extra.config(foreground="orange", text="Buscando")
        Text_Status_Extra.update_idletasks()

        time.sleep(5)

        ViaVarejo_final(brand)

        #Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Extra.config(foreground="green", text="Finalizado")
        Text_Status_Extra.update_idletasks()
    else:
        Text_Status_Extra.config(foreground="red", text="Desativado")

def Start_Kabum(Kabum, brand):
    #Importando a função
    from Spiders.Kabum import Kabum_final

    if Kabum.get() == "Ligado":

        Text_Status_Kabum.config(foreground="orange", text="Buscando")
        Text_Status_Kabum.update_idletasks()

        time.sleep(5)

        Kabum_final(brand)

        #Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Kabum.config(foreground="green", text="Finalizado")
        Text_Status_Kabum.update_idletasks()
    else:
        Text_Status_Kabum.config(foreground="red", text="Desativado")

def Start_Magazine(Magazine, brand):
    #Importando a função
    from Spiders.Magazine import magalu_final

    if Magazine.get() == "Ligado":

        Text_Status_Magazine.config(foreground="orange", text="Buscando")
        Text_Status_Magazine.update_idletasks()

        time.sleep(5)

        magalu_final(brand)

        #Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Magazine.config(foreground="green", text="Finalizado")
        Text_Status_Magazine.update_idletasks()
    else:
        Text_Status_Magazine.config(foreground="red", text="Desativado")

def Start_Mercado(Mercado, brand):
    #Importando a função
    from Spiders.Mercado_Livre import Mercado_livre_final

    if Mercado.get() == "Ligado":

        Text_Status_Mercado.config(foreground="orange", text="Buscando")
        Text_Status_Mercado.update_idletasks()

        time.sleep(5)

        Mercado_livre_final(brand)

        #Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Mercado.config(foreground="green", text="Finalizado")
        Text_Status_Mercado.update_idletasks()
    else:
        Text_Status_Mercado.config(foreground="red", text="Desativado")

def Start_Shopee(Shopee, brand):
    # Importando a função

    if Shopee.get() == "Ligado":

        Text_Status_Shopee.config(foreground="orange", text="Buscando")
        Text_Status_Shopee.update_idletasks()

        time.sleep(5)

        # Testando o som de finalizado
        winsound.PlaySound("*", winsound.SND_ALIAS)

        Text_Status_Shopee.config(foreground="green", text="Finalizado")
        Text_Status_Shopee.update_idletasks()
    else:
        Text_Status_Shopee.config(foreground="red", text="Desativado")

def Start_Spiders(Amazon, Americanas, Carrefour, Extra, Kabum, Magazine, Mercado, Shopee, brand_name):
    Start_Magazine(Magazine, brand_name)
    Start_Extra(Extra, brand_name)
    Start_Carrefour(Carrefour, brand_name)
    Start_Kabum(Kabum, brand_name)
    Start_Mercado(Mercado, brand_name)
    Start_Amazon(Amazon, brand_name)
    Start_Americanas(Americanas, brand_name)
    Start_Shopee(Shopee, brand_name)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #


#Criando a verificação de Login do Usuário
def User_verification(username, password,root):
    #Pegando o caminho para o banco de dados
    Current_dir = os.getcwd()

    Database_path = Current_dir + "\Data\\Users.db"

    #Criando a conexão com o banco de dados
    Database = sql.connect(Database_path)

    #Criando o cursor
    C = Database.cursor()

    #Fazendo a query do nome de usuário
    Query_User = "SELECT ID FROM Users WHERE Name = " + username

    #Fazendo a query da senha do usuário
    Query_Login = "SELECT ID FROM Users WHERE Name = (?) AND Password = (?)"

    #Execute Login
    result = C.execute(Query_Login,(username,password))

    #Fazendo as condicionais
    #Se tudo estiver correto
    if result.fetchone():
        #print("Usuário -- Correto\nSenha -- Correto")

        #Destroindo a página de Login
        root.destroy()

        #Iniciando a página inicial
        Principal_Page()

    #Se algo estiver incorreto
    else:
        #print("Usuário -- Errado\nSenha -- Errado")
        pass

#Criando a página de Login
def Login_Page():
    #Criando a página
    Login_root = tk.Tk()
    Login_root.title("Turtle App - V2.0")
    Login_root.geometry('320x250')

    #Carregando a imagem
    load_img = Image.open('Img/horizontal_mono_preto.png').resize((250,80))

    #Renderizando a imagem
    Img = ImageTk.PhotoImage(load_img)

    #Colocando o imagem dentro do frame
    Img_Label = tk.Label(Login_root, image=Img, width=250, height=80)
    Img_Label.grid(row=1, column=0, sticky="N", columnspan=2, padx=30, pady=30)

    #Colocando Texto de usuário
    User_Text = tk.Label(Login_root, text="Nome de usuário:")
    User_Text.grid(row=2, column=0,padx=5, pady=5)

    #Colocando caixa de texto para entrada do nome de usuário
    User_name = tk.Entry(Login_root)
    User_name.grid(row=2, column=1,padx=5, pady=5)

    #Colocando Texto de senha
    Password_Text = tk.Label(Login_root, text="Senha:")
    Password_Text.grid(row=3, column=0,padx=5, pady=5)

    #Colocando caixa de texto para entrada do nome de usuário
    Password = tk.Entry(Login_root)
    Password.grid(row=3, column=1,padx=5, pady=5)

    #Colocando botão de Login
    Button_Login = tk.Button(Login_root, text='Login', width=15, command=lambda: User_verification(User_name.get(), Password.get(), Login_root))
    Button_Login.grid(row=4, column=0, pady=8, padx=8)

    #Colocando de esqueceu a senha
    Button_Forget = tk.Button(Login_root, text='Esqueceu a senha', width=15)
    Button_Forget.grid(row=4, column=1, pady=8, padx=8)


    Login_root.mainloop()

#Criando a função para buscar a atualização do git automática
def Automatic_update(root):
    #Importando a função de Destroy
    from Func.Destroy_Pages import destroy_multiple_pages

    #Criando a janela em PopUp
    PopUp_Git = tk.Tk()
    PopUp_Git.geometry("280x100")

    #Pegando diretório principal
    current = os.getcwd()

    #Importando a biblioteca
    import git

    #Pegando o repositório
    repo = git.Repo(current)

    Text = ttk.Label(PopUp_Git, text="O aplicativo será atualizado\nApós clicar no botão o aplicativo deve reiniciado")
    Text.pack(pady=10, padx=10)

    repo.remotes.origin.pull("Version_2.0")

    #Colocando o botão
    Button = ttk.Button(PopUp_Git, text="OK", command=lambda: destroy_multiple_pages(PopUp_Git,root))
    Button.pack(pady=10, padx=10)


#Criando a página principal
def Principal_Page():
    global Text_Status_Amazon,Text_Status_Americanas,Text_Status_Carrefour,Text_Status_Extra,Text_Status_Kabum,Text_Status_Magazine,Text_Status_Mercado,Text_Status_Shopee

    #Importando função de pegar marcas
    from Func.Menu_Brands import getting_brands

    #Criando a página principal
    root = tk.Tk()
    root.geometry("610x380")
    root.title("Turtle Brand Protection - V2.0")

    #Colocando a imagem como ícone no canto superior esquerdo
    #Carregando a imagem
    load_img = Image.open('Img/Logo_pequeno.png').resize((55,70))

    #Renderizando a imagem
    Img = ImageTk.PhotoImage(load_img)

    #Colocando o imagem dentro do frame
    Img_Label = tk.Label(root, image=Img, width=55, height=70)
    Img_Label.place(x=40, y=10)

    # -------------------------------------- FUNÇOES --------------------------------------------------- #
    # #Criando o label frame para a área de funções
    Frame_Func = ttk.LabelFrame(root, text="Funções")
    Frame_Func.place(x=10, y=100)
    #
    #
    # #Criando o Label para criação de novas marcas no banco
    Add_New_Brands_Button = ttk.Button(Frame_Func, text='Adicionar marca', width=15)
    Add_New_Brands_Button.grid(row=0,column=0, padx=8, pady=8, sticky="W")
    #
    # #Criando Label para adicionar novos itens a marcas já registradas
    Add_New_Itens_Button = ttk.Button(Frame_Func, text='Adicionar itens', width=15)
    Add_New_Itens_Button.grid(row=1,column=0, padx=8, pady=8, sticky="W")
    #
    # #Criando Label para subir dados para históricos
    Upload_Button = ttk.Button(Frame_Func, text='Subir dados', width=15, command=Upload_Data)
    Upload_Button.grid(row=2,column=0, padx=8, pady=8, sticky="W")
    #
    # #Estoque
    Estoque_Button = ttk.Button(Frame_Func, text='Estoque', width=15, command=Estoque)
    Estoque_Button.grid(row=3,column=0, padx=8, pady=8, sticky="W")
    #
    # #Busca Urls
    Search_urls_Button = ttk.Button(Frame_Func, text='Busca urls', width=15)
    Search_urls_Button.grid(row=4,column=0, padx=8, pady=8, sticky="W")
    #
    # #E-mail Motorola
    Motorola_Button = ttk.Button(Frame_Func, text='E-mail Motorola', width=15)
    Motorola_Button.grid(row=5,column=0, padx=8, pady=8, sticky="W")
    #
    # # -------------------------------------------------------------------------------------------- #
    #
    # # ------------------------------------------ SPIDERS ---------------------------------------------------------#
    # #Criando o LabelFrame para os Spiders dos Marketplaces
    Spiders_Frame = ttk.LabelFrame(root, text="Spiders")
    Spiders_Frame.place(x=150,y=10)
    #
    # #Utilizando função para pegar as marcas
    #Pegando as marcas
    Marcas = list(getting_brands())
    Value_inside = tkinter.StringVar(root)
    #Value_inside.set(Marcas[0])
    Menu = ttk.OptionMenu(Spiders_Frame, Value_inside, *Marcas)
    Menu.grid(row=0, column=0, padx=5, pady=5)
    #
    # #Criando os botões para inicialização das marcas
    #
    # #Amazon
    # #Criando a variável de butão para Amazon
    AmazonVar = tk.StringVar(Spiders_Frame, value='Desligado')
    # #Criando botão da Amazon
    Amazon_Button = ttk.Checkbutton(Spiders_Frame, text="Amazon", variable=AmazonVar, onvalue='Ligado', offvalue='Desligado')
    Amazon_Button.grid(row=0, column=1, padx=20)
    # #Criando o texto de Status para display
    Text_Status_Amazon = ttk.Label(Spiders_Frame, text="Desativado")
    Text_Status_Amazon.config(foreground='red')
    Text_Status_Amazon.grid(row=1, column=1)
    #
    # #Americanas
    # #Criando a variável de butão para Amazon
    AmericanasVar = tk.StringVar(Spiders_Frame, value='Desligado')
    # #Criando botão da Americanas
    Americanas_Button = ttk.Checkbutton(Spiders_Frame, text="Americanas", variable=AmericanasVar, onvalue='Ligado', offvalue='Desligado')
    Americanas_Button.grid(row=0, column=2, pady=10, padx=20)
    # #Criando o texto de Status para display
    Text_Status_Americanas = ttk.Label(Spiders_Frame, text="Desativado")
    Text_Status_Americanas.config(foreground='red')
    Text_Status_Americanas.grid(row=1, column=2)
    #
    # #Carrefour
    # #Criando a variável de butão para Amazon
    CarrefourVar = tk.StringVar(Spiders_Frame, value='Desligado')
    # #Criando botão da Americanas
    Carrefour_Button = ttk.Checkbutton(Spiders_Frame, text="Carrefour", variable=CarrefourVar, onvalue='Ligado', offvalue='Desligado')
    Carrefour_Button.grid(row=0, column=3, pady=10, padx=20)
    # #Criando o texto de Status para display
    Text_Status_Carrefour = ttk.Label(Spiders_Frame, text="Desativado")
    Text_Status_Carrefour.config(foreground='red')
    Text_Status_Carrefour.grid(row=1, column=3)
    #
    # #Extra
    # #Criando a variável de butão para Amazon
    ExtraVar = tk.StringVar(Spiders_Frame, value='Desligado')
    # #Criando botão da Americanas
    Extra_Button = ttk.Checkbutton(Spiders_Frame, text="Extra", variable=ExtraVar, onvalue='Ligado', offvalue='Desligado')
    Extra_Button.grid(row=2, column=1, pady=10, padx=20, sticky="W")
    # #Criando o texto de Status para display
    Text_Status_Extra = ttk.Label(Spiders_Frame, text="Desativado")
    Text_Status_Extra.config(foreground='red')
    Text_Status_Extra.grid(row=3, column=1)
    #
    # #Kabum
    # #Criando a variável de butão para Amazon
    KabumVar = tk.StringVar(Spiders_Frame, value='Desligado')
    # #Criando botão da Americanas
    Kabum_Button = ttk.Checkbutton(Spiders_Frame, text="Kabum", variable=KabumVar, onvalue='Ligado', offvalue='Desligado')
    Kabum_Button.grid(row=2, column=2, pady=10, padx=20, sticky="W")
    # #Criando o texto de Status para display
    Text_Status_Kabum = ttk.Label(Spiders_Frame, text="Desativado")
    Text_Status_Kabum.config(foreground='red')
    Text_Status_Kabum.grid(row=3, column=2)
    #
    # #Magazine Luiza
    # #Criando a variável de butão para Amazon
    MagazineVar = tk.StringVar(Spiders_Frame, value='Desligado')
    # #Criando botão da Americanas
    Magazine_Button = ttk.Checkbutton(Spiders_Frame, text="Magazine", variable=MagazineVar, onvalue='Ligado', offvalue='Desligado')
    Magazine_Button.grid(row=2, column=3, pady=10, padx=20, sticky="W")
    # #Criando o texto de Status para display
    Text_Status_Magazine = ttk.Label(Spiders_Frame, text="Desativado")
    Text_Status_Magazine.config(foreground='red')
    Text_Status_Magazine.grid(row=3, column=3)
    #
    # #Criando a variável de butão para Amazon
    MercadoVar = tk.StringVar(Spiders_Frame, value='Desligado')
    # #Criando botão da Americanas
    Mercado_Button = ttk.Checkbutton(Spiders_Frame, text="Mercado L", variable=MercadoVar, onvalue='Ligado', offvalue='Desligado')
    Mercado_Button.grid(row=5, column=1, pady=10, padx=20, sticky="W")
    # #Criando o texto de Status para display
    Text_Status_Mercado = ttk.Label(Spiders_Frame, text="Desativado")
    Text_Status_Mercado.config(foreground='red')
    Text_Status_Mercado.grid(row=6, column=1)
    # #Shopee
    # # Criando a variável de butão para Amazon
    ShopeeVar = tk.StringVar(Spiders_Frame, value='Desligado')
    # #Criando botão da Americanas
    Shopee_Button = ttk.Checkbutton(Spiders_Frame, text="Shopee", variable=ShopeeVar, onvalue='Ligado', offvalue='Desligado')
    Shopee_Button.grid(row=5, column=2, pady=10, padx=20, sticky="W")
    # #Criando o texto de Status para display
    Text_Status_Shopee = ttk.Label(Spiders_Frame, text="Desativado")
    Text_Status_Shopee.config(foreground='red')
    Text_Status_Shopee.grid(row=6, column=2)
    #
    # #Colocando o botão para inicialização dos Spiders selecionados
    Active_Button = ttk.Button(Spiders_Frame, text="Iniciar Spiders", command=lambda: Start_Spiders(AmazonVar, AmericanasVar, CarrefourVar, ExtraVar, KabumVar, MagazineVar, MercadoVar, ShopeeVar,Value_inside.get()))
    Active_Button.grid(row=1, column=0, padx=5, sticky="N", rowspan=3)
    #
    # # -------------------------------------------------------------------------------------------- #
    #
    # # --------------------------------------------- VERSION APP ------------------------------------------ #
    # #Criando o LabelFrame para mostar a versão do Aplicativo
    Version_Frame = ttk.LabelFrame(root, text="App")
    Version_Frame.place(x=150,y=220)

    #Criando o print da versão do App
    Version  = '2.0.4'
    Version_text = "Versão do Aplicativo: " + Version

    #Printando a versão do aplicativo
    Print_Version = ttk.Label(Version_Frame, text=Version_text)
    Print_Version.grid(row=1, column=1,padx=10, pady=10)

    #Criando botão para procurar atualizações automátoicas
    Seek_Version = ttk.Button(Version_Frame, text="Procurar atualização", width=20, command=lambda: Automatic_update(root))
    Seek_Version.grid(row=2, column=1, pady=10, padx=10)

    #Botão para versão desenvolvedor
    Dev_version = ttk.Button(Version_Frame, text="Dev Version", width=20)
    Dev_version.grid(row=3, column=1, padx=8, pady=8)

    # # -------------------------------------------------------------------------------------------- #

    ## ------------------------------------ LOGS AREA --------------------------------------------------- #
    Logs_Frame = ttk.LabelFrame(root, text="Logs")
    Logs_Frame.place(x=330, y=220)

    teste = ttk.Label(Logs_Frame, text="Entrada dos Spiders")
    teste.grid(row=0, column=0, padx=10, pady=10)





    #Loop principal
    root.mainloop()


Login_Page()

#Principal_Page()

#Iniciando a env


#Entrando na página de Login















