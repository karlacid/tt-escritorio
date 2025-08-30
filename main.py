from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
import webbrowser
from kivy.uix.spinner import Spinner
from registro import RegistroScreen
from torneos_anteriores import TorneosAnterioresScreen
from crear_torneo import CrearTorneoScreen
from crear_combate import CrearCombateScreen
from tablero import MainScreentab
from tablero_central import MainScreentabc
from combates_anteriore import CombatesScreen
from inicio import InicioSesionScreen
from ini import MainInAuthScreen
from ini_juez import InicioSesionJuezScreen
from cuenta import VerInfoScreen
from actualizar_torneos import ActualizarTorneoScreen
from actualizar import ActualizarDatosScreen

class HoverButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_background_color = (0.1, 0.4, 0.7, 1)
        self.hover_background_color = (0.2, 0.5, 0.9, 1)
        self.background_color = self.original_background_color
        self.size_hint_y = None
        self.height = 50
        self.font_size = 18
        self.color = (1, 1, 1, 1)
        self.border_radius = 25

        with self.canvas.before:
            Color(*self.original_background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[self.border_radius])
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.rect.radius = [self.border_radius]

class Navbar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (.2, 1)
        self.orientation = "vertical"
        self.padding = [20, 20]
        self.spacing = 10

        with self.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        self.logo = Image(source="Imagen5-Photoroom.png", size_hint=(1, None), height=150)
        self.add_widget(self.logo)

        self.botones_navbar = BoxLayout(orientation="vertical", spacing=10)

        menu_items = [
            ("Manual de usuario", self.descargar_manual),
            ("Contáctanos", self.enviar_correo),
            ("Conócenos", self.ir_a_conocenos),
        ]

        for text, action in menu_items:
            boton = HoverButton(text=text)
            boton.bind(on_press=action)
            self.botones_navbar.add_widget(boton)

        self.add_widget(self.botones_navbar)

        empty_widget = Widget(size_hint_y=1)
        self.add_widget(empty_widget)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def descargar_manual(self, instance):
        webbrowser.open("ilovepdf_merged (2)[1].pdf")

    def enviar_correo(self, instance):
        webbrowser.open("mailto:karlycid0925@gmail.com")

    def ir_a_conocenos(self, instance):
        App.get_running_app().root.current = 'conocenos'

class ConocenosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 0])
        self.navbar = Navbar()
        main_layout.add_widget(self.navbar)

        # Contenido principal
        content_layout = BoxLayout(orientation='vertical', spacing=0, padding=[0, 0], size_hint=(.8, 1))

        with content_layout.canvas.before:
            Color(0.98, 0.98, 0.98, 1)
            self.background_rect = Rectangle(size=content_layout.size, pos=content_layout.pos)

        content_layout.bind(size=self.update_background_rect, pos=self.update_background_rect)

        # ScrollView para contenido extenso
        from kivy.uix.scrollview import ScrollView
        scroll_view = ScrollView(
            size_hint=(1, 1), 
            do_scroll_x=False,
            bar_width=10,
            scroll_type=['bars', 'content']
        )
        
        # Layout principal dentro del ScrollView
        main_content = BoxLayout(
            orientation='vertical', 
            spacing=30, 
            padding=[20, 20], 
            size_hint_y=None,
            size_hint_x=1
        )
        main_content.bind(
            minimum_height=main_content.setter('height'),
            width=lambda mc, val: setattr(mc, 'width', val)
        )

        # Título principal con altura fija adecuada
        titulo = Label(
            text='[b]CONÓCENOS[/b]',
            font_size=42,
            markup=True,
            color=(0.1, 0.3, 0.6, 1),
            size_hint_y=None,
            height=100,
            halign='center',
            valign='middle'
        )
        main_content.add_widget(titulo)

        # Separador visual
        from kivy.uix.behaviors import ButtonBehavior
        class Separator(ButtonBehavior, Widget):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.size_hint_y = None
                self.height=5
                with self.canvas:
                    Color(0.1, 0.4, 0.7, 0.6)
                    self.rect = Rectangle(size=self.size, pos=self.pos)
                self.bind(size=self._update_rect, pos=self._update_rect)
            
            def _update_rect(self, *args):
                self.rect.size = self.size
                self.rect.pos = self.pos

        main_content.add_widget(Separator())

        # Función para crear secciones con alturas bien definidas
        def crear_seccion(titulo_seccion, contenido, color_titulo=(0.1, 0.4, 0.7, 0.6)):
            container = BoxLayout(
                orientation='vertical', 
                size_hint_y=None,
                spacing=0,
                padding=[0, 0, 0, 30]
            )
            
            with container.canvas.before:
                Color(0.95, 0.95, 0.95, 1)
                container.rect = RoundedRectangle(
                    size=container.size,
                    pos=container.pos,
                    radius=[15]
                )
            container.bind(
                size=lambda c, val: setattr(c.rect, 'size', val),
                pos=lambda c, val: setattr(c.rect, 'pos', val))
            
            seccion = BoxLayout(
                orientation='vertical', 
                spacing=20,
                size_hint_y=None,
                padding=[30, 30]
            )
            
            # Título de sección con altura fija adecuada
            lbl_titulo = Label(
                text=f'[b]{titulo_seccion}[/b]',
                font_size=28,
                markup=True,
                color=color_titulo,
                size_hint_y=None,
                height=70,
                halign='center',
                valign='middle'
            )
            seccion.add_widget(lbl_titulo)
            
            # Contenido con altura calculada dinámicamente
            lbl_contenido = Label(
                text=contenido,
                font_size=20,
                color=(0.2, 0.2, 0.2, 1),
                size_hint_y=80,
                halign='center',
                valign='top',
                text_size=(content_layout.width * 0.8, 0.8),
                padding=(10, 10))
            
            # Función para calcular altura del texto
            def update_text_height(lbl, *args):
                lbl.texture_update()
                if lbl.texture:
                    lbl.height = max(lbl.texture.height + 50, 100)
            
            lbl_contenido.bind(
                texture_size=update_text_height,
                width=lambda lbl, val: setattr(lbl, 'text_size', (val * 0.8, None)))
            
            seccion.add_widget(lbl_contenido)
            
            # Establecer altura mínima para la sección
            def update_section_height(sec, *args):
                sec.height = lbl_titulo.height + lbl_contenido.height + 60
            
            seccion.bind(height=update_section_height)
            
            container.add_widget(seccion)
            
            # Establecer altura del contenedor
            container.height = seccion.height + 30
            
            return container

        # Sección Misión
        mision = crear_seccion(
            "MISIÓN",
            "En Peto Tech nos dedicamos a desarrollar soluciones tecnológicas innovadoras para la gestión de torneos deportivos. Nuestra plataforma facilita la organización, seguimiento y análisis de combates, ofreciendo herramientas intuitivas para atletas, entrenadores y organizadores.",
            (0.1, 0.4, 0.7, 0.6)
        )
        main_content.add_widget(mision)

        # Sección Visión
        vision = crear_seccion(
            "VISIÓN",
            "Aspiramos a ser reconocidos como líderes en software deportivo, destacando por nuestra innovación, calidad y compromiso con nuestros usuarios. Buscamos transformar la experiencia de gestión deportiva mediante tecnología accesible y de alto rendimiento.",
            (0.1, 0.4, 0.7, 0.6)
        )
        main_content.add_widget(vision)

        # Galería de imágenes del equipo con altura fija adecuada
        gallery_title = Label(
            text="[b]CONOCE A NUESTRO EQUIPO[/b]",
            font_size=24,
            markup=True,
            color=(0.1, 0.3, 0.6, 1),
            size_hint_y=None,
            height=80,
            halign='center'
        )
        main_content.add_widget(gallery_title)

        from kivy.uix.anchorlayout import AnchorLayout

        # Contenedor que centrará nuestro grid horizontal
        img_container = AnchorLayout(
            anchor_x='center',
            size_hint_y=None,
            height=300
        )

        # Grid horizontal para las tarjetas
        img_grid = BoxLayout(
            orientation='horizontal',
            spacing=20,
            size_hint=(None, 1),
            padding=[0, 20]
        )
        img_grid.bind(minimum_width=img_grid.setter('width'))

        # Clase para tarjetas de equipo (modificada)
        class TeamCard(BoxLayout):
            def __init__(self, image_path, name, role, **kwargs):
                super().__init__(
                    orientation='vertical', 
                    spacing=5, 
                    size_hint=(None, None),
                    size=(200, 250),
                    padding=[10, 10],
                    **kwargs
                )
                
                with self.canvas.before:
                    Color(0.9, 0.9, 0.9, 1)
                    self.rect = RoundedRectangle(
                        size=self.size,
                        pos=self.pos,
                        radius=[10]
                    )
                self.bind(
                    size=lambda c, val: setattr(c.rect, 'size', val),
                    pos=lambda c, val: setattr(c.rect, 'pos', val))
                
                # Imagen
                img = Image(
                    source=image_path,
                    size_hint_y=0.7,
                    allow_stretch=True,
                    keep_ratio=True
                )
                self.add_widget(img)
                
                # Nombre(s)
                lbl_name = Label(
                    text=f'[b]{name}[/b]',
                    markup=True,
                    color=(0.1, 0.4, 0.7, 1),
                    font_size=16,
                    halign='center'
                )
                self.add_widget(lbl_name)
                
                # Rol
                lbl_role = Label(
                    text=role,
                    color=(0.4, 0.4, 0.4, 1),
                    font_size=14,
                    halign='center'
                )
                self.add_widget(lbl_role)

        # Añadir tarjetas al grid
        img_grid.add_widget(TeamCard("p1-Photoroom.png", "Karla", "x"))
        img_grid.add_widget(TeamCard("p2-Photoroom.png", "Enrique", "x"))
        img_grid.add_widget(TeamCard("p2-Photoroom.png", "Leonardo", "x"))

        # Añadir el grid al contenedor centrado
        img_container.add_widget(img_grid)

        # Añadir el contenedor al contenido principal
        main_content.add_widget(img_container)

        # Botón de regreso
        btn_back = Button(
            text="Volver al Inicio",
            size_hint=(0.4, None),
            height=50,
            pos_hint={'center_x': 0.5},
            background_color=(0.1, 0.4, 0.7, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            bold=True
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        main_content.add_widget(btn_back)

        scroll_view.add_widget(main_content)
        content_layout.add_widget(scroll_view)
        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)

    def update_background_rect(self, instance, value):
        self.background_rect.size = instance.size
        self.background_rect.pos = instance.pos

class MainInScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 0])
        self.navbar = Navbar()
        main_layout.add_widget(self.navbar)

        content_layout = BoxLayout(orientation='vertical', spacing=20, padding=[30, 30], size_hint=(.8, 1))

        with content_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.background_rect = Rectangle(size=content_layout.size, pos=content_layout.pos)

        content_layout.bind(size=self.update_background_rect, pos=self.update_background_rect)

        center_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, None), height=400)
        center_layout.bind(size=self.update_center_layout)

        titulo = Label(
            text='PETO TECH',
            font_size=70,
            color=(0.1, 0.1, 0.2, 1),
            bold=True,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=100,
            text_size=(content_layout.width, None))
        center_layout.add_widget(titulo)

        eslogan = Label(
            text='Tu solución tecnológica para la gestión de torneos de Taekwondo.',
            font_size=24,
            color=(0.1, 0.4, 0.7),
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=50,
            text_size=(content_layout.width, None)
        )
        center_layout.add_widget(eslogan)

        botones_frame = BoxLayout(orientation="horizontal", size_hint_y=None, height=50, spacing=20)

        btn_iniciar_sesion = HoverButton(text="INICIAR SESIÓN")
        btn_iniciar_sesion.bind(on_press=self.ir_a_inicio_sesion)
        botones_frame.add_widget(btn_iniciar_sesion)

        btn_registrarse = HoverButton(text="REGISTRARSE")
        btn_registrarse.bind(on_press=self.ir_a_registro)
        botones_frame.add_widget(btn_registrarse)

        center_layout.add_widget(botones_frame)
        
        # Botón modificado para acceso juez
        btn_tengo_contraeña = HoverButton(
            text="ACCESO JUEZ",
            size_hint=(None, None),
            size=(500, 40),
            pos_hint={'center_x': 0.5}
        )
        btn_tengo_contraeña.bind(on_press=lambda x: setattr(App.get_running_app().root, 'current', 'ini_juez'))
        center_layout.add_widget(btn_tengo_contraeña)

        quienes_somos = Label(
            text="Somos un equipo dedicado a ofrecer soluciones tecnológicas innovadoras para el deporte.",
            font_size=18,
            color=(0.1, 0.1, 0.1, 1),
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=60,
            text_size=(content_layout.width, None)
        )
        center_layout.add_widget(quienes_somos)

        content_layout.add_widget(center_layout)

        im_frame = BoxLayout(orientation="horizontal", size_hint_y=None, height=350, spacing=20)
        self.i1 = Image(source="p1-Photoroom.png", size_hint_x=(1), height=350)
        im_frame.add_widget(self.i1)
        self.i2 = Image(source="p2-Photoroom.png", size_hint_x=(1), height=350)
        im_frame.add_widget(self.i2)
        center_layout.add_widget(im_frame)

        copyright = Label(
            text="Copyright © 2025 - PetoTech System",
            font_size=15,
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            halign="center")
        
        content_layout.add_widget(copyright)

        def update_text_size(instance, value):
            titulo.text_size = (content_layout.width, None)
            eslogan.text_size = (content_layout.width, None)
            quienes_somos.text_size = (content_layout.width, None)

        content_layout.bind(width=update_text_size)

        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)

    def update_background_rect(self, instance, value):
        self.background_rect.size = instance.size
        self.background_rect.pos = instance.pos

    def update_center_layout(self, instance, value):
        instance.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

    def ir_a_inicio_sesion(self, instance):
        self.manager.current = 'inicio_sesion'

    def ir_a_registro(self, instance):
        self.manager.current = 'registro'

class MyApp(App):
    def build(self):
       
        sm = ScreenManager()
        sm.add_widget(MainInScreen(name='main'))
        sm.add_widget(ConocenosScreen(name='conocenos'))
        sm.add_widget(InicioSesionScreen(name='inicio_sesion'))
        sm.add_widget(RegistroScreen(name='registro'))
        sm.add_widget(TorneosAnterioresScreen(name='torneos_anteriores'))
        sm.add_widget(CrearTorneoScreen(name='crear_torneo'))
        sm.add_widget(CrearCombateScreen(name='crear_combate'))
        sm.add_widget(MainScreentab(name='visualizar_combate'))
        sm.add_widget(MainScreentabc(name='visualizar_tablero_central'))
        sm.add_widget(MainInAuthScreen(name='ini'))
        sm.add_widget(InicioSesionJuezScreen(name='ini_juez'))
        sm.add_widget(VerInfoScreen(name='cuenta'))
        sm.add_widget(ActualizarDatosScreen(name='actualizar'))
        sm.add_widget(CombatesScreen(name='combates_anteriores'))

        return sm

if __name__ == '__main__':
    MyApp().run()