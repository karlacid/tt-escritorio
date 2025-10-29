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
from kivy.utils import platform


# ------------------ UTILIDADES RESPONSIVE (COPIADAS DE registro.py) ------------------
class ResponsiveHelper:
    @staticmethod
    def is_mobile():
        return platform in ['android', 'ios']
    
    @staticmethod
    def is_desktop():
        return platform in ['win', 'linux', 'macosx']
    
    @staticmethod
    def get_form_width():
        """Retorna el ancho del formulario según el tamaño de ventana"""
        width = Window.width
        if width < 600:
            return 0.95  # 95% en pantallas muy pequeñas
        elif width < 900:
            return 0.85  # 85% en pantallas pequeñas
        elif width < 1200:
            return 0.7   # 70% en pantallas medianas
        else:
            return 0.6   # 60% en pantallas grandes
    
    @staticmethod
    def get_font_size(base_size):
        """Retorna tamaño de fuente responsive"""
        width = Window.width
        if width < 600:
            return sp(base_size * 0.7)
        elif width < 900:
            return sp(base_size * 0.85)
        return sp(base_size)
    
    @staticmethod
    def get_popup_size():
        """Retorna tamaño apropiado para popups"""
        width = Window.width
        height = Window.height
        if width < 600:
            return (width * 0.9, min(height * 0.5, dp(400)))
        else:
            return (min(width * 0.7, dp(500)), min(height * 0.5, dp(400)))
    
    @staticmethod
    def get_logo_height():
        """Retorna altura del logo responsive"""
        width = Window.width
        height = Window.height
        if width < 600:
            return dp(80)
        elif width < 900:
            return dp(100)
        return min(dp(120), height * 0.12)
    
    @staticmethod
    def get_button_layout_orientation():
        """Retorna orientación de botones según tamaño de ventana"""
        return 'horizontal' if Window.width > 600 else 'vertical'
    
    @staticmethod
    def get_button_layout_height():
        """Retorna altura del contenedor de botones"""
        return dp(50) if Window.width > 600 else dp(110)


# ------------------ TEXT INPUT REDONDEADO RESPONSIVE Y AZUL ------------------
class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Configuración mejorada y responsive
        self.background_normal = ""
        self.background_active = ""
        self.background_color = (0, 0, 0, 0)  
        self.multiline = False
        self.size_hint_y = None
        self.height = dp(55)  
        self.padding = [dp(15), dp(15), dp(15), dp(15)]  
        self.font_size = ResponsiveHelper.get_font_size(18)  
        self.color = (1, 1, 1, 1)  
        self.hint_text_color = (0.9, 0.9, 0.9, 0.8)  
        self.cursor_color = (1, 1, 1, 1) 
        self.selection_color = (0.2, 0.6, 1, 0.5)  
        self.bold = True  

       
        with self.canvas.before:
            Color(0.1, 0.4, 0.7, 0.9) # Azul principal

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
                radius=[dp(10)]
            )

        self.bind(pos=self._update_rects, size=self._update_rects)
        Window.bind(on_resize=self.on_window_resize)

    def _update_rects(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_rect.pos = (self.pos[0]+dp(2), self.pos[1]+dp(2))
        self.border_rect.size = (self.size[0]-dp(4), self.size[1]-dp(4))
    
    def on_window_resize(self, instance, width, height):
        self.font_size = ResponsiveHelper.get_font_size(18)
        self.height = dp(55)

    def on_focus(self, instance, value):
        if value:
            # Estado activo
            self.canvas.before.clear()
            with self.canvas.before:
                Color(0.2, 0.5, 0.9, 1) # Azul más claro al enfocar
                self.bg_rect = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[dp(12)]
                )
                Color(1, 1, 1, 0.5)
                self.border_rect = RoundedRectangle(
                    pos=(self.pos[0]+dp(2), self.pos[1]+dp(2)),
                    size=(self.size[0]-dp(4), self.size[1]-dp(4)),
                    radius=[dp(10)]
                )
        else:
            # Estado normal
            self.canvas.before.clear()
            with self.canvas.before:
                Color(0.1, 0.4, 0.7, 0.9) # Azul principal
                self.bg_rect = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[dp(12)]
                )
                Color(1, 1, 1, 0.3)
                self.border_rect = RoundedRectangle(
                    pos=(self.pos[0]+dp(2), self.pos[1]+dp(2)),
                    size=(self.size[0]-dp(4), self.size[1]-dp(4)),
                    radius=[dp(10)]
                )
            self._update_rects() # Asegura que la geometría se actualice al perder el foco


