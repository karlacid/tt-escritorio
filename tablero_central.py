from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from kivy.utils import get_color_from_hex, platform
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.metrics import dp, sp
from kivy.core.window import Window
from threading import Thread
from kivy.clock import mainthread
import requests
import json

try:
    import websocket
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    print("=" * 60)
    print("  ADVERTENCIA: websocket-client no instalado")
    print("  Ejecuta: pip install websocket-client")
    print("  Las actualizaciones en tiempo real NO funcionarán")
    print("=" * 60)


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
        width = Window.width
        height = Window.height
        min_dimension = min(width, height)
        if min_dimension < 600:
            return sp(base_size * 0.6)
        elif min_dimension < 900:
            return sp(base_size * 0.75)
        elif min_dimension < 1200:
            return sp(base_size * 0.9)
        return sp(base_size)

    @staticmethod
    def get_popup_size():
        width = Window.width
        height = Window.height
        if width < 600:
            return (width * 0.9, min(height * 0.4, dp(300)))
        else:
            return (min(width * 0.6, dp(450)), min(height * 0.35, dp(250)))

    @staticmethod
    def get_layout_orientation():
        return 'horizontal' if Window.width > Window.height and Window.width > 800 else 'vertical'

    @staticmethod
    def get_button_height():
        width = Window.width
        if width < 600:
            return dp(40)
        return dp(50)


