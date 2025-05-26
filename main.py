from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime
from database import adicionar_os, buscar_os_mes
from relatorio import enviar_relatorio

class FormularioOS(BoxLayout):
    def enviar_os(self):
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        equipamento = self.ids.equipamento.text
        problema = self.ids.problema.text
        solucao = self.ids.solucao.text
        tempo_reparo = float(self.ids.tempo_reparo.text)

        adicionar_os(data, equipamento, problema, solucao, tempo_reparo)
        self.mostrar_mensagem("OS salva com sucesso!")

    def enviar_relatorio(self):
        mes = datetime.now().month
        ano = datetime.now().year
        dados = buscar_os_mes(mes,ano)
        enviar_relatorio("Relatório enviado!")
    
    def mostrar_mensagem(self, texto):
        popup = Popup(title="Aviso", content=Label(text=texto), size_hint=(0.7, 0.4))
        popup.open()

class OSApp(App):
    def build(self):
        return FormularioOS()
    
if __name__ == "__main__":
    OSApp().run()