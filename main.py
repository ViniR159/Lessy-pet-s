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
from kivy.uix.screenmanager import ScreenManager, FadeTransition, SlideTransition
from kivy.factory import Factory
import dropbox
import io
from sqlalchemy import create_engine, text

ACCESS_TOKEN = "sl.u.AFm8cgxDRoKiJuzywu-53XXUzfTms6JeFpVLcQda_jMOId-zyp37w6nkhy3O4eQafE4kgytX1iZyS4D8d6FcNFY3P8ytLap_sL6L_oxZb0kp10snmepH7RgWrzNo0xvUjdux817R5UhaFvTFvhAX6BkNg00tuRPMEtHtjB4oP2H3AxKpVoBIIGAhSUQDhqztKfeJMMs2WJqKVGstyCIS5Sm12ETPRWvlOwB143cDdReXV-c_re3_WjZLyCU5BRH_ZIqPVLmkWcOXqVxuUWV4H-k17Kd623UgnxaCGCw2uIN4sfBJonj8rVDUhpfNwbzbI0UrJ5-_R0-mSJ2ptsxXBKrtW2Z2vAN9Z5abpGHc_jVSeAYyoEuhrXFy0FiffrawwBahlpiHoKQLVI7Gbz_m5L8lMqPqy70SA4cRdZ3HSexROhzLsw1GmYHtCsjmyVVKakmBvDeDQv36sRf_lqPO_SMjnq29vwjUbA6sGNuu3Hlk8Q2U7KR3BR8vxCDeEfVhBgG1I7uIiKNMTx8FE3Cx9fPGf1lX5yMTd3wIWhnMlXa-NtJtIFFkZ3_wwFNHNbXgN9YsbiuVHkmNyJGMcapoc7_xMU6n5dcpmdjZOHuoRzQUr67qnB83xM8LMBxB22mJrogmkuoN4HheYXPAZ5G5FVD_fP80iH4vaw6vNl8J2ZrrnziBPogfFlmZdMEeKZNQlg7A91Ux4cn2ApkMCIkFLc0_r5R8br5Z7XNCI8HhFqz1mVeZ4o5QE1RHWtr2LT9KmHBvPFv65iHhESzwC9EdeWjmuz-wnTizK24wkr0XLwZsKDCCSbEW4Lley34ZWt_hLbln_W8tSFF_RXwAWjrzOH3vXZF4uzD-wOKWGIw9vUgHyLvw3HpI04bETxUsNFW9us0u-l2vI7xdUv-rg1VGs3z9TAjJjScTqfXbWrIpuxnAhOWV-XfRrHU64n3nYz7Gd3Nr2dnjG4xOygwhBPYzmWoDzX0StX8dvkHZuiov208dpOl92XzRqa4PTwhP380P86p3lrio4j4xVys9lUZj8vIjcuHXUZ44B_HMuI61Y-WxJBarAmE-ZP6AZDf1eSe_mKI-t9ItesUwVkx0KM9wOmeViBbnZmj9p1ZAUjovF_J6sqb3DnB2GSd0hfnYrs_sguSHeqDQvQWn7vuYSr089fT54stLrkiIFyRh364CAAuBVT7UCRMWlA39L4ptynNbrKEi6w8TYjOhAWNxdaPdj-Lj6n0QlesjkAE5EZ8RtVtNf4f7TNhNEOjA4V_SujPeiubLE9JQzkXcCKq7R7A-grAzULY5TJ0BcG9JnwPp668vjsIklOc7iXAUGJBAAqKj5DFCXK9yjvt1w-3i9q6-KA0PDI6fyAmv-PSMNpXe7om55he22_Y5VF5kIianCcBlmbyvvBMQGq5fMVf-MU05X7t3-rSXo-STn-zmdDmY6EzvFQ"
dbx = dropbox.Dropbox(ACCESS_TOKEN)


Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '1280')
Config.set('graphics', 'resizable', False)