# ------------------ POPUP DE DESCANSO ENTRE ROUNDS ------------------
class RestPopup(Popup):
    """Popup que aparece automáticamente durante el descanso con su propio cronómetro"""
    
    def __init__(self, round_number, duracion_descanso, on_rest_end_callback, round_scores, **kwargs):
        self.round_number = round_number
        self.duracion_descanso = duracion_descanso
        self.on_rest_end_callback = on_rest_end_callback
        self.round_scores = round_scores  # dict: {'rojo': [...], 'azul': [...]}
        self.remaining = duracion_descanso
        self._clock_event = None
        
        content = self._build_content()
        
        super().__init__(
            title='',
            content=content,
            size_hint=(None, None),
            size=(dp(750), dp(620)),
            separator_height=0,
            background='',
            auto_dismiss=False
        )
        
        with self.canvas.before:
            Color(0.05, 0.05, 0.15, 0.97)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
        self.bind(pos=self._update_bg, size=self._update_bg)
        self._clock_event = Clock.schedule_interval(self._tick, 1)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _build_content(self):
        root = BoxLayout(orientation='vertical', spacing=dp(8), padding=[dp(25), dp(20)])

        # Título DESCANSO
        rest_lbl = Label(
            text="DESCANSO",
            font_size=sp(34),
            bold=True,
            color=(1, 0.75, 0.1, 1),
            size_hint_y=None,
            height=dp(50)
        )
        root.add_widget(rest_lbl)

        # Próximo round
        next_round = self.round_number + 1
        next_lbl = Label(
            text=f"Próximo Round {next_round}",
            font_size=sp(20),
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(30)
        )
        root.add_widget(next_lbl)

        # Cronómetro grande
        mins = self.remaining // 60
        secs = self.remaining % 60
        timer_container = BoxLayout(size_hint_y=None, height=dp(160))
        with timer_container.canvas.before:
            Color(0.02, 0.02, 0.12, 1)
            timer_container._bg = RoundedRectangle(pos=timer_container.pos, size=timer_container.size, radius=[dp(12)])
        timer_container.bind(
            pos=lambda i, v: setattr(i._bg, 'pos', v),
            size=lambda i, v: setattr(i._bg, 'size', v)
        )
        self.timer_lbl = Label(
            text=f"{mins:02}:{secs:02}",
            font_size=sp(120),
            bold=True,
            color=(1, 0.85, 0.1, 1),
            size_hint_y=None,
            height=dp(155)
        )
        timer_container.add_widget(self.timer_lbl)
        root.add_widget(timer_container)

        # Tabla de puntajes por round
        table_title = Label(
            text="PUNTAJES POR ROUND",
            font_size=sp(15),
            bold=True,
            color=(0.6, 0.9, 1, 1),
            size_hint_y=None,
            height=dp(24)
        )
        root.add_widget(table_title)

        # Grid tabla
        grid = self._build_scores_table()
        root.add_widget(grid)

        # Botón skip
        btn_skip = Button(
            text="SALTAR DESCANSO",
            size_hint_y=None,
            height=dp(45),
            background_normal='',
            background_color=(0.15, 0.55, 0.9, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(16)
        )
        btn_skip.bind(on_press=self._skip)
        root.add_widget(btn_skip)

        return root

    def _build_scores_table(self):
        num_rounds = len(self.round_scores.get('rojo', []))
        cols = num_rounds + 2  # round col + scores + total
        grid = GridLayout(
            cols=cols,
            size_hint_y=None,
            height=dp(85),
            spacing=[dp(3), dp(3)]
        )

        # Header row
        self._add_cell(grid, "", (0.2, 0.2, 0.35, 1), (0.6, 0.6, 0.6, 1), bold=True)
        for i in range(num_rounds):
            self._add_cell(grid, f"R{i+1}", (0.2, 0.2, 0.35, 1), (0.8, 0.8, 0.8, 1), bold=True)
        self._add_cell(grid, "TOTAL", (0.15, 0.15, 0.3, 1), (1, 0.85, 0.2, 1), bold=True)

        # Row ROJO (ahora primero, izquierda)
        self._add_cell(grid, "ROJO", (0.6, 0.1, 0.1, 1), (1, 1, 1, 1), bold=True)
        rojo_scores = self.round_scores.get('rojo', [])
        for s in rojo_scores:
            self._add_cell(grid, str(s), (0.5, 0.1, 0.1, 1), (1, 1, 1, 1))
        total_rojo = sum(rojo_scores)
        self._add_cell(grid, str(total_rojo), (0.45, 0.08, 0.08, 1), (1, 0.85, 0.2, 1), bold=True)

        # Row AZUL (ahora segundo, derecha)
        self._add_cell(grid, "AZUL", (0.1, 0.25, 0.6, 1), (1, 1, 1, 1), bold=True)
        azul_scores = self.round_scores.get('azul', [])
        for s in azul_scores:
            self._add_cell(grid, str(s), (0.12, 0.2, 0.5, 1), (1, 1, 1, 1))
        total_azul = sum(azul_scores)
        self._add_cell(grid, str(total_azul), (0.08, 0.15, 0.45, 1), (1, 0.85, 0.2, 1), bold=True)

        return grid

    def _add_cell(self, grid, text, bg_color, text_color, bold=False):
        lbl = Label(
            text=text,
            font_size=sp(13),
            bold=bold,
            color=text_color
        )
        with lbl.canvas.before:
            Color(*bg_color)
            lbl._bg_rect = Rectangle(pos=lbl.pos, size=lbl.size)
        lbl.bind(pos=lambda i, v: setattr(i._bg_rect, 'pos', v),
                 size=lambda i, v: setattr(i._bg_rect, 'size', v))
        grid.add_widget(lbl)

    def _tick(self, dt):
        if self.remaining > 0:
            self.remaining -= 1
            mins = self.remaining // 60
            secs = self.remaining % 60
            self.timer_lbl.text = f"{mins:02}:{secs:02}"
        else:
            self._end_rest()

    def _skip(self, *args):
        self._end_rest()

    def _end_rest(self):
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None
        self.dismiss()
        if self.on_rest_end_callback:
            Clock.schedule_once(lambda dt: self.on_rest_end_callback(), 0.2)


# ------------------ PANEL DE COMPETIDOR ------------------
class CompetitorPanel(BoxLayout):
    score = NumericProperty(0)
    penalty_score = NumericProperty(0)
    api_score = NumericProperty(0)

    def __init__(self, name, color, nationality="", alumno_id=None, combate_id=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.name = name
        self.bg_color = get_color_from_hex(color)
        self.nationality = nationality
        self.alumno_id = alumno_id
        self.combate_id = combate_id
        self.parent_screen = None
        self.max_gamjeom = 3
        self.round_scores = []   # puntajes por round
        self.current_round_score = 0

        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        self.spacing = dp(4)
        self.padding = [dp(10), dp(10)]

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Nacionalidad
        if self.nationality:
            nat_lbl = Label(
                text=self.nationality.upper(),
                font_size=ResponsiveHelper.get_font_size(20),
                bold=True,
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=dp(32)
            )
            self.add_widget(nat_lbl)

        # Nombre
        name_lbl = Label(
            text=self.name,
            font_size=ResponsiveHelper.get_font_size(22),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(name_lbl)

        # ── SCORE GRANDE estilo Daedo ──
        score_outer = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(300),
            padding=[dp(5), dp(5)]
        )

        # Fila: [-]  NÚMERO  [+]
        score_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(280),
            spacing=dp(6)
        )

        btn_minus = Button(
            text="−",
            on_press=lambda x: self.subtract_score_api(),
            size_hint_x=None,
            width=dp(36),
            font_size=sp(22),
            background_normal='',
            background_color=(0, 0, 0, 0.4),
            color=(1, 1, 1, 1),
            bold=True
        )
        score_row.add_widget(btn_minus)

        self.score_label = Label(
            text="0",
            font_size=sp(260),
            color=(1, 1, 1, 1),
            bold=True,
        )
        score_row.add_widget(self.score_label)

        btn_plus = Button(
            text="+",
            on_press=lambda x: self.add_score_api(),
            size_hint_x=None,
            width=dp(36),
            font_size=sp(22),
            background_normal='',
            background_color=(0, 0, 0, 0.4),
            color=(1, 1, 1, 1),
            bold=True
        )
        score_row.add_widget(btn_plus)

        score_outer.add_widget(score_row)
        self.add_widget(score_outer)

        # Status indicator
        self.status_indicator = Label(
            text="",
            font_size=ResponsiveHelper.get_font_size(11),
            color=(1, 1, 0.5, 1),
            size_hint_y=None,
            height=dp(18)
        )
        self.add_widget(self.status_indicator)

        # ── GAM-JEOM ──
        gj_title = Label(
            text="GAM-JEOM",
            font_size=ResponsiveHelper.get_font_size(15),
            color=(1, 1, 1, 0.9),
            size_hint_y=None,
            height=dp(24)
        )
        self.add_widget(gj_title)

        penalty_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(6)
        )

        btn_minus_p = Button(
            text="−",
            on_press=lambda x: self.subtract_gamjeom_api(),
            size_hint_x=None,
            width=dp(32),
            font_size=sp(18),
            background_normal='',
            background_color=(0, 0, 0, 0.4),
            color=(1, 1, 1, 1),
            bold=True
        )
        penalty_row.add_widget(btn_minus_p)

        self.penalty_label = Label(
            text="0",
            font_size=sp(70),
            color=(1, 1, 1, 1),
            bold=True
        )
        penalty_row.add_widget(self.penalty_label)

        btn_plus_p = Button(
            text="+",
            on_press=lambda x: self.add_gamjeom_api(),
            size_hint_x=None,
            width=dp(32),
            font_size=sp(18),
            background_normal='',
            background_color=(0, 0, 0, 0.4),
            color=(1, 1, 1, 1),
            bold=True
        )
        penalty_row.add_widget(btn_plus_p)
        self.add_widget(penalty_row)

        self.gamjeom_status = Label(
            text="",
            font_size=ResponsiveHelper.get_font_size(11),
            color=(1, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(18)
        )
        self.add_widget(self.gamjeom_status)

        # ── TABLA DE PUNTAJES POR ROUND ──
        self.add_widget(BoxLayout(size_hint_y=None, height=dp(6)))

        table_title = Label(
            text="PUNTOS POR ROUND",
            font_size=sp(16),
            bold=True,
            color=(1, 1, 1, 0.85),
            size_hint_y=None,
            height=dp(26)
        )
        self.add_widget(table_title)

        self.round_table_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            height=dp(80),
            spacing=dp(3)
        )
        self._rebuild_round_table()
        self.add_widget(self.round_table_layout)

        # ── INDICADORES LED JUECES ──
        self.add_widget(BoxLayout(size_hint_y=None, height=dp(8)))

        judges_title = Label(
            text="JUECES",
            font_size=sp(13),
            bold=True,
            color=(1, 1, 1, 0.6),
            size_hint_y=None,
            height=dp(18)
        )
        self.add_widget(judges_title)

        judges_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(62),
            spacing=dp(10),
            padding=[dp(6), dp(2)]
        )

        self._judge_indicators = {}
        CIRCLE_D = dp(26)
        CELL_W   = dp(40)

        # Espaciador izquierdo para centrar el grupo
        judges_row.add_widget(BoxLayout())

        for j_name in ['J1', 'J2', 'J3']:
            cell = BoxLayout(
                orientation='vertical',
                size_hint=(None, 1),
                width=CELL_W,
                spacing=dp(4)
            )

            circle_row = BoxLayout(size_hint_y=None, height=CIRCLE_D)
            spacer_l = BoxLayout()
            led_widget = Widget(size_hint=(None, None), size=(CIRCLE_D, CIRCLE_D))
            with led_widget.canvas:
                led_widget._led_color = Color(1, 1, 1, 1)  # blanco apagado
                led_widget._led_circle = RoundedRectangle(
                    pos=led_widget.pos, size=led_widget.size, radius=[CIRCLE_D / 2]
                )
            led_widget.bind(
                pos=lambda i, v: setattr(i._led_circle, 'pos', v),
                size=lambda i, v: (
                    setattr(i._led_circle, 'size', v),
                    setattr(i._led_circle, 'radius', [v[0] / 2])
                )
            )
            spacer_r = BoxLayout()
            circle_row.add_widget(spacer_l)
            circle_row.add_widget(led_widget)
            circle_row.add_widget(spacer_r)

            lbl_name = Label(
                text=j_name,
                font_size=sp(14),
                bold=True,
                color=(1, 1, 1, 0.85),
                size_hint_y=None,
                height=dp(18),
                halign='center',
                valign='middle'
            )
            lbl_name.bind(size=lbl_name.setter('text_size'))

            cell.add_widget(circle_row)
            cell.add_widget(lbl_name)
            judges_row.add_widget(cell)
            self._judge_indicators[j_name] = led_widget

        # Espaciador derecho
        judges_row.add_widget(BoxLayout())
        self.add_widget(judges_row)
        self.add_widget(BoxLayout(size_hint_y=0.05))

    def _rebuild_round_table(self):
        self.round_table_layout.clear_widgets()

        if not self.round_scores and not self.current_round_score:
            empty = Label(
                text="—",
                font_size=sp(16),
                color=(1, 1, 1, 0.4),
                size_hint_y=None,
                height=dp(30)
            )
            self.round_table_layout.add_widget(empty)
            return

        num_rounds = len(self.round_scores) + 1
        self.round_table_layout.cols = num_rounds + 1
        self.round_table_layout.size_hint_y = None
        self.round_table_layout.height = dp(76)

        header_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30), spacing=dp(2))
        self._add_table_cell(header_row, "", (0, 0, 0, 0.3), (0.7, 0.7, 0.7, 1), sp(14))
        for i in range(len(self.round_scores)):
            self._add_table_cell(header_row, f"R{i+1}", (0, 0, 0, 0.25), (0.85, 0.85, 0.85, 1), sp(14), bold=True)
        self._add_table_cell(header_row, f"R{len(self.round_scores)+1}*", (0, 0, 0, 0.3), (1, 0.9, 0.3, 1), sp(14), bold=True)
        self.round_table_layout.add_widget(header_row)

        score_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(34), spacing=dp(2))
        self._add_table_cell(score_row, "PTS", (0, 0, 0, 0.3), (0.7, 0.7, 0.7, 1), sp(14), bold=True)
        for s in self.round_scores:
            self._add_table_cell(score_row, str(s), (0, 0, 0, 0.2), (1, 1, 1, 1), sp(16))
        self._add_table_cell(score_row, str(self.api_score), (0, 0, 0, 0.2), (1, 1, 0.4, 1), sp(16), bold=True)
        self.round_table_layout.add_widget(score_row)

    def _add_table_cell(self, parent, text, bg, fg, font_size, bold=False):
        lbl = Label(text=text, font_size=font_size, bold=bold, color=fg)
        with lbl.canvas.before:
            Color(*bg)
            lbl._r = Rectangle(pos=lbl.pos, size=lbl.size)
        lbl.bind(pos=lambda i, v: setattr(i._r, 'pos', v),
                 size=lambda i, v: setattr(i._r, 'size', v))
        parent.add_widget(lbl)

    @mainthread
    def set_judge_active(self, judge_name, active, auto_reset_seconds=3):
        if not hasattr(self, '_judge_indicators'):
            return
        led = self._judge_indicators.get(judge_name)
        if not led:
            return
        if active:
            led._led_color.rgba = (0.15, 0.9, 0.25, 1)
            if auto_reset_seconds > 0:
                Clock.schedule_once(
                    lambda dt, j=judge_name: self.set_judge_active(j, False, 0),
                    auto_reset_seconds
                )
        else:
            led._led_color.rgba = (1, 1, 1, 1)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def save_round_score(self):
        self.round_scores.append(self.api_score)
        self._rebuild_round_table()
        print(f"[CompetitorPanel] Round guardado para {self.name}: {self.api_score} → historial: {self.round_scores}")

    def get_total_score(self):
        """Retorna la suma total de todos los rounds incluyendo el actual"""
        return sum(self.round_scores) + self.api_score

    # ==================== MÉTODOS DE PUNTAJE ====================

    def add_score_api(self):
        if not self.alumno_id or not self.combate_id:
            print("[CompetitorPanel] No hay alumno_id o combate_id")
            return
        if self.parent_screen and not self.parent_screen.is_timer_active():
            self.show_status("Inicia el timer primero")
            return
        self.show_status("Guardando...")

        def work():
            try:
                url = f"http://localhost:8080/apiPuntajes/puntaje/simple?combateId={self.combate_id}&alumnoId={self.alumno_id}&valorPuntaje=1"
                response = requests.post(url, timeout=5)
                if response.status_code in [200, 201]:
                    data = response.json()
                    new_count = data.get('newCount', 0)
                    self.update_api_score(new_count)
                    self.show_status("+1")
                    Clock.schedule_once(lambda dt: self.clear_status(), 1)
                else:
                    self.show_status(f"✗ Error {response.status_code}")
            except Exception as e:
                self.show_status("✗ Error conexión")
        Thread(target=work, daemon=True).start()

    def subtract_score_api(self):
        if not self.alumno_id:
            return
        if self.parent_screen and not self.parent_screen.is_timer_active():
            self.show_status("Inicia el timer primero")
            return
        if self.api_score <= 0:
            self.show_status("Ya está en 0")
            return
        self.show_status("Eliminando...")

        def work():
            try:
                url = f"http://localhost:8080/apiPuntajes/puntaje/alumno/{self.alumno_id}/last"
                response = requests.delete(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    new_count = data.get('newCount', 0)
                    self.update_api_score(new_count)
                    self.show_status("-1")
                    Clock.schedule_once(lambda dt: self.clear_status(), 1)
                elif response.status_code == 204:
                    self.refresh_score()
                    self.show_status("✓ -1")
                    Clock.schedule_once(lambda dt: self.clear_status(), 1)
                else:
                    self.show_status(f"✗ Error {response.status_code}")
            except Exception as e:
                self.show_status("✗ Error conexión")
        Thread(target=work, daemon=True).start()

    def refresh_score(self):
        if not self.alumno_id:
            return
        def work():
            try:
                url = f"http://localhost:8080/apiPuntajes/puntaje/alumno/{self.alumno_id}/count"
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    new_count = response.json().get('count', 0)
                    self.update_api_score(new_count)
            except:
                pass
        Thread(target=work, daemon=True).start()

    @mainthread
    def update_api_score(self, new_score):
        self.api_score = new_score
        self.score_label.text = str(self.api_score)
        self._rebuild_round_table()
        print(f"[CompetitorPanel] Score actualizado: {self.name} = {self.api_score}")

    @mainthread
    def show_status(self, text):
        self.status_indicator.text = text

    @mainthread
    def clear_status(self):
        self.status_indicator.text = ""

    # ==================== MÉTODOS DE GAM-JEOM ====================

    def add_gamjeom_api(self):
        if not self.alumno_id or not self.combate_id:
            return
        if self.parent_screen and not self.parent_screen.is_timer_active():
            self.show_gamjeom_status("Inicia el timer primero")
            return
        self.show_gamjeom_status("Registrando falta...")

        def work():
            try:
                url = f"http://localhost:8080/apiGamJeom/falta/simple?combateId={self.combate_id}&alumnoId={self.alumno_id}"
                response = requests.post(url, timeout=5)
                if response.status_code in [200, 201]:
                    data = response.json()
                    total_faltas = data.get('totalFaltas', 0)
                    descalificado = data.get('descalificado', False)
                    self.update_gamjeom_count(total_faltas)
                    if descalificado:
                        self.show_gamjeom_status("DESCALIFICADO")
                        if self.parent_screen:
                            self.parent_screen.on_player_disqualified(self.alumno_id, self.name)
                    else:
                        self.show_gamjeom_status(f"Falta {total_faltas}/3")
                        Clock.schedule_once(lambda dt: self.clear_gamjeom_status(), 2)
                else:
                    self.show_gamjeom_status(f"✗ Error {response.status_code}")
            except:
                self.show_gamjeom_status("✗ Error conexión")
        Thread(target=work, daemon=True).start()

    def subtract_gamjeom_api(self):
        if not self.alumno_id or not self.combate_id:
            return
        if self.parent_screen and not self.parent_screen.is_timer_active():
            self.show_gamjeom_status("Inicia el timer primero")
            return
        if self.penalty_score <= 0:
            self.show_gamjeom_status("Ya está en 0")
            return
        self.show_gamjeom_status("Eliminando falta...")

        def work():
            try:
                url = f"http://localhost:8080/apiGamJeom/falta/alumno/{self.alumno_id}/combate/{self.combate_id}/last"
                response = requests.delete(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    new_count = data.get('newCount', 0)
                    self.update_gamjeom_count(new_count)
                    self.show_gamjeom_status("Falta eliminada")
                    Clock.schedule_once(lambda dt: self.clear_gamjeom_status(), 1)
                else:
                    self.show_gamjeom_status(f"✗ Error {response.status_code}")
            except:
                self.show_gamjeom_status("✗ Error conexión")
        Thread(target=work, daemon=True).start()

    def refresh_gamjeom(self):
        if not self.alumno_id or not self.combate_id:
            return
        def work():
            try:
                url = f"http://localhost:8080/apiGamJeom/falta/alumno/{self.alumno_id}/combate/{self.combate_id}/count"
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    new_count = response.json().get('count', 0)
                    self.update_gamjeom_count(new_count)
            except:
                pass
        Thread(target=work, daemon=True).start()

    @mainthread
    def update_gamjeom_count(self, count):
        self.penalty_score = count
        self.penalty_label.text = str(count)
        if count >= 2:
            self.penalty_label.color = (1, 0.3, 0.3, 1)
        elif count >= 1:
            self.penalty_label.color = (1, 0.7, 0.3, 1)
        else:
            self.penalty_label.color = (1, 1, 1, 1)

    @mainthread
    def show_gamjeom_status(self, text):
        self.gamjeom_status.text = text

    @mainthread
    def clear_gamjeom_status(self):
        self.gamjeom_status.text = ""

    def reset_scores(self):
        self.clear_status()
        self.clear_gamjeom_status()
        self._rebuild_round_table()


# ------------------ POPUP TIEMPO MÉDICO ------------------
class MedicalTimePopup(Popup):
    def __init__(self, athlete_name, athlete_color, on_result_callback, **kwargs):
        self.athlete_name = athlete_name
        self.athlete_color = athlete_color
        self.on_result_callback = on_result_callback
        self.remaining = 60
        self._clock_event = None

        content = self._build_content()

        super().__init__(
            title='',
            content=content,
            size_hint=(None, None),
            size=(dp(600), dp(520)),
            separator_height=0,
            background='',
            auto_dismiss=False
        )

        bg_color = (0.45, 0.04, 0.04, 0.97) if athlete_color == 'rojo' else (0.04, 0.12, 0.50, 0.97)
        with self.canvas.before:
            Color(*bg_color)
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        self.bind(on_open=self._start_clock)
        Clock.schedule_once(self._start_clock, 0.3)

    def _upd_bg(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def _start_clock(self, *args):
        if self._clock_event is None:
            self._clock_event = Clock.schedule_interval(self._tick, 1)

    def _build_content(self):
        root = BoxLayout(orientation='vertical', spacing=dp(8), padding=[dp(20), dp(14)])

        title_lbl = Label(
            text="TIEMPO MÉDICO",
            font_size=sp(26),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(40)
        )
        root.add_widget(title_lbl)

        color_text = "ATLETA ROJO" if self.athlete_color == 'rojo' else "ATLETA AZUL"
        athlete_color_rgba = (1, 0.25, 0.25, 1) if self.athlete_color == 'rojo' else (0.3, 0.65, 1, 1)
        athlete_lbl = Label(
            text=f"{color_text}  —  {self.athlete_name}",
            font_size=sp(18),
            bold=True,
            color=athlete_color_rgba,
            size_hint_y=None,
            height=dp(28)
        )
        root.add_widget(athlete_lbl)

        timer_container = BoxLayout(size_hint_y=None, height=dp(160))
        with timer_container.canvas.before:
            Color(0.05, 0.05, 0.08, 1)
            timer_container._bg = RoundedRectangle(
                pos=timer_container.pos, size=timer_container.size, radius=[dp(10)]
            )
        timer_container.bind(
            pos=lambda i, v: setattr(i._bg, 'pos', v),
            size=lambda i, v: setattr(i._bg, 'size', v)
        )
        self.timer_lbl = Label(
            text="01:00",
            font_size=sp(110),
            bold=True,
            color=(1, 0.85, 0.1, 1),
        )
        timer_container.add_widget(self.timer_lbl)
        root.add_widget(timer_container)

        root.add_widget(BoxLayout(size_hint_y=0.05))

        result_lbl = Label(
            text="RESULTADO",
            font_size=sp(13),
            bold=True,
            color=(1, 1, 1, 0.6),
            size_hint_y=None,
            height=dp(18)
        )
        root.add_widget(result_lbl)

        btn_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            spacing=dp(8)
        )

        btn_continuar = Button(
            text="CONTINUAR",
            background_normal='',
            background_color=(0.12, 0.55, 0.18, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(15)
        )
        btn_continuar.bind(on_press=lambda x: self._result('continuar'))

        btn_abandono = Button(
            text="ABANDONO",
            background_normal='',
            background_color=(0.65, 0.38, 0.04, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(15)
        )
        btn_abandono.bind(on_press=lambda x: self._result('abandono'))

        btn_descalif = Button(
            text="DESCALIFICAR",
            background_normal='',
            background_color=(0.65, 0.08, 0.08, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(15)
        )
        btn_descalif.bind(on_press=lambda x: self._result('descalificacion'))

        btn_row.add_widget(btn_continuar)
        btn_row.add_widget(btn_abandono)
        btn_row.add_widget(btn_descalif)
        root.add_widget(btn_row)

        return root

    def _tick(self, dt):
        if self.remaining > 0:
            self.remaining -= 1
        mins = self.remaining // 60
        secs = self.remaining % 60
        self.timer_lbl.text = f"{mins:02}:{secs:02}"
        if self.remaining <= 10:
            self.timer_lbl.color = (1, 0.3, 0.3, 1)
        elif self.remaining <= 20:
            self.timer_lbl.color = (1, 0.75, 0.2, 1)

    def _stop_clock(self):
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None

    def _result(self, result):
        self._stop_clock()
        self.dismiss()
        if self.on_result_callback:
            Clock.schedule_once(
                lambda dt: self.on_result_callback(result, self.athlete_color, self.athlete_name),
                0.2
            )


# ------------------ POPUP RESULTADO FINAL ------------------
class FinalResultPopup(Popup):
    """Popup que muestra el ganador al finalizar el combate con tabla de puntajes."""

    def __init__(self, nombre_rojo, score_rojo, rounds_rojo,
                       nombre_azul, score_azul, rounds_azul,
                       on_close_callback=None, **kwargs):
        self.on_close_callback = on_close_callback

        # Calcular totales
        total_rojo = sum(rounds_rojo) + score_rojo
        total_azul = sum(rounds_azul) + score_azul

        if total_rojo > total_azul:
            ganador = nombre_rojo
            color_ganador = (1, 0.3, 0.3, 1)        # rojo
            bg_ganador = (0.55, 0.06, 0.06, 0.97)
            etiqueta_ganador = "ROJO"
        elif total_azul > total_rojo:
            ganador = nombre_azul
            color_ganador = (0.3, 0.65, 1, 1)        # azul
            bg_ganador = (0.04, 0.12, 0.52, 0.97)
            etiqueta_ganador = "AZUL"
        else:
            ganador = "EMPATE"
            color_ganador = (1, 0.85, 0.1, 1)        # dorado
            bg_ganador = (0.12, 0.12, 0.18, 0.97)
            etiqueta_ganador = "EMPATE"

        content = self._build_content(
            nombre_rojo, rounds_rojo, score_rojo, total_rojo,
            nombre_azul, rounds_azul, score_azul, total_azul,
            ganador, color_ganador, etiqueta_ganador
        )

        super().__init__(
            title='',
            content=content,
            size_hint=(None, None),
            size=(dp(820), dp(680)),
            separator_height=0,
            background='',
            auto_dismiss=False
        )

        with self.canvas.before:
            Color(*bg_ganador)
            self._bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(22)])
        self.bind(pos=self._upd_bg, size=self._upd_bg)

    def _upd_bg(self, *args):
        self._bg.pos = self.pos
        self._bg.size = self.size

    def _build_content(self, nombre_rojo, rounds_rojo, score_rojo, total_rojo,
                              nombre_azul, rounds_azul, score_azul, total_azul,
                              ganador, color_ganador, etiqueta_ganador):
        root = BoxLayout(orientation='vertical', spacing=dp(10), padding=[dp(28), dp(22)])

        # ── Título COMBATE FINALIZADO ──
        lbl_fin = Label(
            text="COMBATE FINALIZADO",
            font_size=sp(26),
            bold=True,
            color=(1, 1, 1, 0.7),
            size_hint_y=None,
            height=dp(36)
        )
        root.add_widget(lbl_fin)

        # ── Banner GANADOR ──
        winner_box = BoxLayout(size_hint_y=None, height=dp(110))
        with winner_box.canvas.before:
            Color(0.0, 0.0, 0.0, 0.35)
            winner_box._bg = RoundedRectangle(pos=winner_box.pos, size=winner_box.size, radius=[dp(14)])
        winner_box.bind(
            pos=lambda i, v: setattr(i._bg, 'pos', v),
            size=lambda i, v: setattr(i._bg, 'size', v)
        )

        inner = BoxLayout(orientation='vertical', padding=[dp(10), dp(8)])
        lbl_etiqueta = Label(
            text="GANADOR",
            font_size=sp(16),
            bold=True,
            color=(1, 1, 1, 0.55),
            size_hint_y=None,
            height=dp(22)
        )
        lbl_nombre_ganador = Label(
            text=f"{etiqueta_ganador}  {ganador}",
            font_size=sp(38),
            bold=True,
            color=color_ganador,
        )
        inner.add_widget(lbl_etiqueta)
        inner.add_widget(lbl_nombre_ganador)
        winner_box.add_widget(inner)
        root.add_widget(winner_box)

        # ── Tabla de puntajes ──
        lbl_tabla = Label(
            text="TABLA DE PUNTAJES",
            font_size=sp(14),
            bold=True,
            color=(0.6, 0.9, 1, 1),
            size_hint_y=None,
            height=dp(22)
        )
        root.add_widget(lbl_tabla)

        num_rounds = max(len(rounds_rojo), len(rounds_azul))
        # Rellenar con 0 si alguno tiene menos rounds guardados
        r_rojo = list(rounds_rojo) + [0] * (num_rounds - len(rounds_rojo))
        r_azul = list(rounds_azul) + [0] * (num_rounds - len(rounds_azul))

        cols = 1 + num_rounds + 1 + 1  # etiqueta + rounds + actual + total
        grid = GridLayout(
            cols=cols,
            size_hint_y=None,
            height=dp(105),
            spacing=[dp(3), dp(3)]
        )

        # Header
        self._cell(grid, "", (0.18, 0.18, 0.3, 1), (0.6, 0.6, 0.6, 1))
        for i in range(num_rounds):
            self._cell(grid, f"R{i+1}", (0.18, 0.18, 0.3, 1), (0.85, 0.85, 0.85, 1), bold=True)
        self._cell(grid, f"R{num_rounds+1}", (0.18, 0.18, 0.3, 1), (1, 0.9, 0.3, 1), bold=True)
        self._cell(grid, "TOTAL", (0.12, 0.12, 0.25, 1), (1, 0.85, 0.2, 1), bold=True)

        # Fila ROJO
        win_r = total_rojo > total_azul
        self._cell(grid, "ROJO", (0.55, 0.08, 0.08, 1), (1, 1, 1, 1), bold=True)
        for s in r_rojo:
            self._cell(grid, str(s), (0.45, 0.06, 0.06, 1), (1, 1, 1, 1))
        self._cell(grid, str(score_rojo), (0.45, 0.06, 0.06, 1), (1, 1, 0.4, 1), bold=True)
        total_color_r = (0.3, 1, 0.4, 1) if win_r else (1, 1, 1, 1)
        self._cell(grid, str(total_rojo), (0.38, 0.04, 0.04, 1), total_color_r, bold=True)

        # Fila AZUL
        win_a = total_azul > total_rojo
        self._cell(grid, "AZUL", (0.08, 0.22, 0.58, 1), (1, 1, 1, 1), bold=True)
        for s in r_azul:
            self._cell(grid, str(s), (0.08, 0.18, 0.48, 1), (1, 1, 1, 1))
        self._cell(grid, str(score_azul), (0.08, 0.18, 0.48, 1), (1, 1, 0.4, 1), bold=True)
        total_color_a = (0.3, 1, 0.4, 1) if win_a else (1, 1, 1, 1)
        self._cell(grid, str(total_azul), (0.05, 0.12, 0.40, 1), total_color_a, bold=True)

        root.add_widget(grid)

        # ── Diferencia de puntos ──
        diferencia = abs(total_rojo - total_azul)
        if ganador != "EMPATE":
            diff_text = f"Diferencia: {diferencia} punto{'s' if diferencia != 1 else ''}"
        else:
            diff_text = "Puntaje igualado — EMPATE"
        lbl_diff = Label(
            text=diff_text,
            font_size=sp(30),
            bold=True,
            color=(1, 0.9, 0.5, 1),
            size_hint_y=None,
            height=dp(30)
        )
        root.add_widget(lbl_diff)

        root.add_widget(BoxLayout(size_hint_y=0.05))

        # ── Botón cerrar ──
        btn_cerrar = Button(
            text="CERRAR",
            size_hint_y=None,
            height=dp(52),
            background_normal='',
            background_color=(0.2, 0.2, 0.35, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18)
        )
        btn_cerrar.bind(on_press=self._close)
        root.add_widget(btn_cerrar)

        return root

    def _cell(self, grid, text, bg, fg, bold=False):
        lbl = Label(text=text, font_size=sp(14), bold=bold, color=fg)
        with lbl.canvas.before:
            Color(*bg)
            lbl._r = Rectangle(pos=lbl.pos, size=lbl.size)
        lbl.bind(pos=lambda i, v: setattr(i._r, 'pos', v),
                 size=lambda i, v: setattr(i._r, 'size', v))
        grid.add_widget(lbl)

    def _close(self, *args):
        self.dismiss()
        if self.on_close_callback:
            Clock.schedule_once(lambda dt: self.on_close_callback(), 0.2)


# ------------------ PANEL CENTRAL CON CUENTA REGRESIVA ------------------
class CenterPanel(BoxLayout):
    time_str = StringProperty("03:00")
    round_str = StringProperty("Round 1")
    combat_started = BooleanProperty(False)

    def __init__(self, duracion_round=180, duracion_descanso=60, numero_rounds=3, **kwargs):
        super().__init__(**kwargs)
        self.timer_running = False
        self.round_number = 1
        self.numero_rounds = numero_rounds
        self.duracion_round = duracion_round
        self.duracion_descanso = duracion_descanso
        self.remaining_time = duracion_round
        self.is_rest_time = False
        self._rest_popup = None
        self.parent_screen = None

        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        self.orientation = 'vertical'
        self.spacing = dp(8)
        self.padding = [dp(10), dp(12)]

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Estado combate
        self.combat_status_label = Label(
            text="COMBATE NO INICIADO",
            font_size=ResponsiveHelper.get_font_size(13),
            color=(0.8, 0.2, 0.2, 1),
            bold=True,
            size_hint_y=None,
            height=dp(22)
        )
        self.add_widget(self.combat_status_label)

        # Round label
        self.round_label = Label(
            text=self.round_str,
            font_size=ResponsiveHelper.get_font_size(42),
            color=(0, 0, 0, 1),
            bold=True,
            size_hint_y=None,
            height=dp(58)
        )
        self.add_widget(self.round_label)

        # ── TIEMPO GRANDE ──
        time_container = BoxLayout(size_hint_y=None, height=dp(180))
        with time_container.canvas.before:
            Color(0.05, 0.05, 0.08, 1)
            time_container._bg = RoundedRectangle(pos=time_container.pos, size=time_container.size, radius=[dp(10)])
        time_container.bind(
            pos=lambda i, v: setattr(i._bg, 'pos', v),
            size=lambda i, v: setattr(i._bg, 'size', v)
        )

        self.time_label = Label(
            text=self.time_str,
            font_size=sp(144),
            color=(1, 0.85, 0.1, 1),
            bold=True,
        )
        self.bind(time_str=self.time_label.setter('text'))
        time_container.add_widget(self.time_label)
        self.add_widget(time_container)

        self.add_widget(BoxLayout(size_hint_y=0.05))

        # Botones PAUSA / INICIAR
        btn_row = BoxLayout(
            size_hint_y=None,
            height=ResponsiveHelper.get_button_height(),
            spacing=dp(6)
        )
        btn_pause = Button(
            text="PAUSA",
            on_press=lambda x: self.pause_timer(),
            background_normal='',
            background_color=(0.1, 0.4, 0.7, 1),
            color=(1, 1, 1, 1),
            font_size=ResponsiveHelper.get_font_size(20),
            bold=True
        )
        btn_row.add_widget(btn_pause)

        btn_play = Button(
            text="INICIAR",
            on_press=lambda x: self.start_timer(),
            background_normal='',
            background_color=(0.15, 0.65, 0.25, 1),
            color=(1, 1, 1, 1),
            font_size=ResponsiveHelper.get_font_size(20),
            bold=True
        )
        btn_row.add_widget(btn_play)
        self.add_widget(btn_row)

        self.add_widget(BoxLayout(size_hint_y=0.03))

        # Botón siguiente ronda
        self.next_round_button = Button(
            text="SIGUIENTE RONDA",
            size_hint_y=None,
            height=ResponsiveHelper.get_button_height(),
            background_normal='',
            background_color=(0.1, 0.4, 0.7, 1),
            color=(1, 1, 1, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            bold=True,
            on_press=self.show_next_round_confirmation
        )
        self.add_widget(self.next_round_button)

        # Botón finalizar
        self.end_button = Button(
            text="FINALIZAR COMBATE",
            size_hint_y=None,
            height=ResponsiveHelper.get_button_height(),
            background_normal='',
            background_color=(0.1, 0.4, 0.7, 1),
            color=(1, 1, 1, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            bold=True,
            on_press=self.show_end_combat_confirmation
        )
        self.add_widget(self.end_button)

        # Botón tiempo médico
        self.medical_button = Button(
            text="TIEMPO MÉDICO",
            size_hint_y=None,
            height=ResponsiveHelper.get_button_height(),
            background_normal='',
            background_color=(0.7, 0.5, 0.05, 1),
            color=(1, 1, 1, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            bold=True,
            on_press=self.show_medical_time_selector
        )
        self.add_widget(self.medical_button)

        # Botón salir
        self.back_button = Button(
            text="SALIR",
            size_hint_y=None,
            height=ResponsiveHelper.get_button_height(),
            background_normal='',
            background_color=(0.7, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            bold=True,
            on_press=self.go_back
        )
        self.add_widget(self.back_button)

        self.add_widget(BoxLayout(size_hint_y=0.1))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def show_medical_time_selector(self, instance):
        self.pause_timer()

        content = BoxLayout(orientation='vertical', spacing=dp(14), padding=dp(22))

        lbl = Label(
            text="¿Para qué atleta es\nel tiempo médico?",
            font_size=sp(20),
            bold=True,
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(60)
        )
        lbl.bind(size=lbl.setter('text_size'))
        content.add_widget(lbl)

        popup_size = (dp(400), dp(230))
        sel_popup = Popup(
            title='',
            content=content,
            size_hint=(None, None),
            size=popup_size,
            separator_height=0,
            background='',
            auto_dismiss=False
        )
        with sel_popup.canvas.before:
            Color(0.08, 0.08, 0.14, 0.97)
            sel_popup._bg = RoundedRectangle(pos=sel_popup.pos, size=sel_popup.size, radius=[dp(16)])
        sel_popup.bind(
            pos=lambda i, v: setattr(i._bg, 'pos', v),
            size=lambda i, v: setattr(i._bg, 'size', v)
        )

        btn_row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(10))

        btn_rojo = Button(
            text="ROJO",
            background_normal='',
            background_color=(0.75, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18)
        )
        btn_azul = Button(
            text="AZUL",
            background_normal='',
            background_color=(0.1, 0.35, 0.8, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18)
        )

        def open_medical(color):
            sel_popup.dismiss()
            athlete_name = ""
            if self.parent_screen:
                if color == 'rojo':
                    athlete_name = self.parent_screen.com1_panel.name
                else:
                    athlete_name = self.parent_screen.com2_panel.name

            def _open(dt):
                med = MedicalTimePopup(
                    athlete_name=athlete_name,
                    athlete_color=color,
                    on_result_callback=self.on_medical_result
                )
                med.open()
                self.combat_status_label.text = "TIEMPO MÉDICO"
                self.combat_status_label.color = (1, 0.75, 0.1, 1)

            Clock.schedule_once(_open, 0.25)

        btn_rojo.bind(on_press=lambda x: open_medical('rojo'))
        btn_azul.bind(on_press=lambda x: open_medical('azul'))
        btn_row.add_widget(btn_rojo)
        btn_row.add_widget(btn_azul)
        content.add_widget(btn_row)

        btn_cancel = Button(
            text="Cancelar",
            size_hint_y=None,
            height=dp(34),
            background_normal='',
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 0.8),
            font_size=sp(14)
        )
        btn_cancel.bind(on_press=sel_popup.dismiss)
        content.add_widget(btn_cancel)
        sel_popup.open()

    def on_medical_result(self, result, athlete_color, athlete_name):
        print(f"[CenterPanel] Resultado médico: {result} — {athlete_name} ({athlete_color})")

        if result == 'continuar':
            self.combat_status_label.text = "LISTO PARA INICIAR"
            self.combat_status_label.color = (0.2, 0.7, 0.2, 1)
            self.mostrar_mensaje(
                titulo="Tiempo Médico",
                mensaje=f"{athlete_name} continúa\nel combate"
            )

        elif result == 'abandono':
            self.pause_timer()
            self.combat_started = False
            self.time_str = "FIN"
            self.time_label.text = self.time_str
            self.round_label.text = "ABANDONO"
            self.combat_status_label.text = "COMBATE TERMINADO"
            self.combat_status_label.color = (0.8, 0.5, 0.1, 1)
            winner_color = "AZUL" if athlete_color == 'rojo' else "ROJO"
            self.mostrar_mensaje(
                titulo="Abandono",
                mensaje=f"{athlete_name} abandona el combate.\n\n Gana el atleta {winner_color}"
            )

        elif result == 'descalificacion':
            self.pause_timer()
            self.combat_started = False
            self.time_str = "FIN"
            self.time_label.text = self.time_str
            self.round_label.text = "DESCALIFICACIÓN"
            self.combat_status_label.text = "COMBATE TERMINADO"
            self.combat_status_label.color = (0.8, 0.2, 0.2, 1)
            winner_color = "AZUL" if athlete_color == 'rojo' else "ROJO"
            self.mostrar_mensaje(
                titulo="Descalificación",
                mensaje=f"{athlete_name} ha sido descalificado.\n\nGana el atleta {winner_color}"
            )

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.combat_started = True
            self.combat_status_label.text = "COMBATE EN CURSO"
            self.combat_status_label.color = (0.2, 0.7, 0.2, 1)
            Clock.schedule_interval(self.update_time, 1)
            print("[CenterPanel] Timer iniciado - Combate ACTIVO")
            if self.parent_screen:
                self.parent_screen.on_combat_started()

    def pause_timer(self):
        self.timer_running = False
        Clock.unschedule(self.update_time)
        if self.combat_started:
            self.combat_status_label.text = "COMBATE PAUSADO"
            self.combat_status_label.color = (0.8, 0.6, 0, 1)
        print("[CenterPanel] Timer pausado")

    def is_combat_active(self):
        return self.combat_started

    def is_timer_running(self):
        return self.timer_running

    def update_time(self, dt):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.time_str = f"{minutes:02}:{seconds:02}"
        else:
            self.pause_timer()
            self._on_round_ended()

    def _on_round_ended(self):
        print(f"[CenterPanel] Round {self.round_number} terminado")

        if self.parent_screen:
            self.parent_screen.save_round_scores()

        if self.round_number >= self.numero_rounds:
            self.end_combat_automatically()
            return

        self.combat_started = False
        self.is_rest_time = True
        self.combat_status_label.text = "DESCANSO"
        self.combat_status_label.color = (0.8, 0.6, 0, 1)

        round_scores = {}
        if self.parent_screen:
            round_scores = {
                'rojo': list(self.parent_screen.com1_panel.round_scores),
                'azul': list(self.parent_screen.com2_panel.round_scores),
            }

        self._rest_popup = RestPopup(
            round_number=self.round_number,
            duracion_descanso=self.duracion_descanso,
            on_rest_end_callback=self._after_rest,
            round_scores=round_scores
        )
        self._rest_popup.open()

    def _after_rest(self):
        self.start_new_round()

    def start_new_round(self):
        if self.round_number >= self.numero_rounds:
            self.end_combat_automatically()
            return

        self.round_number += 1
        self.round_str = f"Round {self.round_number}"
        self.round_label.text = self.round_str
        self.is_rest_time = False
        self.combat_started = False
        self.remaining_time = self.duracion_round
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.time_str = f"{minutes:02}:{seconds:02}"
        self.combat_status_label.text = "LISTO PARA INICIAR"
        self.combat_status_label.color = (0.8, 0.6, 0, 1)

        if self.parent_screen:
            self.parent_screen.reset_competitor_scores()

        print(f"[CenterPanel] Round {self.round_number} listo - Presiona INICIAR")

    def end_combat_automatically(self):
        """Finaliza el combate automáticamente y muestra el popup con el ganador."""
        self.pause_timer()
        self.combat_started = False
        self.is_rest_time = False
        self.time_str = "FIN"
        self.time_label.text = self.time_str
        self.round_label.text = "Combate Finalizado"
        self.combat_status_label.text = "COMBATE FINALIZADO"
        self.combat_status_label.color = (0.5, 0.5, 0.5, 1)
        print(f"[CenterPanel] Combate finalizado - {self.numero_rounds} rounds completados")

        # Mostrar popup de resultado final con ganador
        if self.parent_screen:
            self._show_final_result_popup()
        else:
            self.mostrar_mensaje(
                titulo="Combate Finalizado",
                mensaje=f"Se han completado los {self.numero_rounds} rounds\n\nEl combate ha finalizado"
            )

    def _show_final_result_popup(self):
        """Construye y abre el FinalResultPopup con los datos reales."""
        ps = self.parent_screen
        nombre_rojo   = ps.com1_panel.name
        rounds_rojo   = list(ps.com1_panel.round_scores)
        score_rojo    = ps.com1_panel.api_score

        nombre_azul   = ps.com2_panel.name
        rounds_azul   = list(ps.com2_panel.round_scores)
        score_azul    = ps.com2_panel.api_score

        popup = FinalResultPopup(
            nombre_rojo=nombre_rojo,
            score_rojo=score_rojo,
            rounds_rojo=rounds_rojo,
            nombre_azul=nombre_azul,
            score_azul=score_azul,
            rounds_azul=rounds_azul,
        )
        popup.open()

    def end_combat_by_disqualification(self, player_name):
        self.pause_timer()
        self.combat_started = False
        self.time_str = "FIN"
        self.time_label.text = self.time_str
        self.round_label.text = "DESCALIFICACIÓN"
        self.combat_status_label.text = "COMBATE TERMINADO"
        self.combat_status_label.color = (0.8, 0.2, 0.2, 1)

    def mostrar_mensaje(self, titulo, mensaje, confirm_callback=None):
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        lbl = Label(
            text=mensaje,
            color=(0.1, 0.4, 0.7, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80)
        )
        lbl.bind(size=lbl.setter('text_size'))
        content.add_widget(lbl)

        btn_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=ResponsiveHelper.get_button_height())
        popup_size = ResponsiveHelper.get_popup_size()
        popup = Popup(
            title=titulo,
            title_color=(1, 1, 1, 1),
            title_size=ResponsiveHelper.get_font_size(22),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=popup_size,
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
                font_size=ResponsiveHelper.get_font_size(16)
            )
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
            font_size=ResponsiveHelper.get_font_size(16)
        )
        if confirm_callback:
            btn_aceptar.bind(on_press=lambda x: [popup.dismiss(), confirm_callback()])
        else:
            btn_aceptar.bind(on_press=popup.dismiss)
        btn_layout.add_widget(btn_aceptar)
        content.add_widget(btn_layout)

        with popup.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            popup.rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(15)])
        popup.bind(
            pos=lambda i, v: setattr(i.rect, 'pos', v),
            size=lambda i, v: setattr(i.rect, 'size', v)
        )
        popup.open()

    def show_next_round_confirmation(self, instance):
        if self.round_number >= self.numero_rounds:
            self.mostrar_mensaje(
                titulo="Máximo de Rondas",
                mensaje=f"Ya estás en la ronda {self.numero_rounds}\n(última ronda configurada)"
            )
            return
        self.mostrar_mensaje(
            titulo="Confirmar Siguiente Ronda",
            mensaje="¿Estás seguro de avanzar\na la siguiente ronda?",
            confirm_callback=lambda: self.next_round(instance)
        )

    def show_end_combat_confirmation(self, instance):
        self.mostrar_mensaje(
            titulo="Finalizar Combate",
            mensaje="¿Confirmas que deseas\nfinalizar el combate?",
            confirm_callback=lambda: self.end_combat(instance)
        )

    def next_round(self, instance):
        if self.parent_screen:
            self.parent_screen.save_round_scores()

        self.round_number += 1
        self.round_str = f"Round {self.round_number}"
        self.round_label.text = self.round_str
        self.remaining_time = self.duracion_round
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.time_str = f"{minutes:02}:{seconds:02}"
        self.is_rest_time = False
        self.pause_timer()

        if self.parent_screen:
            self.parent_screen.reset_competitor_scores()

        self.mostrar_mensaje(
            titulo="Ronda Actualizada",
            mensaje=f"Has avanzado a la\nronda {self.round_number}"
        )

    def end_combat(self, instance):
        """Finalizar combate manualmente — también muestra el popup de ganador."""
        self.pause_timer()
        self.combat_started = False
        self.time_str = "FIN"
        self.time_label.text = self.time_str
        self.round_label.text = "Combate Finalizado"
        self.combat_status_label.text = "COMBATE FINALIZADO"
        self.combat_status_label.color = (0.5, 0.5, 0.5, 1)

        # Guardar puntaje del round actual antes de mostrar resultado
        if self.parent_screen:
            self.parent_screen.save_round_scores()
            self._show_final_result_popup()
        else:
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
        self.parent.parent.parent.current = 'ini'


# ------------------ PANTALLA PRINCIPAL CON WEBSOCKET ------------------
class MainScreentabc(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'tablero_central'
        self.combate_id = None
        self.id_alumno_rojo = None
        self.id_alumno_azul = None
        self.ws = None
        self.ws_thread = None
        self.ws_keepalive = None
        self.build_ui()

    def set_competitors(self, name1, nat1, name2, nat2, combate_data=None):
        print("\n" + "=" * 60)
        print("[MainScreentabc] CONFIGURANDO COMPETIDORES")
        print(f"Rojo: {name1} ({nat1})")
        print(f"Azul: {name2} ({nat2})")

        if combate_data:
            self.combate_id = combate_data.get('idCombate') or combate_data.get('id')
            self.id_alumno_rojo = combate_data.get('idAlumnoRojo')
            self.id_alumno_azul = combate_data.get('idAlumnoAzul')
            duracion_round = self.parse_time_to_seconds(combate_data.get('duracionRound', '00:03:00'))
            duracion_descanso = self.parse_time_to_seconds(combate_data.get('duracionDescanso', '00:01:00'))
            numero_rounds = combate_data.get('numeroRounds', 3)
        else:
            duracion_round = 180
            duracion_descanso = 60
            numero_rounds = 3

        self.rebuild_with_data(name1, nat1, name2, nat2, duracion_round, duracion_descanso, numero_rounds)

        if self.combate_id and WEBSOCKET_AVAILABLE:
            self.connect_websocket()

    def parse_time_to_seconds(self, time_str):
        try:
            parts = time_str.split(':')
            hours = int(parts[0]) if len(parts) > 0 else 0
            minutes = int(parts[1]) if len(parts) > 1 else 0
            seconds = int(parts[2]) if len(parts) > 2 else 0
            return hours * 3600 + minutes * 60 + seconds
        except:
            return 180

    def rebuild_with_data(self, name1, nat1, name2, nat2, duracion_round, duracion_descanso, numero_rounds):
        self.clear_widgets()
        orientation = ResponsiveHelper.get_layout_orientation()
        main_layout = BoxLayout(orientation=orientation, spacing=0)

        # ── ROJO a la IZQUIERDA ──
        self.com1_panel = CompetitorPanel(
            name=name1, color="#E53935",
            nationality=nat1,
            alumno_id=self.id_alumno_rojo,
            combate_id=self.combate_id
        )
        self.com1_panel.parent_screen = self
        main_layout.add_widget(self.com1_panel)

        self.center_panel = CenterPanel(
            duracion_round=duracion_round,
            duracion_descanso=duracion_descanso,
            numero_rounds=numero_rounds
        )
        self.center_panel.parent_screen = self
        main_layout.add_widget(self.center_panel)

        # ── AZUL a la DERECHA ──
        self.com2_panel = CompetitorPanel(
            name=name2, color="#1E88E5",
            nationality=nat2,
            alumno_id=self.id_alumno_azul,
            combate_id=self.combate_id
        )
        self.com2_panel.parent_screen = self
        main_layout.add_widget(self.com2_panel)

        self.add_widget(main_layout)

    def is_timer_active(self):
        if hasattr(self, 'center_panel') and self.center_panel:
            return self.center_panel.is_combat_active() and not self.center_panel.is_rest_time
        return False

    def on_combat_started(self):
        print("[MainScreentabc] Combate iniciado")
        self.fetch_initial_gamjeom()

    def on_player_disqualified(self, alumno_id, player_name):
        print(f"\n{'='*60}\nDESCALIFICACIÓN: {player_name}\n{'='*60}\n")
        if alumno_id == self.id_alumno_rojo:
            winner = self.com2_panel.name
        else:
            winner = self.com1_panel.name
        self.center_panel.end_combat_by_disqualification(player_name)
        self.center_panel.mostrar_mensaje(
            titulo="DESCALIFICACIÓN",
            mensaje=f"{player_name} ha sido descalificado\npor acumular 3 faltas GAM-JEOM.\n\nGanador: {winner}"
        )

    def save_round_scores(self):
        if hasattr(self, 'com1_panel'):
            self.com1_panel.save_round_score()
        if hasattr(self, 'com2_panel'):
            self.com2_panel.save_round_score()

    def connect_websocket(self):
        if not WEBSOCKET_AVAILABLE:
            return

        def on_message(ws, message):
            try:
                data = json.loads(message)
                if data.get('event') == 'score_update':
                    alumno_id = data.get('alumnoId')
                    new_count = data.get('count', 0)
                    if not self.is_timer_active():
                        self.revert_score(alumno_id)
                        return
                    if alumno_id == self.id_alumno_rojo:
                        self.com1_panel.update_api_score(new_count)
                    elif alumno_id == self.id_alumno_azul:
                        self.com2_panel.update_api_score(new_count)
                elif data.get('status') == 'connected':
                    self.fetch_initial_scores()
            except Exception as e:
                print(f"[WebSocket] ✗ Error: {e}")

        def on_error(ws, error):
            print(f"[WebSocket] ✗ Error: {error}")

        def on_close(ws, close_status_code, close_msg):
            print(f"[WebSocket] ✗ Cerrado")
            if self.ws_keepalive:
                Clock.schedule_once(lambda dt: self.reconnect_websocket(), 3)

        def on_open(ws):
            print(f"[WebSocket] ✓ Conectado al combate {self.combate_id}")
            self.start_keepalive()

        ws_url = f"ws://localhost:8080/ws/tablero/{self.combate_id}"
        self.ws = websocket.WebSocketApp(ws_url, on_message=on_message,
                                          on_error=on_error, on_close=on_close, on_open=on_open)
        self.ws_thread = Thread(target=self.ws.run_forever, daemon=True)
        self.ws_thread.start()

    def revert_score(self, alumno_id):
        def work():
            try:
                url = f"http://localhost:8080/apiPuntajes/puntaje/alumno/{alumno_id}/last"
                requests.delete(url, timeout=5)
            except:
                pass
        Thread(target=work, daemon=True).start()

    def start_keepalive(self):
        def send_ping(dt):
            if self.ws and self.ws.sock and self.ws.sock.connected:
                try:
                    self.ws.send('ping')
                except:
                    pass
        if self.ws_keepalive:
            self.ws_keepalive.cancel()
        self.ws_keepalive = Clock.schedule_interval(send_ping, 30)

    def reconnect_websocket(self):
        if self.combate_id and WEBSOCKET_AVAILABLE:
            self.connect_websocket()

    @mainthread
    def update_judges_status(self, text):
        if hasattr(self, 'center_panel') and self.center_panel:
            self.center_panel.mostrar_mensaje(titulo="Estado de Jueces", mensaje=text)

    def fetch_initial_scores(self):
        def work():
            try:
                if self.id_alumno_rojo:
                    r = requests.get(f"http://localhost:8080/apiPuntajes/puntaje/alumno/{self.id_alumno_rojo}/count", timeout=2)
                    if r.status_code == 200:
                        self.com1_panel.update_api_score(r.json().get('count', 0))
                if self.id_alumno_azul:
                    r = requests.get(f"http://localhost:8080/apiPuntajes/puntaje/alumno/{self.id_alumno_azul}/count", timeout=2)
                    if r.status_code == 200:
                        self.com2_panel.update_api_score(r.json().get('count', 0))
            except:
                pass
        Thread(target=work, daemon=True).start()

    def fetch_initial_gamjeom(self):
        def work():
            try:
                if self.id_alumno_rojo and self.combate_id:
                    r = requests.get(f"http://localhost:8080/apiGamJeom/falta/alumno/{self.id_alumno_rojo}/combate/{self.combate_id}/count", timeout=2)
                    if r.status_code == 200:
                        self.com1_panel.update_gamjeom_count(r.json().get('count', 0))
                if self.id_alumno_azul and self.combate_id:
                    r = requests.get(f"http://localhost:8080/apiGamJeom/falta/alumno/{self.id_alumno_azul}/combate/{self.combate_id}/count", timeout=2)
                    if r.status_code == 200:
                        self.com2_panel.update_gamjeom_count(r.json().get('count', 0))
            except:
                pass
        Thread(target=work, daemon=True).start()

    def pausar_tiempo(self):
        if hasattr(self, 'center_panel') and self.center_panel:
            self.center_panel.pause_timer()

    def mostrar_popup_incidencia(self):
        content = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(30))
        lbl = Label(
            text="INCIDENCIA REPORTADA\n\n2 o más jueces confirmaron\nuna incidencia",
            color=(0, 0, 0, 1),
            font_size=sp(24),
            halign='center',
            valign='middle',
            bold=True,
            size_hint_y=None,
            height=dp(140)
        )
        lbl.bind(size=lbl.setter('text_size'))
        content.add_widget(lbl)
        btn = Button(
            text='CONTINUAR',
            background_normal='',
            background_color=(1, 0.8, 0, 1),
            color=(0, 0, 0, 1),
            bold=True,
            font_size=sp(20),
            size_hint_y=None,
            height=dp(60)
        )
        content.add_widget(btn)
        popup = Popup(
            title=" ALERTA ",
            title_color=(0, 0, 0, 1),
            title_size=sp(24),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=(dp(500), dp(380)),
            separator_height=0,
            background='',
            auto_dismiss=False
        )
        with popup.canvas.before:
            Color(1, 0.9, 0.3, 0.98)
            popup.rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(15)])
        popup.bind(
            pos=lambda i, v: setattr(i.rect, 'pos', v),
            size=lambda i, v: setattr(i.rect, 'size', v)
        )
        btn.bind(on_press=popup.dismiss)
        popup.open()

    def reanudar_tiempo(self):
        if hasattr(self, 'center_panel') and self.center_panel:
            self.center_panel.start_timer()

    def disconnect_websocket(self):
        if self.ws_keepalive:
            self.ws_keepalive.cancel()
            self.ws_keepalive = None
        if self.ws:
            try:
                self.ws.close()
            except:
                pass

    def reset_competitor_scores(self):
        self.com1_panel.reset_scores()
        self.com2_panel.reset_scores()

    def notify_judge(self, judge_name, panel='both', auto_reset_seconds=3):
        if panel in ('rojo', 'both') and hasattr(self, 'com1_panel'):
            self.com1_panel.set_judge_active(judge_name, True, auto_reset_seconds)
        if panel in ('azul', 'both') and hasattr(self, 'com2_panel'):
            self.com2_panel.set_judge_active(judge_name, True, auto_reset_seconds)
        print(f"[MainScreentabc] LED {judge_name} activado (panel={panel})")

    def build_ui(self):
        self.clear_widgets()
        orientation = ResponsiveHelper.get_layout_orientation()
        main_layout = BoxLayout(orientation=orientation, spacing=0)

        # ROJO izquierda
        self.com1_panel = CompetitorPanel(name="COMPETIDOR ROJO", color="#E53935", nationality="")
        self.com1_panel.parent_screen = self
        main_layout.add_widget(self.com1_panel)

        self.center_panel = CenterPanel()
        self.center_panel.parent_screen = self
        main_layout.add_widget(self.center_panel)

        # AZUL derecha
        self.com2_panel = CompetitorPanel(name="COMPETIDOR AZUL", color="#1E88E5", nationality="")
        self.com2_panel.parent_screen = self
        main_layout.add_widget(self.com2_panel)

        self.add_widget(main_layout)

    def on_pre_leave(self, *args):
        self.disconnect_websocket()
        return super().on_pre_leave(*args)


