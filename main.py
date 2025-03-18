from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import re
import os
import login
from login_pasta import client
from login_pasta import pets

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


identificador = ""
class gerenciador(ScreenManager):
    pass

class Login(Screen):
    def validar_email(self, email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email)

    
    def butao(self):
        n = self.ids.nome.text 
        e = self.ids.email.text
        s = self.ids.senha.text
        q = self.ids.quant.text

        # if not self.validar_email(e):
        #     self.mostrar_popup("E-mail inválido! Digite um e-mail válido.")
        #     return

        # if not n or not e or not s or not q:
        #     self.mostrar_popup("Preencha todos os campos!")
        #     return

        # if not q.isdigit():
        #     self.mostrar_popup("Quantidade deve ser um número inteiro!")
        #     return

        q = int(q)
        if q <= 0:
            self.mostrar_popup("A quantidade deve ser maior que 0!")
            return

        login.criar(n, e, s, q)

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

    # def mostrar_pet(identificador):

    #     if not tabelas:
    #         self.ids.lista_pets.add_widget(Label(text="Nenhum pet cadastrado.", size_hint_y=None, height=40))
    #         return
        
    #     for tabela in tabelas:
    #         pets = client.buscar_dados_tabela(self.identificador, tabela)
    #         for pet in pets:
    #             pet_texto = f"Tabela: {tabela} | ID: {pet[0]} | Nome: {pet[1]} | Idade: {pet[2]} | Raça: {pet[3]}"
    #             self.ids.lista_pets.add_widget(Label(text=pet_texto, size_hint_y=None, height=40))

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
                lista_clients.add_widget(Label(text=arquivo, size_hint_y=None, height=40))

                btn = Button(text="Abrir", size_hint_y=None, height=40)
                btn.bind(on_release=lambda btn, arq=arquivo: self.abrir_arquivo(arq))
                lista_clients.add_widget(btn)

    def abrir_arquivo(self, nome_arquivo):
        caminho_completo = os.path.join(self.pastaCliente, nome_arquivo)
        print(f"Abrindo arquivo: {caminho_completo}") 


class PastaPets(Screen):
    pastapets = "login_pasta\clients"
    def on_enter(self):
        lista_clients = self.ids.get("lista_clients")

        lista_clients.clear_widgets()

        arquivos_db = [arquivo for arquivo in os.listdir(self.pastaCliente) if arquivo.endswith(".db")]

        if not arquivos_db:
            lista_clients.add_widget(Label(text="Nenhum pet cadastrado.", size_hint_y=None, height=40))
        else:
            for arquivo in arquivos_db:
                lista_clients.add_widget(Label(text=arquivo, size_hint_y=None, height=40))

                btn = Button(text="Abrir", size_hint_y=None, height=40)
                btn.bind(on_release=lambda btn, arq=arquivo: self.abrir_arquivo(arq))
                lista_clients.add_widget(btn)

    def abrir_arquivo(self, nome_arquivo):
        caminho_completo = os.path.join(self.pastaCliente, nome_arquivo)
        print(f"Abrindo arquivo: {caminho_completo}") 

class Telacadastro(App):
    def build(self):
        return gerenciador()



if __name__ == "__main__":
    Telacadastro().run()
 