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
from kivy.uix.scrollview import ScrollView


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
        self.height = dp(45)
        self.font_size = dp(20)
        self.bold = True
        self.border_radius = dp(10)

        with self.canvas.before:
            Color(*self.background_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.border_radius])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class RegistroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(10)],
            spacing=dp(10)
        )

        # Fondo
        with main_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.background_rect = Rectangle(size=Window.size, pos=self.pos)

        self.bind(size=self.update_background, pos=self.update_background)

        # Logo
        logo = Image(
            source="Imagen5-Photoroom.png",
            size_hint=(1, None),
            height=dp(120),
            pos_hint={'center_x': 0.5}
        )
        main_layout.add_widget(logo)

        # ScrollView para el formulario
        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            bar_width=10,
            scroll_type=['bars', 'content']
        )

        # Contenedor del formulario (dentro del ScrollView)
        form_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            spacing=dp(12),
            padding=[dp(50), dp(50)],
            pos_hint={'center_x': 0.5}
        )
        # Ajustar altura según contenido
        form_container.bind(minimum_height=form_container.setter('height'))

        # Título
        titulo = Label(
            text='REGISTRO',
            font_size=dp(32),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )
        form_container.add_widget(titulo)

        # Función para crear campos de formulario
        def crear_campo(texto, hint_text, password=False):
            campo_layout = BoxLayout(
                orientation='vertical',
                spacing=dp(5),
                size_hint_y=None,
                height=dp(85)
            )

            campo_layout.add_widget(Label(
                text=texto,
                font_size=dp(18),
                color=(0.1, 0.1, 0.2, 1),
                size_hint_y=None,
                height=dp(25)
            ))

            input_field = RoundedTextInput(
                hint_text=hint_text,
                password=password,
                size_hint_y=None,
                height=dp(55)
            )
            campo_layout.add_widget(input_field)

            return campo_layout, input_field

        # Campos del formulario (simplificando nombres)
        campos = [
            ('Nombre', 'Ingresa tu nombre', False),
            ('Apellidos', 'Ingresa tu Apellidos', False),
            ('Usuario', 'Ingresa tu usuario', False),
            ('Correo', 'usuario@ejemplo.com', False),  # Cambiado a "Correo" para simplificar
            ('contraseña', '********', True),
            ('Confirmar contraseña', '********', True)
        ]

        # Añadir campos al formulario
        for texto, hint, is_password in campos:
            layout, input_field = crear_campo(texto, hint, is_password)
            # Generamos nombres de atributos consistentes
            attr_name = texto.lower().replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u") + "_input"
            setattr(self, attr_name, input_field)
            form_container.add_widget(layout)

        # Espaciador para separar los campos de los botones
        form_container.add_widget(Widget(size_hint_y=None, height=dp(10)))

        # Contenedor de botones
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50),
            padding=[0, dp(10), 0, 0]
        )

        # Botón Registrar
        btn_registrar = HoverButton(text='REGISTRARSE')
        btn_registrar.bind(on_press=self.registrar)
        botones_layout.add_widget(btn_registrar)

        # Botón Volver
        btn_volver = HoverButton(
            text='VOLVER',
            background_color=(0.7, 0.1, 0.1, 1)
        )
        btn_volver.bind(on_press=self.volver)
        botones_layout.add_widget(btn_volver)

        # Añadir botones al formulario
        form_container.add_widget(botones_layout)

        # Añadir formulario al ScrollView
        scroll_view.add_widget(form_container)

        # Añadir ScrollView al layout principal
        main_layout.add_widget(scroll_view)

        # Añadir layout principal a la pantalla
        self.add_widget(main_layout)

    def update_background(self, *args):
        self.background_rect.size = Window.size
        self.background_rect.pos = self.pos

    def on_enter(self, *args):
        Clock.schedule_once(self.establecer_foco, 0.1)

    def establecer_foco(self, dt):
        self.nombre_input.focus = True

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

    def mostrar_popup_campos_faltantes_registro(self, campos_faltantes):
        content = ScrollView()
        lista_campos = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20), size_hint_y=None)
        lista_campos.bind(minimum_height=lista_campos.setter('height'))

        titulo_label = Label(
            text='Campos Obligatorios Faltantes:',
            font_size=sp(20),
            color=(0.2, 0.6, 1, 1),
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        lista_campos.add_widget(titulo_label)

        for mensaje in campos_faltantes:
            label_campo = Label(
                text=f"• {mensaje}",
                font_size=sp(18),
                color=(0.1, 0.1, 0.2, 1),
                size_hint_y=None,
                height=dp(30)
            )
            lista_campos.add_widget(label_campo)

        content.add_widget(lista_campos)

        popup = Popup(
            title='¡Atención!',
            title_color=(0.2, 0.6, 1, 1),
            title_size=sp(22),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=(dp(500), dp(400)),
            separator_height=0,
            background=''
        )

        with popup.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            popup.rect = RoundedRectangle(
                pos=popup.pos,
                size=popup.size,
                radius=[dp(15)]
            )

        def update_popup_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        popup.bind(pos=update_popup_rect, size=update_popup_rect)

        btn_cerrar = Button(
            text='CERRAR',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))
        btn_cerrar.bind(on_press=popup.dismiss)
        lista_campos.add_widget(btn_cerrar)

        popup.open()

    def registrar(self, instance):
        required_fields = [
            (self.nombre_input, "Por favor ingresa tu nombre"),
            (self.apellidos_input, "Por favor ingresa tu Apellidos"),
            (self.usuario_input, "Por favor ingresa un nombre de usuario"),
            (self.correo_input, "Por favor ingresa tu correo electrónico"),  # Ahora usa correo_input
            (self.contraseña_input, "Por favor ingresa una contraseña")
        ]

        campos_faltantes = []
        for campo, mensaje in required_fields:
            if not campo.text.strip():
                campos_faltantes.append(mensaje)

        if campos_faltantes:
            self.mostrar_popup_campos_faltantes_registro(campos_faltantes)
            return

        # Validar formato de correo electrónico (simple)
        if "@" not in self.correo_input.text or "."not in self.correo_input.text:
            self.mostrar_mensaje("Correo inválido", "Por favor ingresa un correo electrónico válido")
            self.correo_input.focus = True
            return

        # Validar contraseñas coincidentes
        if self.contraseña_input.text != self.confirmar_contraseña_input.text:
            self.mostrar_mensaje("Error en contraseña", "Las contraseñas no coinciden")
            self.contraseña_input.text = ""
            self.confirmar_contraseña_input.text = ""
            self.contraseña_input.focus = True
            return

        # Validar longitud mínima de contraseña, definir regla de negocio
        #----------------------------------------------------------
        if len(self.contraseña_input.text) < 8:
            self.mostrar_mensaje("contraseña débil", "La contraseña debe tener al menos 8 caracteres")
            self.contraseña_input.text = ""
            self.confirmar_contraseña_input.text = ""
            self.contraseña_input.focus = True
            return

        
        self.mostrar_mensaje(
            "¡Registro exitoso!",
            f"Bienvenido {self.nombre_input.text} {self.Apellidos_input.text}\nTu cuenta ha sido creada con éxito"
        )

      
        for campo in [self.nombre_input, self.Apellidos_input, self.usuario_input,
                      self.correo_input, self.contraseña_input, self.confirmar_contraseña_input]:
            campo.text = ""

    def volver(self, instance):
        self.manager.current = 'main'


class RegistroApp(App):
    def build(self):
        from kivy.uix.screenmanager import ScreenManager
        sm = ScreenManager()
        sm.add_widget(RegistroScreen(name='registro'))
        return sm


if __name__ == '__main__':
    RegistroApp().run()