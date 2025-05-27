from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from datetime import datetime
from database import adicionar_os, buscar_todas_os
from kivy.core.text import LabelBase
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

# Registrar as fontes
LabelBase.register(
    name="Roboto",
    fn_regular="fonts/Roboto-Regular.ttf",
    fn_bold="fonts/Roboto-Bold.ttf"
)

# Configuração padrão para todos os widgets
from kivy.config import Config
Config.set('kivy', 'default_font', ['Roboto', 'Arial'])

class DarkTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.1, 0.1, 0.1, 1)  # fundo escuro
        self.foreground_color = (1, 1, 1, 1)  # texto branco
        self.cursor_color = (1, 1, 1, 1)
        self.size_hint_y = None
        self.height = 40
        self.padding = [10, 10]  # padding interno

class DarkButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)  # completamente transparente
        self.color = (1, 1, 1, 1)  # texto branco
        self.size_hint_y = None
        self.height = 40
class FormularioOS(BoxLayout):
    def limpar_campos(self):
        self.ids.equipamento.text = ""
        self.ids.problema.text = ""
        self.ids.solucao.text = ""
        self.ids.tempo_reparo.text = ""

    def validar_campos(self):
        if not self.ids.equipamento.text.strip():
            self.mostrar_mensagem("Preencha o equipamento!")
            return False
        if not self.ids.problema.text.strip():
            self.mostrar_mensagem("Descreva o problema!")
            return False
        if not self.ids.solucao.text.strip():
            self.mostrar_mensagem("Descreva a solução!")
            return False
        if not self.ids.tempo_reparo.text.strip():
            self.mostrar_mensagem("Informe o tempo de reparo!")
            return False
        if not self.ids.inicio_os.text.strip():
            self.mostrar_mensagem("Informe o início da OS!")
            return False
        if not self.ids.fim_os.text.strip():
            self.mostrar_mensagem("Informe o fim da OS!")
            return False

        # Tenta converter para datetime
        try:
            inicio = datetime.strptime(self.ids.inicio_os.text.strip(), "%d/%m/%Y %H:%M")
            fim = datetime.strptime(self.ids.fim_os.text.strip(), "%d/%m/%Y %H:%M")
        except ValueError:
            self.mostrar_mensagem("Formato de data/hora inválido! Use: dd/mm/yyyy hh:mm")
            return False

        if fim <= inicio:
            self.mostrar_mensagem("O fim da OS deve ser depois do início!")
            return False

        try:
            float(self.ids.tempo_reparo.text)
        except ValueError:
            self.mostrar_mensagem("Tempo de reparo deve ser um número!")
            return False
        return True

    def enviar_os(self):
        if not self.validar_campos():
            return
        
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        equipamento = self.ids.equipamento.text
        problema = self.ids.problema.text
        solucao = self.ids.solucao.text
        inicio = datetime.strptime(self.ids.inicio_os.text.strip(), "%d/%m/%Y %H:%M")
        fim = datetime.strptime(self.ids.fim_os.text.strip(), "%d/%m/%Y %H:%M")
        tempo_reparo = (fim - inicio).total_seconds() / 60  # em minutos
        
        adicionar_os(data, equipamento, problema, solucao, tempo_reparo, inicio, fim)
        self.mostrar_mensagem("OS salva com sucesso!")
        self.limpar_campos()

    def mostrar_os_salvas(self):
        dados = buscar_todas_os()
        popup = Popup(title="OS Cadastradas", size_hint=(0.9, 0.9))
        
        scroll = ScrollView()
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        for os in dados:
            texto =     f"Início: {os[6]}\n"f"Fim: {os[7]}\n"f"Equipamento: {os[2]}\n"f"Problema: {os[3]}\n"f"Solução: {os[4]}\n"f"Tempo: {os[5]:.0f} minutos"
            label = Label(text=texto, size_hint_y=None, height=150, halign="left", valign="top")
            layout.add_widget(label)
        
        scroll.add_widget(layout)
        popup.content = scroll
        popup.open()

    def mostrar_mensagem(self, texto, titulo="Aviso"):
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=texto))
        btn = Button(text="OK", size_hint_y=None, height=50)
        popup = Popup(title=titulo, content=content, size_hint=(0.7, 0.4))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()

class OSApp(App):
    title = "Gestão de OS"
    icon = "assets/icon.png"
    def build(self):
        return FormularioOS()

if __name__ == "__main__":
    OSApp().run()