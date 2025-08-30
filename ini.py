from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.core.window import Window

class HoverButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_background_color = (0.1, 0.4, 0.7, 1)
        self.hover_background_color = (0.2, 0.5, 0.9, 1)
        self.background_color = self.original_background_color
        self.size_hint_y = None
        self.height = dp(50)
        self.font_size = sp(18)
        self.color = (1, 1, 1, 1)
        self.border_radius = dp(25)

        with self.canvas.before:
            Color(*self.original_background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[self.border_radius])
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.rect.radius = [self.border_radius]

class NavbarAuth(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, 1)
        self.width = dp(200)
        self.orientation = "vertical"
        self.padding = [dp(20), dp(20)]
        self.spacing = dp(10)

        with self.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        self.logo = Image(source="Imagen5-Photoroom.png", size_hint=(1, None), height=dp(150))
        self.add_widget(self.logo)

        # Añadimos un Widget vacío para crear espacio después del logo
        self.espacio_logo = Widget(size_hint_y=None, height=dp(100))  # Ajusta la altura según necesites
        self.add_widget(self.espacio_logo)

        self.botones_navbar = BoxLayout(orientation="vertical", spacing=dp(10))
        self.agregar_botones()
        self.add_widget(self.botones_navbar)

        self.add_widget(Widget(size_hint_y=1))

    def agregar_botones(self):
        menu_items = [
            ("Torneos", self.ir_a_torneos),
            ("Combates", self.ir_a_visualizar_combate),
            ("Crear Torneo", self.ir_a_crear_torneo),
            ("Crear Combate", self.ir_a_crear_combate),
            ("Mi cuenta", self.ir_a_cuenta),
            ("Cerrar Sesión", self.mostrar_popup_confirmacion)
        ]

        for text, action in menu_items:
            bg_color = (0.7, 0.1, 0.1, 1) if text == "Cerrar Sesión" else (0.1, 0.4, 0.7, 1)
            boton = HoverButton(text=text, size_hint_y=None, height=dp(50))
            boton.background_color = bg_color
            boton.bind(on_press=action)
            self.botones_navbar.add_widget(boton)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def ir_a_torneos(self, instance):
        App.get_running_app().root.current = 'torneos_anteriores'
    def ir_a_cuenta(self, instance):
        App.get_running_app().root.current = 'cuenta'

    def ir_a_crear_torneo(self, instance):
        App.get_running_app().root.current = 'crear_torneo'

    def ir_a_crear_combate(self, instance):
        App.get_running_app().root.current = 'crear_combate'

    def ir_a_visualizar_combate(self, instance):
        app = App.get_running_app()
        if not app.root.has_screen('combates_anteriores'):
            from combates_anteriore import CombatesScreen
            app.root.add_widget(CombatesScreen(name='combates_anteriores'))
        app.root.current = 'combates_anteriores'

    def mostrar_popup_confirmacion(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        lbl_mensaje = Label(
            text='¿Estás seguro que deseas\ncerrar sesión?',
            color=(0.2, 0.6, 1, 1),
            font_size=sp(20),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80))
        content.add_widget(lbl_mensaje)

        btn_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))

        btn_cancelar = Button(
            text='CANCELAR',
            background_normal='',
            background_color=(0.7, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(16))

        btn_confirmar = Button(
            text='CONFIRMAR',
            background_normal='',
            background_color=(0.1, 0.4, 0.7, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(16))

        btn_layout.add_widget(btn_cancelar)
        btn_layout.add_widget(btn_confirmar)
        content.add_widget(btn_layout)

        self.popup = Popup(
            title='Confirmar acción',
            title_color=(0.2, 0.6, 1, 1),
            title_size=sp(22),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=(dp(350), dp(220)),
            separator_height=0,
            background=''
        )

        with self.popup.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            self.popup.rect = RoundedRectangle(
                pos=self.popup.pos,
                size=self.popup.size,
                radius=[dp(15)]
            )

        def update_popup_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        self.popup.bind(pos=update_popup_rect, size=update_popup_rect)

        btn_cancelar.bind(on_press=self.popup.dismiss)
        btn_confirmar.bind(on_press=self.cerrar_sesion)

        self.popup.open()

    def cerrar_sesion(self, instance):
        self.popup.dismiss()
        App.get_running_app().root.current = 'main'

class MainInAuthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        Window.bind(on_resize=self.actualizar_tamanos)

    def build_ui(self):
        self.main_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0)

        self.navbar = NavbarAuth()
        self.main_layout.add_widget(self.navbar)

        self.content_container = BoxLayout(orientation='vertical', size_hint=(1, 1))

        with self.content_container.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(size=self.content_container.size,
                                     pos=self.content_container.pos)

        self.content_container.bind(size=self._update_bg_rect,
                                     pos=self._update_bg_rect)

        self.content_layout = BoxLayout(orientation='vertical',
                                         spacing=dp(20),
                                         padding=[dp(30), dp(20), dp(30), dp(20)])

        self.titulo = Label(
            text='PETO TECH',
            font_size=sp(40),
            color=(0.1, 0.1, 0.2, 1),
            bold=True,
            halign="center",
            size_hint_y=None,
            height=dp(80))
        self.content_layout.add_widget(self.titulo)

        self.eslogan = Label(
            text='Bienvenido al sistema de gestión de torneos',
            font_size=sp(24),
            color=(0.1, 0.4, 0.7, 1),
            halign="center",
            size_hint_y=None,
            height=dp(40))
        self.content_layout.add_widget(self.eslogan)

        self.imagenes_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(250),
            spacing=dp(20))

        self.img1 = Image(source="p1-Photoroom.png", size_hint_x=1)
        self.img2 = Image(source="p2-Photoroom.png", size_hint_x=1)
        self.imagenes_layout.add_widget(self.img1)
        self.imagenes_layout.add_widget(self.img2)
        self.content_layout.add_widget(self.imagenes_layout)

        self.copyright = Label(
            text="Copyright © 2025 - PetoTech System",
            font_size=sp(14),
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(30),
            halign="center")
        self.content_layout.add_widget(self.copyright)

        self.content_container.add_widget(self.content_layout)
        self.main_layout.add_widget(self.content_container)
        self.add_widget(self.main_layout)

        self.actualizar_tamanos()

    def _update_bg_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def actualizar_tamanos(self, *args):
        content_width = Window.width * 0.8 - dp(60)
        self.titulo.text_size = (content_width, None)
        self.eslogan.text_size = (content_width, None)
        self.imagenes_layout.height = max(dp(200), Window.height * 0.35)

class MainApp(App):
    def build(self):
        from kivy.uix.screenmanager import ScreenManager
        sm = ScreenManager()
        sm.add_widget(MainInAuthScreen(name='main_auth'))
        return sm

if __name__ == '__main__':
    MainApp().run()