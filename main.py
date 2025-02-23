from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import re
import login
from Login import client

identificador = "A"
class gerenciador(ScreenManager):
    pass

class Login(Screen):
    def validar_email(self, email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email)

    
    def butao(self):
        n =  self.ids.nome.text 
        e = self.ids.email.text
        s = self.ids.senha.text
        q =  self.ids.quant.text

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

        login.criar(n, e, s, q)
        if q > 0:
            self.manager.get_screen("Client").quantidade_restante = q
            self.manager.get_screen("Client").quantidade_total = q
            self.manager.get_screen("Client").dono = n
            identificador = n

            self.manager.current = "Client"
        else:
            self.manager.current = "Principal"

    
    def mostrar_popup(self, mensagem):
        popup = Popup(title="Erro",
                      content=Label(text=mensagem),
                      size_hint=(0.7, 0.3))
        popup.open()


class Client(Screen):
    dono = ""
    quantidade_restante = 0
    quantidade_total = 0

    def cadastrar_pet(self):
        nome_pet = self.ids.nome_pet.text
        raca_pet = self.ids.Raca.text
        idade_pet = self.ids.idade_pet.text

        if not nome_pet or not raca_pet or not idade_pet.isdigit():
            self.mostrar_popup("Preencha todos os campos corretamente!")
            return

        self.quantidade_restante -= 1

        print(f"Pet cadastrado: Nome: {nome_pet}, Raca: {raca_pet}, Idade: {idade_pet}")
        client.cadastrar_dog(nome_pet, raca_pet, idade_pet)

        self.ids.nome_pet.text = ""
        self.ids.Raca.text = ""
        self.ids.idade_pet.text = ""

        if self.quantidade_restante > 0:
            self.ids.label_status.text = f"Cadastro {self.quantidade_total - self.quantidade_restante + 1} de {self.quantidade_total}"
        else: 
            self.manager.current = "Principal"

    def mostrar_popup(self, mensagem):
        popup = Popup(title="Erro",
                      content=Label(text=mensagem),
                      size_hint=(0.7, 0.3))
        popup.open()


class Principal(Screen):
    pass

class Tela(App):
    def build(self):
        return gerenciador()



if __name__ == "__main__":
    Tela().run()
 