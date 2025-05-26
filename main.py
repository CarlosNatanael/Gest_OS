from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from database import criar_banco
from datetime import datetime
from database import adicionar_os, buscar_os_mes, buscar_todas_os
from relatorio import enviar_relatorio

class FormularioOS(BoxLayout):
    def limpar_campos(self):
        self.ids.equipamento.text = ""
        self.ids.problema.text = ""
        self.ids.solucao.text = ""
        self.ids.tempo_reparo.text = ""

    def enviar_os(self):
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        equipamento = self.ids.equipamento.text
        problema = self.ids.problema.text
        solucao = self.ids.solucao.text
        tempo_reparo = float(self.ids.tempo_reparo.text)
        
        adicionar_os(data, equipamento, problema, solucao, tempo_reparo)
        self.mostrar_mensagem("OS salva com sucesso!")
        self.limpar_campos()

    def mostrar_os_salvas(self):
        dados = buscar_todas_os()
        popup = Popup(title="OS Cadastradas", size_hint=(0.9, 0.9))
        
        scroll = ScrollView()
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        for os in dados:
            texto = f"Data: {os[1]}\nEquipamento: {os[2]}\nProblema: {os[3]}\nSolução: {os[4]}\nTempo: {os[5]}h"
            label = Label(text=texto, size_hint_y=None, height=150, halign="left", valign="top")
            layout.add_widget(label)
        
        scroll.add_widget(layout)
        popup.content = scroll
        popup.open()



    def enviar_relatorio(self):
        mes = datetime.now().month
        ano = datetime.now().year
        dados = buscar_os_mes(mes, ano)
        enviar_relatorio("seu_email@gmail.com", dados)
        self.mostrar_mensagem("Relatório enviado!")

    def mostrar_mensagem(self, texto):
        popup = Popup(title="Aviso", content=Label(text=texto), size_hint=(0.7, 0.4))
        popup.open()

class OSApp(App):
    def build(self):
        criar_banco()  # Garante que o banco existe
        return FormularioOS()

if __name__ == "__main__":
    OSApp().run()