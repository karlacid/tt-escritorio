from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.popup import Popup
from kivy.metrics import dp, sp
from kivy.properties import StringProperty

class ResponsiveDataDisplay(BoxLayout):
    text = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = [dp(15), dp(10)]
        self.spacing = dp(5)
        
        # Fondo azul con bordes redondeados
        with self.canvas.before:
            Color(0.2, 0.6, 1,0.5)  # Azul sólido
            self.rect = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=[dp(10)],
                width=dp(400),
            )
        
        # Label para mostrar el texto
        self.label = Label(
            text=self.text,
            font_size=dp(20),
            color=(1, 1, 1, 1),
            halign='left',
            valign='middle',
            size_hint_y=None,
            padding=[dp(10), dp(10)],
            bold=True,
            text_size=(None, None)
        )
        
        self.add_widget(self.label)
        self.bind(
            size=self._update_rect,
            pos=self._update_rect,
            text=self._update_text
        )
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.height = self.label.texture_size[1] + dp(30)
    
    def _update_text(self, instance, value):
        self.label.text = value
        self.label.texture_update()
        self.height = self.label.texture_size[1] + dp(30)

class HoverButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.1, 0.4, 0.7, 1)
        self.color = (1, 1, 1, 1)
        self.bold = True
        self.font_size = dp(18)

class VerInfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=[dp(20), dp(10)], spacing=dp(10))
        
        # Fondo de la pantalla
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

        # ScrollView para el contenido
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
            spacing=dp(15),  # Más espacio entre elementos
            padding=[dp(40), dp(40)],  # Padding reducido para más espacio
            pos_hint={'center_x': 0.5}
        )
        form_container.bind(minimum_height=form_container.setter('height'))

        # Título
        titulo = Label(
            text='MI PERFIL',
            font_size=dp(32),
            color=(0.1, 0.4, 0.7, 1),
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )
        form_container.add_widget(titulo)

        # Función para crear campos
        def crear_campo(etiqueta, valor):
            campo_layout = BoxLayout(
                orientation='vertical',
                spacing=dp(8),  # Más espacio entre etiqueta y recuadro
                size_hint_y=None,
                height=dp(100)  # Altura inicial suficiente
            )

            # Etiqueta del campo
            lbl_etiqueta = Label(
                text=etiqueta,
                font_size=dp(18),
                color=(0.1, 0.1, 0.2, 1),
                size_hint_y=None,
                height=dp(30),  # Altura fija para etiquetas
                bold=True,
                halign='left'
            )
            campo_layout.add_widget(lbl_etiqueta)

            # Display de datos responsivo
            data_display = ResponsiveDataDisplay(text=valor)
            campo_layout.add_widget(data_display)
            
            return campo_layout, data_display

        # Campos de información
        campos_info = [
            ('Nombre(s)', 'Karla'),
            ('Apellidos', 'Cid Martínez'),
            ('Usuario', 'kcidm'),
            ('Correo', 'karla@example.com')
        ]

        for etiqueta, valor in campos_info:
            layout, display = crear_campo(etiqueta, valor)
            attr_name = etiqueta.lower().replace(" ", "_") + "_display"
            setattr(self, attr_name, display)
            form_container.add_widget(layout)

        # Espaciador
        form_container.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Botones
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(55))
        

        btn_actualizar = HoverButton(text='ACTUALIZAR')
        btn_actualizar.bind(on_press=self.actualizar_datos)

        btn_volver = HoverButton(text='VOLVER')
        btn_volver.bind(on_press=self.volver)

        botones_layout.add_widget(btn_actualizar)
        botones_layout.add_widget(btn_volver)
        form_container.add_widget(botones_layout)

        scroll_view.add_widget(form_container)
        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

    def update_background(self, *args):
        self.background_rect.size = Window.size
        self.background_rect.pos = self.pos

    def actualizar_datos(self, instance):
        self.manager.current = 'actualizar'
    def volver(self, instance):
        self.manager.current = 'ini'

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
                radius=[dp(15)]
            )

        def update_popup_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        popup.bind(pos=update_popup_rect, size=update_popup_rect)
        btn_aceptar.bind(on_press=popup.dismiss)
        content.add_widget(btn_aceptar)
        popup.open()