from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MinhaApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        botao = Button(text="Criar OS", size_hint=(0.5, 0.2))
        botao.bind(on_press=self.criar_os)
        layout.add_widget(botao)
        return layout

    def criar_os(self, instance):
        print("Nova OS criada!")  # Aqui você implementa a lógica

MinhaApp().run()