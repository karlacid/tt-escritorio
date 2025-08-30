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
from kivy.uix.behaviors import ButtonBehavior

class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Configuración mejorada
        self.background_normal = ""
        self.background_active = ""
        self.background_color = (0, 0, 0, 0)  # Fondo transparente
        self.multiline = False
        self.size_hint_y = None
        self.height = dp(55)  # Altura aumentada
        self.padding = [dp(8), dp(8), dp(8), dp(8)]  # Más espacio interno
        self.font_size = sp(24)  # Tamaño de fuente grande
        self.color = (1, 1, 1, 1)  # Texto blanco
        self.hint_text_color = (0.9, 0.9, 0.9, 0.9)  # Hint semi-transparente blanco
        self.cursor_color = (1, 1, 1, 1)  # Cursor blanco
        self.selection_color = (0.2, 0.6, 1, 0.5)  # Color de selección azul claro
        self.bold = True  # Texto en negrita

        # Efectos gráficos
        with self.canvas.before:
            # Fondo azul
            Color(0.1, 0.4, 0.7, 0.9)
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(12)]
            )

            # Borde interior
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
            # Estado activo
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
            # Estado normal
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

class EnlaceRecuperar(ButtonBehavior, Label):
    pass

class InicioSesionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        self.popup_usuario = None
        self.popup_correo = None

    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=[dp(30), dp(5), dp(30), dp(30)], spacing=dp(15))

        # Fondo blanco
        with main_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.background_rect = Rectangle(size=Window.size, pos=self.pos)

        self.bind(size=self.update_background, pos=self.update_background)

        # Contenedor del formulario
        form_container = BoxLayout(
            orientation='vertical',
            size_hint=(0.8, None),
            height=Window.height * 0.9,
            pos_hint={'center_x': 0.5, 'top': 1.1},
            spacing=dp(15))

        # Logo
        logo = Image(
            source="Imagen5-Photoroom.png",
            size_hint=(1, None),
            height=dp(150),
            pos_hint={'top': 1.1})
        form_container.add_widget(logo)

        # Título
        titulo = Label(
            text='INICIO DE SESIÓN',
            font_size=sp(32),
            color=(0.1, 0.4, 0.7, 1),
            bold=True,
            size_hint_y=None,
            height=dp(80))
        form_container.add_widget(titulo)

        # Campos de entrada
        campos_layout = BoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=None, height=dp(220))

        # Campo correo
        correo_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        correo_layout.add_widget(Label(
            text='Correo electrónico',
            font_size=sp(20),
            color=(0.1, 0.1, 0.2, 1),
            size_hint_y=None,
            height=dp(30)))
        self.correo_input = RoundedTextInput(hint_text='usuario@ejemplo.com')
        correo_layout.add_widget(self.correo_input)
        campos_layout.add_widget(correo_layout)

        # Campo contraseña
        contraseña_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        contraseña_layout.add_widget(Label(
            text='contraseña',
            font_size=sp(20),
            color=(0.1, 0.1, 0.2, 1),
            size_hint_y=None,
            height=dp(30)))
        self.contraseña_input = RoundedTextInput(hint_text='********', password=True)
        contraseña_layout.add_widget(self.contraseña_input)
        campos_layout.add_widget(contraseña_layout)

        form_container.add_widget(campos_layout)

        # Espaciador
        form_container.add_widget(Widget(size_hint_y=None, height=dp(10)))

        # Botones
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

        # Enlace recuperar contraseña
        recuperar_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30), pos_hint={'center_x': 0.5})
        recuperar_label = EnlaceRecuperar(
            text='¿Olvidaste tu contraseña?',
            font_size=sp(16),
            color=(0.1, 0.4, 0.7, 1),
            underline=True,
            on_press=self.mostrar_popup_usuario
        )
        recuperar_layout.add_widget(recuperar_label)
        form_container.add_widget(recuperar_layout)

        main_layout.add_widget(form_container)
        self.add_widget(main_layout)

    def update_background(self, *args):
        self.background_rect.size = Window.size
        self.background_rect.pos = self.pos

    def on_enter(self, *args):
        Clock.schedule_once(self.establecer_foco, 0.1)

    def establecer_foco(self, dt):
        self.correo_input.focus = True

    def iniciar_sesion(self, instance):
        USUARIO_VALIDO = "a"
        contraseña_VALIDA = "1"

        correo = self.correo_input.text.strip()
        contraseña = self.contraseña_input.text.strip()

        if correo == USUARIO_VALIDO and contraseña == contraseña_VALIDA:
            App.get_running_app().root.current = 'ini'
            self.mostrar_mensaje("Éxito", "Sesión iniciada correctamente")
        else:
            self.mostrar_mensaje("Error", "Correo o contraseña incorrectos")

    def mostrar_mensaje(self, titulo, mensaje):
        # Configuración del contenido del popup
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        # Etiqueta del mensaje
        lbl_mensaje = Label(
            text=mensaje,
            color=(0.2, 0.6, 1, 1),
            font_size=sp(20),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80))
        content.add_widget(lbl_mensaje)

        # Botón de aceptar
        btn_aceptar = Button(
            text='ACEPTAR',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))

        # Crear el popup
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

        # Fondo azul del popup con esquinas redondeadas
        with popup.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            popup.rect = RoundedRectangle(
                pos=popup.pos,
                size=popup.size,
                radius=[dp(15)]
            )

        # Función para actualizar el fondo cuando cambie de posición/tamaño
        def update_popup_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        popup.bind(pos=update_popup_rect, size=update_popup_rect)

        btn_aceptar.bind(on_press=popup.dismiss)
        content.add_widget(btn_aceptar)

        popup.open()

    def mostrar_popup_usuario(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        lbl_usuario = Label(text='Ingresa tu nombre de usuario:', font_size=sp(20), color=(0.2, 0.6, 1, 1))
        txt_usuario = TextInput(hint_text='Tu nombre de usuario', multiline=False, size_hint_y=None, height=dp(40))
        btn_aceptar = Button(text='ACEPTAR', size_hint_y=None, height=dp(40),
                               background_normal='', background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1), bold=True, font_size=sp(18))

        content.add_widget(lbl_usuario)
        content.add_widget(txt_usuario)
        content.add_widget(btn_aceptar)

        self.popup_usuario = Popup(
            title='Recuperar Contraseña',
            title_color=(0.2, 0.6, 1, 1),
            title_size=sp(22),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=(dp(400), dp(250)),
            separator_height=0,
            background=''
        )
        with self.popup_usuario.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            self.popup_usuario.rect = RoundedRectangle(pos=self.popup_usuario.pos, size=self.popup_usuario.size, radius=[dp(15)])
        self.popup_usuario.bind(pos=self._update_popup_rect, size=self._update_popup_rect)

        btn_aceptar.bind(on_press=lambda btn: self.mostrar_popup_correo(txt_usuario.text))
        self.popup_usuario.open()

    def mostrar_popup_correo(self, usuario):
        if self.popup_usuario:
            self.popup_usuario.dismiss() # Cierra el primer popup
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        lbl_correo_enviado = Label(
            text=f'Se ha enviado un correo a la cuenta asociada con el usuario: {usuario}',
            color=(0.2, 0.6, 1, 1),
            font_size=sp(20),
            halign='center',  # Centrar el texto horizontalmente
            valign='middle',
            size_hint_y=None,
            height=dp(80),
            text_size=(dp(400 - 40), None), 
            markup=True 
        )
        btn_cerrar = Button(
            text='CERRAR',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18),
            on_press=self.cerrar_popup_correo
        )
        content.add_widget(lbl_correo_enviado)
        content.add_widget(btn_cerrar)

        self.popup_correo = Popup(
            title='Recuperar Contraseña',
            title_color=(0.2, 0.6, 1, 1),
            title_size=sp(22),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=(dp(450), dp(250)),
            separator_height=0,
            background=''
        )
        with self.popup_correo.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            self.popup_correo.rect = RoundedRectangle(pos=self.popup_correo.pos, size=self.popup_correo.size, radius=[dp(15)])
        self.popup_correo.bind(pos=self._update_popup_rect, size=self._update_popup_rect)
        self.popup_correo.open()

    def cerrar_popup_correo(self, instance):
        if self.popup_correo:
            self.popup_correo.dismiss()

    def _update_popup_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def _update_title_bg(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.08, 0.3, 0.6, 1)
            Rectangle(
                pos=(instance.parent.x, instance.parent.top - instance.height),
                size=(instance.parent.width, instance.height)
            )

    def volver(self, instance):
        self.manager.current = 'main'