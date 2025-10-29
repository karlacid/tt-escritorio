from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.utils import platform
from kivy.clock import Clock

# ------------------ UTILIDADES RESPONSIVE ------------------
class ResponsiveHelper:
    @staticmethod
    def is_mobile():
        return platform in ['android', 'ios']
    
    @staticmethod
    def is_desktop():
        return platform in ['win', 'linux', 'macosx']
    
    @staticmethod
    def get_font_size(base_size):
        """Retorna tamaño de fuente responsive"""
        width = Window.width
        height = Window.height
        # Para pantallas muy pequeñas
        if width < 600 or height < 400:
            return sp(base_size * 0.5)
        # Para pantallas pequeñas
        elif width < 900 or height < 600:
            return sp(base_size * 0.7)
        # Para pantallas medianas
        elif width < 1200:
            return sp(base_size * 0.85)
        # Para pantallas grandes
        return sp(base_size)
    
    @staticmethod
    def get_layout_orientation():
        """Determina si el layout debe ser vertical u horizontal"""
        width = Window.width
        height = Window.height
        # Si es más alto que ancho o muy pequeño, usar vertical
        if height > width or width < 800:
            return 'vertical'
        return 'horizontal'
    
    @staticmethod
    def get_spacing():
        """Retorna espaciado responsive"""
        width = Window.width
        if width < 600:
            return dp(5)
        elif width < 900:
            return dp(10)
        return dp(15)
    
    @staticmethod
    def get_padding():
        """Retorna padding responsive"""
        width = Window.width
        if width < 600:
            return dp(5)
        elif width < 900:
            return dp(8)
        return dp(10)


