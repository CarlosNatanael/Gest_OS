from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button  # Importação adicionada
from datetime import datetime
from database import adicionar_os, buscar_todas_os
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.core.text import LabelBase
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

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
        # Pode adicionar lógica de inicialização aqui se necessário

class DarkButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class DarkTheme:
    """Paleta de cores do tema escuro"""
    bg_color = [0.07, 0.07, 0.07, 1]  # #121212
    card_color = [0.12, 0.12, 0.12, 1]  # #1E1E1E
    text_primary = [0.88, 0.88, 0.88, 1]  # #E1E1E1
    accent_color = [0.73, 0.53, 0.99, 1]  # #BB86FC

class GradientWidget:
    def __init__(self, colors=[(0.1,0.5,0.8,1), (0.2,0.6,0.9,1)]):
        self.colors = colors
    
    def apply_gradient(self, widget):
        with widget.canvas.before:
            for i, color in enumerate(self.colors):
                Color(*color)
                Rectangle(
                    pos=(widget.x, widget.y + (widget.height/len(self.colors))*i),
                    size=(widget.width, widget.height/len(self.colors))
                )
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

    def mostrar_mensagem(self, texto, titulo="Aviso"):
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=texto))
        btn = Button(text="OK", size_hint_y=None, height=50)
        popup = Popup(title=titulo, content=content, size_hint=(0.7, 0.4))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()

class OSApp(App):
    def build(self):
        return FormularioOS()

if __name__ == "__main__":
    OSApp().run()