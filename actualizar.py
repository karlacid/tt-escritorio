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
from kivy.metrics import dp, sp
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView


class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Configuración mejorada
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
class ActualizarDatosScreen(Screen):
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

        # Contenedor del formulario
        form_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            spacing=dp(12),
            padding=[dp(50), dp(50)],
            pos_hint={'center_x': 0.5}
        )
        form_container.bind(minimum_height=form_container.setter('height'))

        # Título
        titulo = Label(
            text='ACTUALIZAR DATOS',
            font_size=dp(32),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )
        form_container.add_widget(titulo)

        # Función para crear campos editables
        def crear_campo_editable(texto, valor_actual):
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
                text=valor_actual,
                size_hint_y=None,
                height=dp(55)
            )
            campo_layout.add_widget(input_field)

            return campo_layout, input_field

        # Campos editables (con datos actuales del usuario)
        campos_edicion = [
            ('Nombre', 'Juan'),
            ('Apellidos', 'Pérez'),
            ('Usuario', 'juanito123'),
            ('Correo', 'juan@example.com'),
            ('Nueva Contraseña', '', True)
        ]

        # Añadir campos al formulario
        for texto, valor, *resto in campos_edicion:
            is_password = resto[0] if resto else False
            layout, input_field = crear_campo_editable(texto, valor)
            if is_password:
                input_field.password = True
            attr_name = texto.lower().replace(" ", "_") + "_input"
            setattr(self, attr_name, input_field)
            form_container.add_widget(layout)

        # Espaciador
        form_container.add_widget(Widget(size_hint_y=None, height=dp(10)))

        # Contenedor de botones
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50),
            padding=[0, dp(10), 0, 0]
        )

        # Botón Guardar Cambios
        btn_guardar = HoverButton(text='GUARDAR CAMBIOS')
        btn_guardar.bind(on_press=self.guardar_cambios)
        botones_layout.add_widget(btn_guardar)

        # Botón Cancelar
        btn_cancelar = HoverButton(
            text='CANCELAR',
            background_color=(0.7, 0.1, 0.1, 1)
        )
        btn_cancelar.bind(on_press=self.cancelar)
        botones_layout.add_widget(btn_cancelar)

        form_container.add_widget(botones_layout)
        scroll_view.add_widget(form_container)
        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

    def update_background(self, *args):
        self.background_rect.size = Window.size
        self.background_rect.pos = self.pos

    def on_enter(self, *args):

        Clock.schedule_once(self.establecer_foco, 0.1)

    def establecer_foco(self, dt):
        self.nombre_input.focus = True

    def guardar_cambios(self, instance):
        """Validar y guardar los cambios realizados"""
        # Validar campos obligatorios
        campos_obligatorios = [
            (self.nombre_input, "El nombre es obligatorio"),
            (self.Apellidos_input, "El Apellidos es obligatorio"),
            (self.correo_input, "El correo es obligatorio")
        ]

        errores = []
        for campo, mensaje in campos_obligatorios:
            if not campo.text.strip():
                errores.append(mensaje)

        # Validar formato de correo
        if "@" not in self.correo_input.text or "." not in self.correo_input.text:
            errores.append("El correo electrónico no es válido")

        # Validar contraseña si se ingresó una nueva
        if self.nueva_contraseña_input.text:
            if len(self.nueva_contraseña_input.text) < 8:
                errores.append("La contraseña debe tener al menos 8 caracteres")

        if errores:
            self.mostrar_errores(errores)
            return

        datos_actualizados = {
            'nombre': self.nombre_input.text,
            'Apellidos': self.Apellido_input.text,
            'usuario': self.usuario_input.text,
            'correo': self.correo_input.text,
            'contraseña': self.nueva_contraseña_input.text if self.nueva_contraseña_input.text else None
        }


        self.mostrar_mensaje("Éxito", "Tus datos se han actualizado correctamente")
        self.manager.current = 'cuenta'

    def cancelar(self, instance):
        self.manager.current = 'cuenta'

    def mostrar_errores(self, errores):
        """Mostrar popup de errores con estilo azul consistente (CORREGIDO)"""
        content = ScrollView()
        lista_campos = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20), size_hint_y=None)
        lista_campos.bind(minimum_height=lista_campos.setter('height'))

        titulo_label = Label(
            text='Campos Obligatorios Faltantes:',
            font_size=sp(20),
            color=(0.1, 0.4, 0.7, 1), # Azul principal
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        lista_campos.add_widget(titulo_label)

        for mensaje in errores:
            label_campo = Label(
                text=f"• {mensaje}",
                font_size=sp(18),
                color=(0.1, 0.1, 0.2, 1), # Un tono más oscuro
                size_hint_y=None,
                height=dp(30)
            )
            lista_campos.add_widget(label_campo)

        btn_cerrar = Button(
            text='CERRAR',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.1, 0.4, 0.7, 0.9), # Azul principal (normal)
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))
        lista_campos.add_widget(btn_cerrar)
        content.add_widget(lista_campos)

        popup = Popup(
            title='¡Atención!',
            title_color=(0.1, 0.4, 0.7, 1), # Azul principal
            title_size=sp(22),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=(dp(500), dp(400)),
            separator_height=0,
            background=''
        )
        btn_cerrar.bind(on_press=popup.dismiss)

        with popup.canvas.before:
            Color(0.1, 0.4, 0.7, 0.9) # Azul principal (normal)
            popup.rect = RoundedRectangle(
                pos=popup.pos,
                size=popup.size,
                radius=[dp(12)]
            )

        def update_popup_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        popup.bind(pos=update_popup_rect, size=update_popup_rect)
        popup.open()

    def mostrar_mensaje(self, titulo, mensaje):
        """Mostrar popup de mensaje con estilo azul consistente (CORREGIDO)"""
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        mensaje_label = Label(
            text=mensaje,
            font_size=sp(20),
            color=(0.1, 0.4, 0.7, 1), # Azul principal
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80))
        content.add_widget(mensaje_label)

        btn_aceptar = Button(
            text='ACEPTAR',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.1, 0.4, 0.7, 0.9), # Azul principal (normal)
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))

        popup = Popup(
            title=titulo,
            title_color=(0.1, 0.4, 0.7, 1), # Azul principal
            title_size=sp(22),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=(dp(450), dp(250)),
            separator_height=0,
            background=''
        )
        btn_aceptar.bind(on_press=popup.dismiss)
        content.add_widget(btn_aceptar)

        with popup.canvas.before:
            Color(0.1, 0.4, 0.7, 0.9) # Azul principal (normal)
            popup.rect = RoundedRectangle(
                pos=popup.pos,
                size=popup.size,
                radius=[dp(12)]
            )

        def update_popup_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        popup.bind(pos=update_popup_rect, size=update_popup_rect)
        popup.open()