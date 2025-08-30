from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.metrics import dp, sp

"""import requests
try:
    respuesta = requests.get("http://localhost:8080/apiAlumnos/alumno/1", json=datos)
    if respuesta.status_code == 201:
        self.ids.mensaje.text = "Usuario registrado con éxito."
    else:
        self.ids.mensaje.text = "Error al registrar usuario."
except Exception as e:
    self.ids.mensaje.text = f"Fallo conexión: {str(e)}"

try:
    respuesta = requests.post("http://localhost:8080/apiPuntajeDetalle/", json=datos)
    if respuesta.status_code == 201:
        self.ids.mensaje.text = "Usuario registrado con éxito."
    else:
        self.ids.mensaje.text = "Error al registrar usuario."
except Exception as e:
    self.ids.mensaje.text = f"Fallo conexión: {str(e)}"
"""

class CompetitorPanel(BoxLayout):
    score = NumericProperty(0)
    penalty_score = NumericProperty(0)

    def __init__(self, name, color, nationality="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 15
        self.name = name
        self.bg_color = get_color_from_hex(color)
        self.nationality = nationality

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        if self.nationality:
            self.add_widget(Label(text=self.nationality.upper(), font_size=20, bold=True, color=(1, 1, 1, 1)))

        self.add_widget(Label(text=name, font_size=30, bold=True, color=(1, 1, 1, 1)))

        score_layout = BoxLayout(size_hint=(1, 0.4), spacing=10)
        score_layout.add_widget(Button(text="-", on_press=lambda x: self.update_score(-1),
                                       font_size=30, background_color=(0.2, 0.2, 0.2, 1), color=(1, 1, 1, 1)))
        self.score_label = Label(text="0", font_size=60, color=(1, 1, 1, 1))
        score_layout.add_widget(self.score_label)
        score_layout.add_widget(Button(text="+", on_press=lambda x: self.update_score(1),
                                       font_size=30, background_color=(0.2, 0.2, 0.2, 1), color=(1, 1, 1, 1)))
        self.add_widget(score_layout)

        self.add_widget(Label(text="GAM-JEOM", font_size=20, color=(1, 1, 1, 1)))

        penalty_layout = BoxLayout(size_hint=(1, 0.4), spacing=10)
        penalty_layout.add_widget(Button(text="-", on_press=lambda x: self.update_penalty(-1),
                                         font_size=30, background_color=(0.2, 0.2, 0.2, 1), color=(1, 1, 1, 1)))
        self.penalty_label = Label(text="0", font_size=40, color=(1, 1, 1, 1))
        penalty_layout.add_widget(self.penalty_label)
        penalty_layout.add_widget(Button(text="+", on_press=lambda x: self.update_penalty(1),
                                         font_size=30, background_color=(0.2, 0.2, 0.2, 1), color=(1, 1, 1, 1)))

        self.add_widget(penalty_layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_penalty(self, value):
        self.penalty_score += value
        if self.penalty_score < 0:
            self.penalty_score = 0
        self.penalty_label.text = str(self.penalty_score)

    def update_score(self, value):
        self.score += value
        if self.score < 0:
            self.score = 0
        self.score_label.text = str(self.score)

class CenterPanel(BoxLayout):
    time_str = StringProperty("00:00")
    round_str = StringProperty("Round 1")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 10
        self.timer_running = False
        self.elapsed_time = 0
        self.round_number = 1

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.add_widget(Label(text="RONDA ACTUAL", font_size=20, color=(0, 0, 0, 1)))
        self.round_label = Label(text=self.round_str, font_size=40, color=(0, 0, 0, 1))
        self.add_widget(self.round_label)

        self.add_widget(Label(text="TIEMPO", font_size=20, color=(0, 0, 0, 1)))
        self.time_label = Label(text=self.time_str, font_size=50, color=(0, 0, 0, 1))
        self.bind(time_str=self.time_label.setter('text'))
        self.add_widget(self.time_label)

        btn_layout = BoxLayout(size_hint=(1, 0.3), spacing=10)
        btn_layout.add_widget(Button(text="PAUSA", on_press=lambda x: self.pause_timer(),
                                     background_color=(0.1, 0.4, 0.7, 1), color=(1, 1, 1, 1)))
        btn_layout.add_widget(Button(text="PLAY", on_press=lambda x: self.start_timer(),
                                     background_color=(0.1, 0.4, 0.7, 1), color=(1, 1, 1, 1)))
        self.add_widget(btn_layout)

        self.next_round_button = Button(text="SIGUIENTE RONDA", size_hint=(1, 0.2),
                                        background_color=(0.1, 0.4, 0.7, 1), color=(1, 1, 1, 1),
                                        on_press=self.show_next_round_confirmation)
        self.add_widget(self.next_round_button)

        self.end_button = Button(text="FINALIZAR COMBATE", size_hint=(1, 0.2),
                                 background_color=(0.1, 0.4, 0.7, 1), color=(1, 1, 1, 1),
                                 on_press=self.show_end_combat_confirmation)
        self.add_widget(self.end_button)
        
        self.back_button = Button(text="SALIR", size_hint=(1, 0.2),
                                 background_color=(0.1, 0.4, 0.7, 1), color=(1, 1, 1, 1),
                                 on_press=self.go_back)
        self.add_widget(self.back_button)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            Clock.schedule_interval(self.update_time, 1)

    def pause_timer(self):
        self.timer_running = False
        Clock.unschedule(self.update_time)

    def update_time(self, dt):
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.time_str = f"{minutes:02}:{seconds:02}"

    def mostrar_mensaje(self, titulo, mensaje, confirm_callback=None):
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
        
        btn_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
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
        
        if confirm_callback:
            btn_cancelar = Button(
                text='CANCELAR',
                size_hint_x=0.5,
                background_normal='',
                background_color=(0.8, 0.2, 0.2, 1),
                color=(1, 1, 1, 1),
                bold=True,
                font_size=sp(18))
            btn_cancelar.bind(on_press=popup.dismiss)
            btn_layout.add_widget(btn_cancelar)
        
        btn_text = 'ACEPTAR' if confirm_callback else 'ENTENDIDO'
        btn_aceptar = Button(
            text=btn_text,
            size_hint_x=0.5 if confirm_callback else 1,
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))
        
        if confirm_callback:
            btn_aceptar.bind(on_press=lambda x: [popup.dismiss(), confirm_callback()])
        else:
            btn_aceptar.bind(on_press=popup.dismiss)
        
        btn_layout.add_widget(btn_aceptar)
        content.add_widget(btn_layout)
        
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
        popup.open()

    def show_next_round_confirmation(self, instance):
        self.mostrar_mensaje(
            titulo="Confirmar Siguiente Ronda",
            mensaje="¿Estás seguro de avanzar a\na la siguiente ronda?",
            confirm_callback=lambda: self.next_round(instance)
        )

    def show_end_combat_confirmation(self, instance):
        self.mostrar_mensaje(
            titulo="Finalizar Combate",
            mensaje="¿Confirmas que deseas\nfinalizar el combate?",
            confirm_callback=lambda: self.end_combat(instance)
        )

    def next_round(self, instance):
        if self.round_number < 3:
            self.round_number += 1
            self.round_str = f"Round {self.round_number}"
            self.round_label.text = self.round_str
            self.elapsed_time = 0
            self.time_str = "00:00"
            self.time_label.text = self.time_str
            self.pause_timer()
            self.mostrar_mensaje(
                titulo="Ronda Actualizada",
                mensaje=f"Has avanzado a la\nronda {self.round_number}"
            )

    def end_combat(self, instance):
        self.pause_timer()
        self.time_str = "FIN"
        self.time_label.text = self.time_str
        self.round_label.text = "Combate Finalizado"
        self.mostrar_mensaje(
            titulo="Combate Finalizado",
            mensaje="El combate ha sido\ndado por finalizado"
        )
        
    def go_back(self, instance):
        self.mostrar_mensaje(
            titulo="Confirmar salida",
            mensaje="¿Estás segura(o) que deseas salir\nde este combate?",
            confirm_callback=self.confirm_go_back
        )

    def confirm_go_back(self):
        self.parent.parent.parent.current = 'ini_juez'

class MainScreentabc(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'tablero_central'
        
        main_layout = BoxLayout(spacing=0)
        
        self.com1_panel = CompetitorPanel(name="COM1", color="#1E88E5", nationality="KOR")
        main_layout.add_widget(self.com1_panel)

        self.center_panel = CenterPanel()
        main_layout.add_widget(self.center_panel)

        self.com2_panel = CompetitorPanel(name="COM2", color="#E53935", nationality="USA")
        main_layout.add_widget(self.com2_panel)

        self.add_widget(main_layout)

