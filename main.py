import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import re
import login

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
        
        login.criar(n, e, s, q)
        q = int(q)
        print(q)
        if q > 0:
            self.manager.current = "Client"
        else:
            self.manager.current = "Principal"

    
    def mostrar_popup(self, mensagem):
        popup = Popup(title="Erro",
                      content=Label(text=mensagem),
                      size_hint=(0.7, 0.3))
        popup.open()

class Client(Screen):
    pass

class Principal(Screen):
    pass

class Tela(App):
    def build(self):
        return gerenciador()



if __name__ == "__main__":
    Tela().run()
 