class gerenciador(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition()

class Login(Screen):
    def on_enter(self):
        Clock.schedule_once(self.animar_logo, 2)

    def animar_logo(self, *args):
        anim = Animation(size_hint=(0.3, 0.3), pos_hint={"center_x": 0.5, "center_y": 0.9}, duration=2, t="out_quint")
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


        pets.cadastrar_informacoes(self.identificador, self.nomep, Valor, data, pacote)
        self.manager.current = "Principal" 


    def mostrar_popup(self, mensagem):
        popup = Popup(title="Erro",
                      content=Label(text=mensagem),
                      size_hint=(0.7, 0.3))
        popup.open()

from supabase import create_client, Client
from urllib.parse import quote

senha = "Lessypets987@"
senha_segura = quote(senha, safe="") 
 
DATABASE_URL = f"postgresql://postgres:{senha_segura}@db.xgokuxjnlcvyzpatobne.supabase.co:5432/postgres"

db = create_engine(DATABASE_URL)

class Principal(Screen):
    def on_enter(self):
        try:
            with db.connect() as conn:
                resultado = conn.execute(text('SELECT * FROM public.login'))
                clientes = resultado.fetchall()

            lista_clients = self.ids.get("lista_clients")
            lista_clients.clear_widgets()

            if not clientes:
                lista_clients.add_widget(Label(text="Nenhum cliente cadastrado.", size_hint_y=None, height=40))
            else:
                for cliente in clientes:
                    nome_cliente = cliente[1]  # Supondo que a segunda coluna seja o nome

                    lista_clients.add_widget(Label(text=nome_cliente, size_hint_y=None, height=40))

                    # ✅ Correção: Usando lambda para passar parâmetros corretamente
                    btn_abrir = Factory.CustomButton(text="Abrir", size_hint_y=None, height=40)
                    btn_abrir.bind(on_release=lambda btn, nome=nome_cliente: self.abrir_arquivo(nome))
                    lista_clients.add_widget(btn_abrir)

                    btn_editar = Factory.CustomButton(text="Editar/Atualizar", size_hint_y=None, height=40)
                    btn_editar.bind(on_release=lambda btn, nome=nome_cliente: self.abrir_arquivo(nome))
                    lista_clients.add_widget(btn_editar)

        except Exception as e:
            lista_clients.add_widget(Label(text="Erro ao acessar os dados do Supabase!", size_hint_y=None, height=40))
            print(f"Erro: {e}")

    def abrir_arquivo(self, nome_arquivo):
        tela_pasta_pets = self.manager.get_screen("PastaPets")
        tela_pasta_pets.identificador = nome_arquivo
        tela_pasta_pets.abrirListaP()
        self.manager.current = "PastaPets"

class PastaPets(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.identificador = ""  
        self.nomeP = ""

    def abrirListaP(self):
        lista_pets = self.ids.get("lista_pets")
        lista_pets.clear_widgets()

        try:
            with db.connect() as conn:
                query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = :schema
                AND table_type = 'BASE TABLE'
                AND table_name NOT LIKE '%_visitas';
                """
                resultado = conn.execute(text(query), {"schema": self.identificador})
                pets = [row[0] for row in resultado.fetchall()]

            if not pets:
                lista_pets.add_widget(Label(text="Nenhum pet cadastrado.", size_hint_y=None, height=40))
            else:
                for pet in pets:
                    nome_pet = pet.replace("_", " ")
                    lista_pets.add_widget(Label(text=nome_pet, size_hint_y=None, height=40))

                    btn = Factory.CustomButton(text="Abrir", size_hint_y=None, height=40)
                    btn.bind(on_release=lambda btn, arq=pet: self.exibir_dados(arq, self.identificador))
                    lista_pets.add_widget(btn)

                    btn = Factory.CustomButton(text="Editar/atualizar", size_hint_y=None, height=40)
                    btn.bind(on_release=lambda btn, arq=pet: self.exibir_dados(arq, self.identificador))
                    lista_pets.add_widget(btn)

        except Exception as e:
            lista_pets.add_widget(Label(text="Erro ao acessar os dados do Supabase!", size_hint_y=None, height=40))
            print(f"Erro: {e}")

    def exibir_dados(self, nome_pet, nome):
        InfoPets = self.manager.get_screen("InfoPet")
        InfoPets.nomeP = nome_pet
        InfoPets.schema = nome
        print("nomep = ", nome_pet,
              "nome = ", nome)
        InfoPets.mostrarDadosPet()
        self.manager.current = "InfoPet"

class InfoPet(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.schema = ""  # identificador do cliente
        self.nomeP = ""   # nome do pet

    def on_enter(self):
        self.ids.NomePet.text = self.nomeP.replace("_", " ")
        self.mostrarDadosPet()

    def mostrarDadosPet(self):
        lista_pets = self.ids.get("lista_pets")
        lista_pets.clear_widgets()

        if not self.schema or not self.nomeP:
            lista_pets.add_widget(Label(text="Dados do pet não carregados.", size_hint_y=None, height=40))
            print("Erro: Schema ou nome do pet não definido.")
            return

        try:
            tabela = f"{self.nomeP}_visitas"

            with db.connect() as conn:
                query = text(f'SELECT * FROM "{self.schema}"."{tabela}"')
                resultado = conn.execute(query)
                dados = resultado.fetchall()

            if not dados:
                lista_pets.add_widget(Label(text="Nenhuma informação encontrada.", size_hint_y=None, height=40))
                return

            for linha in dados:
                pacote = linha[1]
                data_agendamento = linha[2]
                valor = linha[3]

                lista_pets.add_widget(Label(text=f"Pacote: {pacote}", size_hint_y=None, height=40))
                lista_pets.add_widget(Label(text=f"Data: {data_agendamento}", size_hint_y=None, height=40))
                lista_pets.add_widget(Label(text=f"Valor: {valor}", size_hint_y=None, height=40))

        except Exception as e:
            lista_pets.add_widget(Label(text="Erro ao acessar os dados do Supabase!", size_hint_y=None, height=40))
            print(f"Erro: {e}")
            
class Telacadastro(App):
    def build(self):
        return gerenciador()

if __name__ == "__main__":
    Telacadastro().run()