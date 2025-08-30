from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.widget import Widget

class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_active = ""
        self.background_color = (0, 0, 0, 0)
        self.multiline = False
        self.size_hint_y = None
        self.height = dp(55)
        self.padding = [dp(8), dp(8), dp(8), dp(8)]
        self.font_size = sp(24)
        self.color = (1, 1, 1, 1)
        self.hint_text_color = (0.9, 0.9, 0.9, 0.9)
        self.cursor_color = (1, 1, 1, 1)
        self.selection_color = (0.2, 0.6, 1, 0.5)
        self.bold = True

        with self.canvas.before:
            Color(0.1, 0.4, 0.7, 0.9)
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(12)]
            )
            
            Color(1, 1, 1, 0.3)
            self.border_rect = RoundedRectangle(
                pos=(self.pos[0]+dp(2), self.pos[1]+dp(2)),
                size=(self.size[0]-dp(4), self.size[1]-dp(4)),
                radius=[dp(8)]
            )

        self.bind(pos=self._update_rects, size=self._update_rects)

    def _update_rects(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_rect.pos = (self.pos[0]+dp(2), self.pos[1]+dp(2))
        self.border_rect.size = (self.size[0]-dp(4), self.size[1]-dp(4))

    def on_focus(self, instance, value):
        if value:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(0.2, 0.5, 0.9, 1)
                self.bg_rect = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[dp(12)]
                )
                Color(1, 1, 1, 0.5)
                self.border_rect = RoundedRectangle(
                    pos=(self.pos[0]+dp(2), self.pos[1]+dp(2)),
                    size=(self.size[0]-dp(4), self.size[1]-dp(4)),
                    radius=[dp(8)]
                )
        else:
            self._update_rects()
            self.canvas.before.clear()
            with self.canvas.before:
                Color(0.1, 0.4, 0.7, 0.9)
                self.bg_rect = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[dp(12)]
                )
                Color(1, 1, 1, 0.3)
                self.border_rect = RoundedRectangle(
                    pos=(self.pos[0]+dp(2), self.pos[1]+dp(2)),
                    size=(self.size[0]-dp(4), self.size[1]-dp(4)),
                    radius=[dp(8)]
                )

class HoverButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.1, 0.4, 0.7, 1)
        self.color = (1, 1, 1, 1)
        self.size_hint_y = None
        self.height = dp(50)
        self.font_size = sp(22)
        self.bold = True
        self.border_radius = dp(12)

        with self.canvas.before:
            Color(*self.background_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.border_radius])
        
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class InicioSesionJuezScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'ini_juez'  # Cambiado de 'inicio_sesion' a 'ini_juez'
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=[dp(30), dp(5), dp(30), dp(30)], spacing=dp(15))

        with main_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.background_rect = Rectangle(size=Window.size, pos=self.pos)
        
        self.bind(size=self.update_background, pos=self.update_background)

        form_container = BoxLayout(
            orientation='vertical', 
            size_hint=(0.8, None),
            height=Window.height * 0.8,
            pos_hint={'center_x': 0.5, 'top': 1.1},
            spacing=dp(15))
        
        logo = Image(
            source="Imagen5-Photoroom.png", 
            size_hint=(1, None), 
            height=dp(150),
            pos_hint={'top': 1.1})
        form_container.add_widget(logo)

        titulo = Label(
            text='INICIO DE SESIÓN',
            font_size=sp(32),
            color=(0.1, 0.4, 0.7, 1),
            bold=True,
            size_hint_y=None,
            height=dp(80))
        form_container.add_widget(titulo)
        titulo2 = Label(
            text='JUEZ',
            font_size=sp(50),
            color=(0.7, 0.1, 0.1, 1),
            bold=True,
            size_hint_y=None,
            height=dp(80))
        form_container.add_widget(titulo2)

        campos_layout = BoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=None, height=dp(120))

        contraeña_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        contraeña_layout.add_widget(Label(
            text='CONTRASEÑA',
            font_size=sp(20),
            color=(0.1, 0.1, 0.2, 1),
            size_hint_y=None,
            height=dp(30)))
        self.contraeña_input = RoundedTextInput(hint_text='********', password=True)
        contraeña_layout.add_widget(self.contraeña_input)
        campos_layout.add_widget(contraeña_layout)

        form_container.add_widget(campos_layout)

        form_container.add_widget(Widget(size_hint_y=None, height=dp(20)))

        botones_layout = BoxLayout(
            orientation='horizontal', 
            spacing=dp(20), 
            size_hint_y=None, 
            height=dp(50))

        btn_iniciar = HoverButton(text='INICIAR SESIÓN', size_hint=(0.5, 1))
        btn_iniciar.bind(on_press=self.iniciar_sesion)
        botones_layout.add_widget(btn_iniciar)

        btn_volver = HoverButton(
            text='VOLVER',
            background_color=(0.7, 0.1, 0.1, 1),
            size_hint=(0.5, 1))
        btn_volver.bind(on_press=self.volver)
        botones_layout.add_widget(btn_volver)

        form_container.add_widget(botones_layout)

        recuperar_label = Label(
            text='¿Olvidaste tu contraseña?',
            font_size=sp(16),
            color=(0.1, 0.4, 0.7, 1),
            size_hint_y=None,
            height=dp(30))
        form_container.add_widget(recuperar_label)

        main_layout.add_widget(form_container)
        self.add_widget(main_layout)

    def update_background(self, *args):
        self.background_rect.size = Window.size
        self.background_rect.pos = self.pos

    def on_enter(self, *args):
        Clock.schedule_once(self.establecer_foco, 0.1)

    def establecer_foco(self, dt):
        self.contraeña_input.focus = True

    def iniciar_sesion(self, instance):
        contraeña_VALIDA = "123"
        
        contraeña = self.contraeña_input.text.strip()
        
        if contraeña == contraeña_VALIDA:
            self.manager.current = 'tablero_central'
            self.mostrar_mensaje("Éxito", "Sesión iniciada correctamente")
        else:
            self.mostrar_mensaje("Error", "Contraseña incorrecta")

    def mostrar_mensaje(self, titulo, mensaje):
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        lbl_mensaje = Label(
            text=mensaje,
            color=(0.2, 0.6, 1, 1),
            font_size=sp(20),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80))
        content.add_widget(lbl_mensaje)
        
        btn_aceptar = Button(
            text='ACEPTAR',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))
        
        popup = Popup(
            title=titulo,
            title_color=(0.2, 0.6, 1, 1),
            title_size=sp(22),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=(dp(450), dp(250)),
            separator_height=0,
            background=''
        )
        
        with popup.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            popup.rect = RoundedRectangle(
                pos=popup.pos,
                size=popup.size,
                radius=[dp(10)]
            )
        
        def update_popup_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        
        popup.bind(pos=update_popup_rect, size=update_popup_rect)
        
        btn_aceptar.bind(on_press=popup.dismiss)
        content.add_widget(btn_aceptar)
        
        popup.open()

    def volver(self, instance):
        self.manager.current = 'main'