# ------------------ BOTÓN HOVER RESPONSIVE Y AZUL ------------------
class HoverButton(Button):
    def __init__(self, **kwargs):
        # Extraer background_color (o usar default azul)
        bg_color = kwargs.pop('background_color', (0.1, 0.4, 0.7, 1))
        
        super().__init__(**kwargs)
        
        self.background_normal = ''
        self.background_color = bg_color # Usar el color provisto o el default
        self.color = (1, 1, 1, 1)
        self.size_hint_y = None
        self.height = dp(50)
        self.font_size = ResponsiveHelper.get_font_size(18)
        self.bold = True
        self.border_radius = dp(12)

        with self.canvas.before:
            Color(*self.background_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.border_radius])

        self.bind(pos=self.update_rect, size=self.update_rect)
        Window.bind(on_resize=self.on_window_resize)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_window_resize(self, instance, width, height):
        self.font_size = ResponsiveHelper.get_font_size(18)
        self.height = dp(50)


# ------------------ PANTALLA ACTUALIZAR DATOS RESPONSIVE ------------------
class ActualizarDatosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        Window.bind(on_resize=self.on_window_resize)

    def build_ui(self):
        self.clear_widgets()
        
        # Layout principal
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(10), dp(20), dp(10)],
            spacing=dp(10)
        )

        # Fondo gris claro
        with main_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.background_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self.update_background, pos=self.update_background)

        # Logo responsive centrado
        logo_height = ResponsiveHelper.get_logo_height()
        logo_container = BoxLayout(size_hint=(1, None), height=logo_height)
        logo = Image(
            source="Imagen5-Photoroom.png",
            size_hint=(None, None),
            width=logo_height * 1.2,
            height=logo_height,
            pos_hint={'center_x': 0.5},
            fit_mode="contain"
        )
        logo_container.add_widget(Widget())
        logo_container.add_widget(logo)
        logo_container.add_widget(Widget())
        main_layout.add_widget(logo_container)

        # ScrollView para el formulario
        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            bar_width=dp(10),
            scroll_type=['bars', 'content']
        )

        # Contenedor para centrar el formulario
        center_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None
        )
        center_container.bind(minimum_height=center_container.setter('height'))
        
        # Contenedor del formulario centrado y responsive
        form_container = BoxLayout(
            orientation='vertical',
            size_hint=(ResponsiveHelper.get_form_width(), None),
            spacing=dp(12),
            padding=[dp(20), dp(20)],
            pos_hint={'center_x': 0.5}
        )
        form_container.bind(minimum_height=form_container.setter('height'))

        # Título
        titulo = Label(
            text='ACTUALIZAR DATOS',
            font_size=ResponsiveHelper.get_font_size(32),
            color=(0.1, 0.4, 0.7, 1),
            bold=True,
            size_hint_y=None,
            height=dp(60),
            halign='center',
            valign='middle'
        )
        form_container.add_widget(titulo)

        # Función para crear campos editables
        def crear_campo_editable(texto, valor_actual):
            campo_layout = BoxLayout(
                orientation='vertical',
                spacing=dp(5),
                size_hint_y=None,
                size_hint_x=1
            )
            campo_layout.bind(minimum_height=campo_layout.setter('height'))

            campo_layout.add_widget(Label(
                text=texto,
                font_size=ResponsiveHelper.get_font_size(18),
                color=(0.1, 0.1, 0.2, 1),
                size_hint_y=None,
                size_hint_x=1,
                height=dp(30),
                halign='left'
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
            
            # Nombres de atributos en minúsculas y sin acentos para consistencia
            attr_name = texto.lower().replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u") + "_input"
            setattr(self, attr_name, input_field)
            form_container.add_widget(layout)

        # Espaciador
        form_container.add_widget(Widget(size_hint_y=None, height=dp(10)))

        # Contenedor de botones responsive
        botones_layout = BoxLayout(
            orientation=ResponsiveHelper.get_button_layout_orientation(),
            spacing=dp(15),
            size_hint_y=None,
            size_hint_x=1,
            height=ResponsiveHelper.get_button_layout_height()
        )

        # Botón Guardar Cambios
        btn_guardar = HoverButton(
            text='GUARDAR CAMBIOS',
            background_color=(0.1, 0.4, 0.7, 1) # Azul principal
        )
        btn_guardar.bind(on_press=self.guardar_cambios)
        botones_layout.add_widget(btn_guardar)

        # Botón Cancelar
        btn_cancelar = HoverButton(
            text='CANCELAR',
            background_color=(0.7, 0.1, 0.1, 1) # Rojo
        )
        btn_cancelar.bind(on_press=self.cancelar)
        
        # Actualizar canvas del botón Cancelar para el color rojo
        btn_cancelar.canvas.before.clear()
        with btn_cancelar.canvas.before:
            Color(0.7, 0.1, 0.1, 1)
            btn_cancelar.rect = RoundedRectangle(
                pos=btn_cancelar.pos,
                size=btn_cancelar.size,
                radius=[btn_cancelar.border_radius]
            )

        botones_layout.add_widget(btn_cancelar)

        form_container.add_widget(botones_layout)
        
        # Espaciador final
        form_container.add_widget(Widget(size_hint_y=None, height=dp(20)))

        center_container.add_widget(form_container)
        scroll_view.add_widget(center_container)
        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

    def update_background(self, instance, value):
        self.background_rect.size = instance.size
        self.background_rect.pos = instance.pos
        
    def on_window_resize(self, instance, width, height):
        # Reconstruir la UI para aplicar cambios de tamaño y disposición
        Clock.schedule_once(lambda dt: self.build_ui(), 0.1)

    def on_enter(self, *args):
        Clock.schedule_once(self.establecer_foco, 0.1)

    def establecer_foco(self, dt):
        if hasattr(self, 'nombre_input'):
            self.nombre_input.focus = True

    def guardar_cambios(self, instance):
        """Validar y guardar los cambios realizados"""
        # Validar campos obligatorios
        # Nota: Los atributos ahora son en minúsculas y sin acentos (ej. self.apellidos_input)
        campos_obligatorios = [
            (self.nombre_input, "El nombre es obligatorio"),
            (self.apellidos_input, "El Apellido es obligatorio"), # Se corrigió la tipografía en el nombre del atributo
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
            'apellidos': self.apellidos_input.text, # Corregido de Apellido_input a apellidos_input
            'usuario': self.usuario_input.text,
            'correo': self.correo_input.text,
            'contraseña': self.nueva_contraseña_input.text if self.nueva_contraseña_input.text else None
        }

        # Simulación de guardado...
        self.mostrar_mensaje("Éxito", "Tus datos se han actualizado correctamente")
        
        # Limpiar campo de contraseña después de la actualización exitosa
        self.nueva_contraseña_input.text = ""
        
        self.manager.current = 'cuenta'

    def cancelar(self, instance):
        self.manager.current = 'cuenta'

    def mostrar_errores(self, errores):
        """Mostrar popup de errores con estilo azul consistente"""
        scroll_content = ScrollView(size_hint=(1, 1))
        lista_campos = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20), size_hint_y=None)
        lista_campos.bind(minimum_height=lista_campos.setter('height'))

        titulo_label = Label(
            text='Errores de Validación:',
            font_size=ResponsiveHelper.get_font_size(20),
            color=(0.5, 0.8, 1, 1), # Azul claro
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        lista_campos.add_widget(titulo_label)

        for mensaje in errores:
            label_campo = Label(
                text=f"• {mensaje}",
                font_size=ResponsiveHelper.get_font_size(16),
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=dp(35),
                halign='left'
            )
            label_campo.bind(size=label_campo.setter('text_size'))
            lista_campos.add_widget(label_campo)

        lista_campos.add_widget(Widget(size_hint_y=None, height=dp(10)))

        btn_cerrar = Button(
            text='CERRAR',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1), # Azul para el botón
            color=(1, 1, 1, 1),
            bold=True,
            font_size=ResponsiveHelper.get_font_size(18))
        lista_campos.add_widget(btn_cerrar)
        scroll_content.add_widget(lista_campos)

        popup_size = ResponsiveHelper.get_popup_size()
        popup = Popup(
            title='¡Atención!',
            title_color=(1, 1, 1, 1), # Color del título blanco
            title_size=ResponsiveHelper.get_font_size(22),
            title_align='center',
            content=scroll_content,
            size_hint=(None, None),
            size=popup_size,
            separator_height=0,
            background=''
        )
        btn_cerrar.bind(on_press=popup.dismiss)

        with popup.canvas.before:
            Color(0.1, 0.4, 0.7, 1) # Azul de fondo del popup
            popup.rect = RoundedRectangle(
                pos=popup.pos,
                size=popup.size,
                radius=[dp(15)]
            )

        def update_popup_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        popup.bind(pos=update_popup_rect, size=update_popup_rect)
        popup.open()

    def mostrar_mensaje(self, titulo, mensaje):
        """Mostrar popup de mensaje con estilo azul consistente"""
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        mensaje_label = Label(
            text=mensaje,
            font_size=ResponsiveHelper.get_font_size(18),
            color=(0.5, 0.8, 1, 1), # Azul claro
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80))
        mensaje_label.bind(size=mensaje_label.setter('text_size'))
        content.add_widget(mensaje_label)

        btn_aceptar = Button(
            text='ACEPTAR',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1), # Azul para el botón
            color=(1, 1, 1, 1),
            bold=True,
            font_size=ResponsiveHelper.get_font_size(18))

        popup_size = ResponsiveHelper.get_popup_size()
        popup = Popup(
            title=titulo,
            title_color=(1, 1, 1, 1), # Color del título blanco
            title_size=ResponsiveHelper.get_font_size(22),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=popup_size,
            separator_height=0,
            background=''
        )
        btn_aceptar.bind(on_press=popup.dismiss)
        content.add_widget(btn_aceptar)

        with popup.canvas.before:
            Color(0.1, 0.4, 0.7, 1) # Azul de fondo del popup
            popup.rect = RoundedRectangle(
                pos=popup.pos,
                size=popup.size,
                radius=[dp(15)]
            )

        def update_popup_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        popup.bind(pos=update_popup_rect, size=update_popup_rect)
        popup.open()