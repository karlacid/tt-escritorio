from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle

class PopupMensaje(Popup):
    def __init__(self, titulo, mensaje, **kwargs):
        super().__init__(**kwargs)
        
        self.title = titulo
        self.title_color = (0.2, 0.6, 1, 1)
        self.title_size = sp(22)
        self.title_align = 'center'
        
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        lbl_mensaje = Label(
            text=mensaje,
            color=(0.2, 0.6, 1, 1),
            font_size=sp(20),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80)
        )
        content.add_widget(lbl_mensaje)
        
        btn_aceptar = Button(
            text='ACEPTAR',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18)
        )
        
        btn_aceptar.bind(on_press=self.dismiss)
        content.add_widget(btn_aceptar)

        self.content = content
        self.size_hint = (None, None)
        self.size = (dp(450), dp(250))
        self.separator_height = 0
        self.background = ''

        with self.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(10)]
            )
        
        self.bind(pos=self.update_popup_rect, size=self.update_popup_rect)

    def update_popup_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

class MyApp(App):
    def build(self):
        self.popup = PopupMensaje("ATENCIÓN", "Incidencia")
        self.popup.open()
        return BoxLayout()

if __name__ == '__main__':
    MyApp().run()