# ------------------ APP DE PRUEBA ------------------
if __name__ == '__main__':
    class TestApp(App):
        def build(self):
            sm = ScreenManager()
            tablero = MainScreentabc(name='tablero_central')
            sm.add_widget(tablero)

            def simulate_combat_creation(dt):
                print("\n" + "=" * 60)
                print("SIMULACIÓN DE COMBATE")
                print("=" * 60)
                combate_data = {
                    'idCombate': 1,
                    'id': 1,
                    'idAlumnoRojo': 1,
                    'idAlumnoAzul': 2,
                    'duracionRound': '00:01:00',
                    'duracionDescanso': '00:00:15',
                    'numeroRounds': 3
                }
                tablero.set_competitors(
                    name1="Juan Pérez",
                    nat1="MEX",
                    name2="Kim Min-ho",
                    nat2="KOR",
                    combate_data=combate_data
                )
                print("\n✅ TABLERO CONFIGURADO")
                print("  🔴 ROJO (Juan Pérez)  - IZQUIERDA")
                print("  🔵 AZUL (Kim Min-ho)  - DERECHA")
                print("  IMPORTANTE: Presiona INICIAR para que cuenten los puntos")
                print("  Al terminar el último round → Popup con GANADOR automático")
                print("=" * 60 + "\n")

            Clock.schedule_once(simulate_combat_creation, 2)
            return sm

    TestApp().run()