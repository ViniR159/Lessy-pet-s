from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config
from kivy.animation import Animation
from kivy.clock import Clock
import re
import os
import cadastro
from login_pasta import client, pets
import sqlite3
from kivy.uix.screenmanager import ScreenManager, FadeTransition

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

identificador = ""
class gerenciador(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition()

class Login(Screen):
    def on_enter(self):
        Clock.schedule_once(self.animar_logo, 0.5)

    def animar_logo(self, *args):
        anim = Animation(size_hint=(0.2, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.9}, duration=2, t="in_out_quart")
        anim.start(self.ids.logo)

    def validar_email(self, email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email)
    
    def login():
        pass

    def cadastro(self):
        self.manager.current = "Cadastro"



class Cadastro(Screen):
    def validar_email(self, email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email)

    
    def butao(self):
        n = self.ids.nome.text 
        e = self.ids.email.text
        s = self.ids.senha.text
        q = self.ids.quant.text

        if not self.validar_email(e):
            self.mostrar_popup("E-mail inválido! Digite um e-mail válido.")
            return

        if not n or not e or not s or not q:
            self.mostrar_popup("Preencha todos os campos!")
            return

        if not q.isdigit():
            self.mostrar_popup("Quantidade deve ser um número inteiro!")
            return

        q = int(q)
        if q <= 0:
            self.mostrar_popup("A quantidade deve ser maior que 0!")
            return

        cadastro.criar(n, e, s, q)

        client_screen = self.manager.get_screen("Client")
        client_screen.quantidade_restante = q
        client_screen.quantidade_total = q
        client_screen.identificador = n 

        self.manager.current = "Client" if q > 0 else "Principal"

    
    def mostrar_popup(self, mensagem):
        popup = Popup(title="Erro",
                      content=Label(text=mensagem),
                      size_hint=(0.7, 0.3))
        popup.open()


class Client(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.identificador = ""
        self.quantidade_restante = 0
        self.quantidade_total = 0 

    def cadastrar_pet(self):
        nome_pet = self.ids.nome_pet.text
        raca_pet = self.ids.Raca.text
        idade_pet = self.ids.idade_pet.text

        if not nome_pet or not raca_pet or not idade_pet.isdigit():
            self.mostrar_popup("Preencha todos os campos corretamente!")
            return

        self.quantidade_restante -= 1

        print(f"Pet cadastrado: Nome: {nome_pet}, Raca: {raca_pet}, Idade: {idade_pet}")
        client.cadastrar_dog(self.identificador, nome_pet, idade_pet, raca_pet) 
        pet_screen = self.manager.get_screen("Pet")
        pet_screen.identificador = self.identificador
        pet_screen.nomep = nome_pet

        self.ids.nome_pet.text = ""
        self.ids.Raca.text = ""
        self.ids.idade_pet.text = ""

                
        if self.quantidade_restante > 0:
            self.ids.label_status.text = f"Cadastro {self.quantidade_total - self.quantidade_restante + 1} de {self.quantidade_total}"
        else:  
            self.manager.current = "Pet"


    def mostrar_popup(self, mensagem):
        popup = Popup(title="Erro",
                      content=Label(text=mensagem),
                      size_hint=(0.7, 0.3))
        popup.open()

class Pet(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.identificador = ""
        self.nomep = ""

    def on_enter(self):
        self.ids.nome_pet.text = f"Fale mais sobre {self.nomep}"
    
    def criar_dog(self):
        pacote = self.ids.pacote.text
        Valor = self.ids.Valor.text
        data = self.ids.data.text

        if not pacote or not Valor.isdigit():
            self.mostrar_popup("Preencha todos os campos corretamente!")
            return


        pets.criar_arquivo_pet(self.identificador, self.nomep, Valor, data, pacote)
        self.manager.current = "Principal" 


    def mostrar_popup(self, mensagem):
        popup = Popup(title="Erro",
                      content=Label(text=mensagem),
                      size_hint=(0.7, 0.3))
        popup.open()
    

class Principal(Screen):
    pastaCliente = "login_pasta\clients"
    def on_enter(self):
        lista_clients = self.ids.get("lista_clients")

        lista_clients.clear_widgets()

        arquivos_db = [arquivo for arquivo in os.listdir(self.pastaCliente) if arquivo.endswith(".db")]

        if not arquivos_db:
            lista_clients.add_widget(Label(text="Nenhum pet cadastrado.", size_hint_y=None, height=40))
        else:
            for arquivo in arquivos_db:
                arquivo_ = arquivo.replace(".db", "").replace("_", " ")
                lista_clients.add_widget(Label(text=arquivo_, size_hint_y=None, height=40))

                btn = Button(text="Abrir", size_hint_y=None, height=40)
                btn.bind(on_release=lambda btn, arq=arquivo: self.abrir_arquivo(arq))
                lista_clients.add_widget(btn)

                btn = Button(text="Editar/atualizar", size_hint_y=None, height=40)
                btn.bind(on_release=lambda btn, arq=arquivo: self.exibir_dados(arq, self.identificador))
                lista_clients.add_widget(btn)

    def abrir_arquivo(self, nome_arquivo):
        tela_pasta_pets = self.manager.get_screen("PastaPets") 
        nome_pasta = nome_arquivo.replace(".db", "")
        tela_pasta_pets.identificador = nome_pasta
        tela_pasta_pets.abrirListaP()

        self.manager.current = "PastaPets"


class PastaPets(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.identificador = ""  
        self.nomeP = ""

    def abrirListaP(self):
        self.pastapets = f"login_pasta/clients/{self.identificador}"

        lista_pets = self.ids.get("lista_pets")
        lista_pets.clear_widgets()

        arquivos_db = [arquivo for arquivo in os.listdir(self.pastapets) if arquivo.endswith(".db")]

        if not arquivos_db:
            lista_pets.add_widget(Label(text="Nenhum pet cadastrado.", size_hint_y=None, height=40))
        else:
            for arquivo in arquivos_db:
                arquivo_ = arquivo.replace(".db", "").replace("_", " ")
                lista_pets.add_widget(Label(text=arquivo_, size_hint_y=None, height=40))

                btn = Button(text="Abrir", size_hint_y=None, height=40)
                btn.bind(on_release=lambda btn, arq=arquivo: self.exibir_dados(arq, self.identificador))
                lista_pets.add_widget(btn)

                btn = Button(text="Editar/atualizar", size_hint_y=None, height=40)
                btn.bind(on_release=lambda btn, arq=arquivo: self.exibir_dados(arq, self.identificador))
                lista_pets.add_widget(btn)

    def exibir_dados(self, nome_pet, nome):
        InfoPets = self.manager.get_screen("InfoPet") 
        nomepet = nome_pet.replace(".db", "")
        InfoPets.nomeP = nomepet
        InfoPets.pasta = nome
        InfoPets.mostrarDadosPet()

        self.manager.current = "InfoPet"
    
class InfoPet(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pasta = ""  
        self.nomeP = ""

    def on_enter(self):
        self.ids.NomePet.text = self.nomeP.replace("_", " ")

    def mostrarDadosPet(self):
        
        try:
            conexao = sqlite3.connect(f"login_pasta/clients/{self.pasta}/{self.nomeP}.db")
            cursor = conexao.cursor()

            cursor.execute("SELECT pacote, data_do_agendamento, valor FROM pet")
            dados = cursor.fetchall()

            if not dados:
                self.ids.lista_pets.add_widget(Label(text="Nenhum pet encontrado."))

            for pacote, data, valor in dados:
                self.ids.lista_pets.add_widget(Label(text=f"É pacote: {pacote}"))
                self.ids.lista_pets.add_widget(Label(text=f"Data: {data}"))
                self.ids.lista_pets.add_widget(Label(text=f"Valor: {valor}"))

            conexao.close()
        except Exception as e:
            print("Erro ao acessar o banco:", e)

class Telacadastro(App):
    def build(self):
        return gerenciador()



if __name__ == "__main__":
    Telacadastro().run()
 