# ------------------ PANEL DE COMPETIDOR CON PUNTAJE ------------------
class CompetitorPanel(BoxLayout):
    score = NumericProperty(0)
    penalty_score = NumericProperty(0)

    def __init__(self, name, color, nationality="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.name = name
        self.bg_color = color
        self.nationality = nationality
        
        self.update_layout()
        Window.bind(on_resize=self.on_window_resize)
        
        # Vincular cambios en score para actualizar el label
        self.bind(score=self.update_score_label)

    def update_layout(self):
        self.clear_widgets()
        self.spacing = ResponsiveHelper.get_spacing()
        self.padding = ResponsiveHelper.get_padding()

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        # Espaciador superior
        self.add_widget(Label(size_hint_y=0.15))

        # Nacionalidad
        if self.nationality:
            nationality_label = Label(
                text=self.nationality.upper(),
                font_size=ResponsiveHelper.get_font_size(20),
                bold=True,
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=dp(30)
            )
            self.add_widget(nationality_label)

        # Nombre del competidor
        name_label = Label(
            text=self.name,
            font_size=ResponsiveHelper.get_font_size(30),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(50)
        )
        self.add_widget(name_label)

        # Espaciador
        self.add_widget(Label(size_hint_y=0.1))

        # Etiqueta "PUNTAJE"
        puntaje_label = Label(
            text="PUNTAJE",
            font_size=ResponsiveHelper.get_font_size(18),
            color=(1, 1, 1, 0.9),
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(puntaje_label)

        # Contenedor del puntaje con fondo
        score_container = BoxLayout(
            orientation='vertical',
            size_hint=(0.8, None),
            height=dp(120),
            pos_hint={'center_x': 0.5}
        )

        # Fondo blanco semi-transparente para el puntaje
        with score_container.canvas.before:
            Color(1, 1, 1, 0.2)
            score_container.bg_rect = RoundedRectangle(
                pos=score_container.pos,
                size=score_container.size,
                radius=[dp(15)]
            )
        
        def update_score_bg(instance, value):
            score_container.bg_rect.pos = instance.pos
            score_container.bg_rect.size = instance.size
        
        score_container.bind(pos=update_score_bg, size=update_score_bg)

        # Label del puntaje
        self.score_label = Label(
            text=str(self.score),
            font_size=ResponsiveHelper.get_font_size(80),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=1
        )
        score_container.add_widget(self.score_label)

        self.add_widget(score_container)

        # Espaciador inferior
        self.add_widget(Label(size_hint_y=0.2))

    def update_score_label(self, instance, value):
        if hasattr(self, 'score_label'):
            self.score_label.text = str(value)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_window_resize(self, instance, width, height):
        Clock.schedule_once(lambda dt: self.update_layout(), 0.1)


# ------------------ PANEL CENTRAL RESPONSIVE ------------------
class CenterPanel(BoxLayout):
    time_str = StringProperty("00:00")
    round_str = StringProperty("Round 1")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.update_layout()
        Window.bind(on_resize=self.on_window_resize)

    def update_layout(self):
        self.clear_widgets()
        self.spacing = ResponsiveHelper.get_spacing()
        self.padding = ResponsiveHelper.get_padding()

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Espaciador superior flexible
        self.add_widget(Label(size_hint_y=0.1))

        # Etiqueta "RONDA ACTUAL"
        ronda_label = Label(
            text="RONDA ACTUAL",
            font_size=ResponsiveHelper.get_font_size(20),
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(ronda_label)

        # Número de ronda
        self.round_label = Label(
            text=self.round_str,
            font_size=ResponsiveHelper.get_font_size(40),
            color=(0, 0, 0, 1),
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )
        self.add_widget(self.round_label)

        # Espaciador
        self.add_widget(Label(size_hint_y=0.1))

        # Etiqueta "TIEMPO"
        tiempo_label = Label(
            text="TIEMPO",
            font_size=ResponsiveHelper.get_font_size(20),
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(tiempo_label)

        # Tiempo
        self.time_label = Label(
            text=self.time_str,
            font_size=ResponsiveHelper.get_font_size(50),
            color=(0, 0, 0, 1),
            bold=True,
            size_hint_y=None,
            height=dp(80)
        )
        self.add_widget(self.time_label)

        # Espaciador flexible
        self.add_widget(Label(size_hint_y=0.2))

        # Botón VOLVER con estilo
        back_button_container = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            padding=[dp(10), 0, dp(10), dp(10)]
        )
        
        self.back_button = Button(
            text="VOLVER",
            size_hint=(1, 1),
            background_normal='',
            background_color=(0.1, 0.4, 0.7, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=ResponsiveHelper.get_font_size(18)
        )
        
        # Agregar bordes redondeados al botón
        with self.back_button.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            self.back_button.rect = RoundedRectangle(
                pos=self.back_button.pos,
                size=self.back_button.size,
                radius=[dp(12)]
            )
        
        def update_button_rect(instance, value):
            self.back_button.rect.pos = instance.pos
            self.back_button.rect.size = instance.size
        
        self.back_button.bind(pos=update_button_rect, size=update_button_rect)
        self.back_button.bind(on_press=self.go_back)
        
        back_button_container.add_widget(self.back_button)
        self.add_widget(back_button_container)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def go_back(self, instance):
        screen_manager = self.parent.parent.parent
        if isinstance(screen_manager, ScreenManager):
            screen_manager.current = 'combates_anteriores'
    
    def on_window_resize(self, instance, width, height):
        Clock.schedule_once(lambda dt: self.update_layout(), 0.1)


# ------------------ PANTALLA PRINCIPAL RESPONSIVE ------------------
class MainScreentab(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        Window.bind(on_resize=self.on_window_resize)

    def build_ui(self):
        self.clear_widgets()
        
        # Determinar orientación según tamaño de ventana
        orientation = ResponsiveHelper.get_layout_orientation()
        
        main_layout = BoxLayout(
            orientation=orientation,
            spacing=0
        )

        # Panel Competidor 1
        self.com1_panel = CompetitorPanel(
            name="COM1",
            color=(0.117, 0.533, 0.898),
            nationality="KOR"
        )
        main_layout.add_widget(self.com1_panel)

        # Panel Central
        self.center_panel = CenterPanel()
        main_layout.add_widget(self.center_panel)

        # Panel Competidor 2
        self.com2_panel = CompetitorPanel(
            name="COM2",
            color=(0.898, 0.2, 0.2),
            nationality="USA"
        )
        main_layout.add_widget(self.com2_panel)

        self.add_widget(main_layout)
    
    def on_window_resize(self, instance, width, height):
        Clock.schedule_once(lambda dt: self.build_ui(), 0.1)


# ------------------ APLICACIÓN ------------------
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreentab(name='main_screen'))
        
        # Pantalla de combates anteriores (placeholder)
        combates_screen = Screen(name='combates_anteriores')
        placeholder_layout = BoxLayout(orientation='vertical', padding=dp(20))
        
        with placeholder_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            placeholder_layout.bg = Rectangle(
                pos=placeholder_layout.pos,
                size=placeholder_layout.size
            )
        
        def update_bg(instance, value):
            placeholder_layout.bg.pos = instance.pos
            placeholder_layout.bg.size = instance.size
        
        placeholder_layout.bind(pos=update_bg, size=update_bg)
        
        placeholder_layout.add_widget(Label(
            text='Pantalla de Combates Anteriores',
            font_size=sp(24),
            color=(0.1, 0.1, 0.2, 1)
        ))
        back_btn = Button(
            text='Volver al Tablero',
            size_hint=(0.5, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            background_normal='',
            background_color=(0.1, 0.4, 0.7, 1)
        )
        back_btn.bind(on_press=lambda x: setattr(sm, 'current', 'main_screen'))
        placeholder_layout.add_widget(back_btn)
        combates_screen.add_widget(placeholder_layout)
        
        sm.add_widget(combates_screen)
        
        return sm


if __name__ == '__main__':
    MyApp().run()