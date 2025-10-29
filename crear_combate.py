from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.widget import Widget
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty
from kivy.utils import platform
from datetime import datetime, date
import calendar


# ------------------ UTILIDADES RESPONSIVE ------------------
class ResponsiveHelper:
    @staticmethod
    def is_mobile():
        return platform in ['android', 'ios']
    
    @staticmethod
    def is_desktop():
        return platform in ['win', 'linux', 'macosx']
    
    @staticmethod
    def get_form_width():
        width = Window.width
        if width < 600:
            return 0.95
        elif width < 900:
            return 0.85
        elif width < 1200:
            return 0.75
        else:
            return 0.65
    
    @staticmethod
    def get_font_size(base_size):
        width = Window.width
        if width < 600:
            return sp(base_size * 0.8)
        elif width < 900:
            return sp(base_size * 0.9)
        return sp(base_size)
    
    @staticmethod
    def get_popup_size():
        width = Window.width
        height = Window.height
        if width < 600:
            return (width * 0.9, min(height * 0.5, dp(350)))
        else:
            return (min(width * 0.7, dp(500)), min(height * 0.5, dp(400)))


# ------------------ SELECTORES RESPONSIVE ------------------
class DateSelector(BoxLayout):
    selected_date = ObjectProperty(date.today())
    
    def __init__(self, initial_date=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(55)
        
        if initial_date:
            try:
                day, month, year = map(int, initial_date.split('/'))
                initial_date = date(year, month, day)
            except:
                initial_date = date.today()
        else:
            initial_date = date.today()
        
        current_year = initial_date.year
        self.year_spinner = Spinner(
            text=str(current_year),
            values=[str(y) for y in range(current_year - 100, current_year + 1)],
            size_hint=(0.3, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1)
        )
        
        meses_espanol = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        self.month_spinner = Spinner(
            text=meses_espanol[initial_date.month - 1],
            values=meses_espanol,
            size_hint=(0.4, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        self.day_spinner = Spinner(
            text=str(initial_date.day),
            values=[],
            size_hint=(0.3, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        self.add_widget(self.day_spinner)
        self.add_widget(self.month_spinner)
        self.add_widget(self.year_spinner)
        
        self.update_days()
        self.month_spinner.bind(text=self.update_days_on_change)
        self.year_spinner.bind(text=self.update_days_on_change)
        Window.bind(on_resize=self.on_window_resize)
        
    def on_window_resize(self, instance, width, height):
        for spinner in [self.year_spinner, self.month_spinner, self.day_spinner]:
            spinner.font_size = ResponsiveHelper.get_font_size(18)
        
    def update_days_on_change(self, *args):
        self.update_days()
        self.get_selected_date()
        
    def update_days(self):
        month = self.month_spinner.text
        year = self.year_spinner.text
        
        if month and year:
            meses_espanol = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                           "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            month_num = meses_espanol.index(month) + 1
            year_num = int(year)
            _, num_days = calendar.monthrange(year_num, month_num)
            
            current_day = int(self.day_spinner.text) if self.day_spinner.text.isdigit() else 1
            days = [str(d) for d in range(1, num_days + 1)]
            self.day_spinner.values = days
            
            if str(current_day) not in days:
                current_day = 1
            self.day_spinner.text = str(current_day)
            
    def get_selected_date(self):
        try:
            meses_espanol = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                           "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            month_num = meses_espanol.index(self.month_spinner.text) + 1
            day = int(self.day_spinner.text)
            year = int(self.year_spinner.text)
            self.selected_date = date(year, month_num, day)
            return self.selected_date
        except:
            return date.today()
            
    def get_formatted_date(self):
        selected_date = self.get_selected_date()
        return selected_date.strftime("%d/%m/%Y")


class TimeSelector(BoxLayout):
    selected_time = ObjectProperty(None)
    
    def __init__(self, initial_time=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(55)
        
        if initial_time:
            try:
                hour, minute = map(int, initial_time.split(':'))
                initial_time = datetime.now().replace(hour=hour, minute=minute).time()
            except:
                initial_time = datetime.now().time()
        else:
            initial_time = datetime.now().time()
        
        self.hour_spinner = Spinner(
            text=f"{initial_time.hour:02d}",
            values=[f"{h:02d}" for h in range(0, 24)],
            size_hint=(0.45, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        minute = (initial_time.minute // 5) * 5
        self.minute_spinner = Spinner(
            text=f"{minute:02d}",
            values=[f"{m:02d}" for m in range(0, 60, 5)],
            size_hint=(0.45, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        self.add_widget(self.hour_spinner)
        self.add_widget(Label(text=":", size_hint=(0.1, 1), 
                             font_size=ResponsiveHelper.get_font_size(24),
                             color=(0.1, 0.4, 0.7, 1)))
        self.add_widget(self.minute_spinner)
        
        self.get_selected_time()
        self.hour_spinner.bind(text=self.update_time)
        self.minute_spinner.bind(text=self.update_time)
        Window.bind(on_resize=self.on_window_resize)
        
    def on_window_resize(self, instance, width, height):
        self.hour_spinner.font_size = ResponsiveHelper.get_font_size(18)
        self.minute_spinner.font_size = ResponsiveHelper.get_font_size(18)
        
    def update_time(self, *args):
        self.get_selected_time()
        
    def get_selected_time(self):
        try:
            hour = int(self.hour_spinner.text)
            minute = int(self.minute_spinner.text)
            self.selected_time = datetime.now().replace(hour=hour, minute=minute).time()
            return self.selected_time
        except:
            return datetime.now().time()
            
    def get_formatted_time(self):
        selected_time = self.get_selected_time()
        return selected_time.strftime("%H:%M")


class RoundsSelector(BoxLayout):
    selected_rounds = ObjectProperty(3)
    
    def __init__(self, initial_rounds=3, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(5)
        self.size_hint = (1, None)
        self.height = dp(55)
       
        self.rounds_spinner = Spinner(
            text=str(initial_rounds),
            values=[str(r) for r in range(1, 6)],
            size_hint=(1, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        self.add_widget(self.rounds_spinner)
        self.get_selected_rounds()
        self.rounds_spinner.bind(text=self.update_rounds)
        Window.bind(on_resize=self.on_window_resize)
        
    def on_window_resize(self, instance, width, height):
        self.rounds_spinner.font_size = ResponsiveHelper.get_font_size(18)
        
    def update_rounds(self, *args):
        self.get_selected_rounds()
        
    def get_selected_rounds(self):
        try:
            self.selected_rounds = int(self.rounds_spinner.text)
            return self.selected_rounds
        except:
            return 3


class DurationSelector(BoxLayout):
    selected_minutes = ObjectProperty(0)
    selected_seconds = ObjectProperty(0)
    
    def __init__(self, initial_minutes=3, initial_seconds=0, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(55)
        
        self.minutes_spinner = Spinner(
            text=str(initial_minutes),
            values=[str(m) for m in range(0, 11)],
            size_hint=(0.3, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        self.add_widget(self.minutes_spinner)
        self.add_widget(Label(text="min", size_hint=(0.15, 1), 
                             font_size=ResponsiveHelper.get_font_size(14),
                             color=(0.1, 0.4, 0.7, 1)))
        
        self.seconds_spinner = Spinner(
            text=f"{initial_seconds:02d}",
            values=[f"{s:02d}" for s in range(0, 60, 5)],
            size_hint=(0.3, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        self.add_widget(self.seconds_spinner)
        self.add_widget(Label(text="seg", size_hint=(0.15, 1), 
                             font_size=ResponsiveHelper.get_font_size(14),
                             color=(0.1, 0.4, 0.7, 1)))
        
        self.get_selected_duration()
        self.minutes_spinner.bind(text=self.update_duration)
        self.seconds_spinner.bind(text=self.update_duration)
        Window.bind(on_resize=self.on_window_resize)
        
    def on_window_resize(self, instance, width, height):
        self.minutes_spinner.font_size = ResponsiveHelper.get_font_size(18)
        self.seconds_spinner.font_size = ResponsiveHelper.get_font_size(18)
        
    def update_duration(self, *args):
        self.get_selected_duration()
        
    def get_selected_duration(self):
        try:
            self.selected_minutes = int(self.minutes_spinner.text)
            self.selected_seconds = int(self.seconds_spinner.text)
            return self.selected_minutes * 60 + self.selected_seconds
        except:
            return 0
            
    def get_formatted_duration(self):
        return f"{self.selected_minutes}:{self.selected_seconds:02d}"


class CategoriaPesoSelector(BoxLayout):
    selected_category = ObjectProperty("")
    
    def __init__(self, initial_category="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(55)
        
        categorias = ["Fin", "Fly", "Bantam", "Feather", "Light", "Welter", "Middle", "Heavy"]
        
        self.category_spinner = Spinner(
            text=initial_category if initial_category else categorias[0],
            values=categorias,
            size_hint=(1, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        self.add_widget(self.category_spinner)
        self.get_selected_category()
        self.category_spinner.bind(text=self.update_category)
        Window.bind(on_resize=self.on_window_resize)
        
    def on_window_resize(self, instance, width, height):
        self.category_spinner.font_size = ResponsiveHelper.get_font_size(18)
        
    def update_category(self, *args):
        self.get_selected_category()
        
    def get_selected_category(self):
        self.selected_category = self.category_spinner.text
        return self.selected_category


class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
            Color(0.1, 0.4, 0.7, 0.9)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
            Color(1, 1, 1, 0.3)
            self.border_rect = RoundedRectangle(
                pos=(self.pos[0]+dp(2), self.pos[1]+dp(2)),
                size=(self.size[0]-dp(4), self.size[1]-dp(4)),
                radius=[dp(10)])

        self.bind(pos=self._update_rects, size=self._update_rects)
        Window.bind(on_resize=self.on_window_resize)

    def _update_rects(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_rect.pos = (self.pos[0]+dp(2), self.pos[1]+dp(2))
        self.border_rect.size = (self.size[0]-dp(4), self.size[1]-dp(4))
    
    def on_window_resize(self, instance, width, height):
        self.font_size = ResponsiveHelper.get_font_size(18)

    def on_focus(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            if value:
                Color(0.2, 0.5, 0.9, 1)
                self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
                Color(1, 1, 1, 0.5)
            else:
                Color(0.1, 0.4, 0.7, 0.9)
                self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
                Color(1, 1, 1, 0.3)
            self.border_rect = RoundedRectangle(
                pos=(self.pos[0]+dp(2), self.pos[1]+dp(2)),
                size=(self.size[0]-dp(4), self.size[1]-dp(4)),
                radius=[dp(10)])
        if not value:
            self._update_rects()


class HoverButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.1, 0.4, 0.7, 1)
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


class CrearCombateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        Window.bind(on_resize=self.on_window_resize)

    def build_ui(self):
        self.clear_widgets()
        
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False, bar_width=dp(10), scroll_type=['bars', 'content'])
        
        main_layout = BoxLayout(orientation='vertical', padding=[dp(20), dp(30), dp(20), dp(30)], 
                               spacing=dp(15), size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))

        with main_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.background_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self.update_background, pos=self.update_background)

        main_layout.add_widget(Widget(size_hint_y=None, height=max(dp(15), Window.height * 0.02)))

        form_container = BoxLayout(orientation='vertical', size_hint=(ResponsiveHelper.get_form_width(), None),
                                  pos_hint={'center_x': 0.5}, spacing=dp(12))
        form_container.bind(minimum_height=form_container.setter('height'))

        logo = Image(source="Imagen5-Photoroom.png", size_hint=(1, None), 
                    height=min(dp(100), Window.height * 0.12), allow_stretch=True, keep_ratio=True)
        form_container.add_widget(logo)

        titulo = Label(text='CREAR COMBATE', font_size=ResponsiveHelper.get_font_size(32),
                      color=(0.1, 0.4, 0.7, 1), bold=True, size_hint_y=None, height=dp(60))
        form_container.add_widget(titulo)
        form_container.add_widget(Widget(size_hint_y=None, height=dp(10)))

        def crear_campo(texto, hint_text=None, widget=None):
            campo_layout = BoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=None)
            campo_layout.bind(minimum_height=campo_layout.setter('height'))
            
            label = Label(text=texto, font_size=ResponsiveHelper.get_font_size(18),
                         color=(0.1, 0.1, 0.2, 1), size_hint_y=None, height=dp(30), halign='left')
            label.bind(size=label.setter('text_size'))
            campo_layout.add_widget(label)
            
            if widget:
                campo_layout.add_widget(widget)
                return campo_layout, widget
            else:
                input_field = RoundedTextInput(hint_text=hint_text)
                campo_layout.add_widget(input_field)
                return campo_layout, input_field

        def crear_titulo_seccion(texto, size=26):
            return Label(text=texto, font_size=ResponsiveHelper.get_font_size(size),
                        color=(0.1, 0.4, 0.7, 1), bold=True, size_hint_y=None, height=dp(45))

        # COMPETIDORES
        form_container.add_widget(crear_titulo_seccion('Datos de los Competidores'))
        form_container.add_widget(crear_titulo_seccion('COMPETIDOR 1', 22))
        
        c1_layout, self.competidor1_input = crear_campo('Nombre(s)', 'Nombre(s)')
        form_container.add_widget(c1_layout)
        
        self.fecha_nac1_selector = DateSelector()
        fn1_layout, _ = crear_campo('Fecha de Nacimiento', widget=self.fecha_nac1_selector)
        form_container.add_widget(fn1_layout)
        
        p1_layout, self.peso1_input = crear_campo('Peso (kg)', 'Peso')
        form_container.add_widget(p1_layout)
        
        a1_layout, self.altura1_input = crear_campo('Altura (cm)', 'Altura')
        form_container.add_widget(a1_layout)
        
        s1_layout, self.sexo1_input = crear_campo('Sexo', 'Sexo')
        form_container.add_widget(s1_layout)
        
        n1_layout, self.nacionalidad1_input = crear_campo('Nacionalidad', 'Nacionalidad')
        form_container.add_widget(n1_layout)
        
        pr_layout, self.peto_rojo_input = crear_campo('Peto Rojo ID', 'ID del peto rojo')
        form_container.add_widget(pr_layout)
        
        form_container.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        form_container.add_widget(crear_titulo_seccion('COMPETIDOR 2', 22))
        
        c2_layout, self.competidor2_input = crear_campo('Nombre(s)', 'Nombre(s)')
        form_container.add_widget(c2_layout)
        
        self.fecha_nac2_selector = DateSelector()
        fn2_layout, _ = crear_campo('Fecha de Nacimiento', widget=self.fecha_nac2_selector)
        form_container.add_widget(fn2_layout)
        
        p2_layout, self.peso2_input = crear_campo('Peso (kg)', 'Peso')
        form_container.add_widget(p2_layout)
        
        a2_layout, self.altura2_input = crear_campo('Altura (cm)', 'Altura')
        form_container.add_widget(a2_layout)
        
        s2_layout, self.sexo2_input = crear_campo('Sexo', 'Sexo')
        form_container.add_widget(s2_layout)
        
        n2_layout, self.nacionalidad2_input = crear_campo('Nacionalidad', 'Nacionalidad')
        form_container.add_widget(n2_layout)
        
        pa_layout, self.peto_azul_input = crear_campo('Peto Azul ID', 'ID del peto azul')
        form_container.add_widget(pa_layout)
        
        form_container.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # DATOS DEL COMBATE
        form_container.add_widget(crear_titulo_seccion('Datos del Combate'))
        
        self.fecha_combate_selector = DateSelector()
        fc_layout, _ = crear_campo('Fecha del Combate', widget=self.fecha_combate_selector)
        form_container.add_widget(fc_layout)
        
        self.hora_combate_selector = TimeSelector()
        hc_layout, _ = crear_campo('Hora del Combate', widget=self.hora_combate_selector)
        form_container.add_widget(hc_layout)
        
        area_layout, self.area_input = crear_campo('Área de Combate', 'Ej: Área A, Tatami 1')
        form_container.add_widget(area_layout)
        
        self.categoria_peso_selector = CategoriaPesoSelector()
        cp_layout, _ = crear_campo('Categoría', widget=self.categoria_peso_selector)
        form_container.add_widget(cp_layout)
        
        self.rounds_selector = RoundsSelector(initial_rounds=3)
        r_layout, _ = crear_campo('Número de Rounds', widget=self.rounds_selector)
        form_container.add_widget(r_layout)
        
        self.duracion_round_selector = DurationSelector(initial_minutes=3, initial_seconds=0)
        dr_layout, _ = crear_campo('Duración del Round', widget=self.duracion_round_selector)
        form_container.add_widget(dr_layout)
        
        self.duracion_descanso_selector = DurationSelector(initial_minutes=1, initial_seconds=0)
        dd_layout, _ = crear_campo('Duración del Descanso', widget=self.duracion_descanso_selector)
        form_container.add_widget(dd_layout)
        
        form_container.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # JUECES
        form_container.add_widget(crear_titulo_seccion('Jueces'))
        form_container.add_widget(crear_titulo_seccion('JUEZ CENTRAL', 22))
        
        an_layout, self.arbitro_nombre_input = crear_campo('Nombre(s)', 'Nombre(s) del árbitro')
        form_container.add_widget(an_layout)
        
        aa_layout, self.arbitro_Apellidos_input = crear_campo('Apellidos', 'Apellidos del árbitro')
        form_container.add_widget(aa_layout)
        
        form_container.add_widget(crear_titulo_seccion('JUEZ 1', 22))
        
        j1n_layout, self.juez1_nombre_input = crear_campo('Nombre(s)', 'Nombre(s) del juez 1')
        form_container.add_widget(j1n_layout)
        
        j1a_layout, self.juez1_Apellidos_input = crear_campo('Apellidos', 'Apellidos del juez 1')
        form_container.add_widget(j1a_layout)
        
        form_container.add_widget(crear_titulo_seccion('JUEZ 2', 22))
        
        j2n_layout, self.juez2_nombre_input = crear_campo('Nombre(s)', 'Nombre(s) del juez 2')
        form_container.add_widget(j2n_layout)
        
        j2a_layout, self.juez2_Apellidos_input = crear_campo('Apellidos', 'Apellidos del juez 2')
        form_container.add_widget(j2a_layout)
        
        form_container.add_widget(crear_titulo_seccion('JUEZ 3', 22))
        
        j3n_layout, self.juez3_nombre_input = crear_campo('Nombre(s)', 'Nombre(s) del juez 3')
        form_container.add_widget(j3n_layout)
        
        j3a_layout, self.juez3_Apellidos_input = crear_campo('Apellidos', 'Apellidos del juez 3')
        form_container.add_widget(j3a_layout)
        
        form_container.add_widget(Widget(size_hint_y=None, height=dp(15)))

        # BOTONES
        botones_layout = BoxLayout(
            orientation='horizontal' if Window.width > 600 else 'vertical',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(50) if Window.width > 600 else dp(110)
        )

        btn_crear = HoverButton(text='CREAR COMBATE')
        btn_crear.bind(on_press=self.crear_combate)
        botones_layout.add_widget(btn_crear)

        btn_volver = HoverButton(text='VOLVER')
        btn_volver.canvas.before.clear()
        with btn_volver.canvas.before:
            Color(0.7, 0.1, 0.1, 1)
            btn_volver.rect = RoundedRectangle(
                pos=btn_volver.pos,
                size=btn_volver.size,
                radius=[btn_volver.border_radius]
            )
        btn_volver.bind(on_press=self.volver_a_principal)
        botones_layout.add_widget(btn_volver)

        form_container.add_widget(botones_layout)

        main_layout.add_widget(form_container)
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(30)))

        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)

    def update_background(self, instance, value):
        self.background_rect.size = instance.size
        self.background_rect.pos = instance.pos

    def on_window_resize(self, instance, width, height):
        Clock.schedule_once(lambda dt: self.build_ui(), 0.1)

    def mostrar_mensaje(self, titulo, mensaje):
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        popup_size = ResponsiveHelper.get_popup_size()
        text_width = popup_size[0] - dp(40)

        lbl_mensaje = Label(
            text=mensaje,
            color=(0.5, 0.8, 1, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80),
            text_size=(text_width, None)
        )
        lbl_mensaje.bind(size=lbl_mensaje.setter('text_size'))
        content.add_widget(lbl_mensaje)

        btn_aceptar = Button(
            text='ACEPTAR',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=ResponsiveHelper.get_font_size(18)
        )

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

        with popup.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            popup.rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(15)])

        def update_popup_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        popup.bind(pos=update_popup_rect, size=update_popup_rect)
        btn_aceptar.bind(on_press=popup.dismiss)
        content.add_widget(btn_aceptar)
        popup.open()

    def mostrar_popup_campos_faltantes(self, campos_faltantes):
        content = ScrollView()
        lista_campos = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20), size_hint_y=None)
        lista_campos.bind(minimum_height=lista_campos.setter('height'))

        titulo_label = Label(
            text='Campos Obligatorios Faltantes:',
            font_size=ResponsiveHelper.get_font_size(20),
            color=(0.5, 0.8, 1, 1),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        lista_campos.add_widget(titulo_label)

        for campo in campos_faltantes:
            label_campo = Label(
                text=f"• {campo}",
                font_size=ResponsiveHelper.get_font_size(16),
                color=(0.5, 0.8, 1, 1),
                size_hint_y=None,
                height=dp(35),
                halign='left'
            )
            label_campo.bind(size=label_campo.setter('text_size'))
            lista_campos.add_widget(label_campo)

        content.add_widget(lista_campos)

        popup_size = ResponsiveHelper.get_popup_size()
        popup = Popup(
            title='¡Atención!',
            title_color=(1, 1, 1, 1),
            title_size=ResponsiveHelper.get_font_size(22),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=popup_size,
            separator_height=0,
            background=''
        )

        with popup.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            popup.rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(15)])

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
            font_size=ResponsiveHelper.get_font_size(18)
        )
        btn_cerrar.bind(on_press=popup.dismiss)
        lista_campos.add_widget(btn_cerrar)
        popup.open()

    def crear_combate(self, instance):
        required_fields = [
            (self.competidor1_input, "Nombre(s) del Competidor 1"),
            (self.peso1_input, "Peso del Competidor 1 (kg)"),
            (self.altura1_input, "Altura del Competidor 1 (cm)"),
            (self.sexo1_input, "Sexo del Competidor 1"),
            (self.nacionalidad1_input, "Nacionalidad del Competidor 1"),
            (self.peto_rojo_input, "Peto Rojo ID"),
            (self.competidor2_input, "Nombre(s) del Competidor 2"),
            (self.peso2_input, "Peso del Competidor 2 (kg)"),
            (self.altura2_input, "Altura del Competidor 2 (cm)"),
            (self.sexo2_input, "Sexo del Competidor 2"),
            (self.nacionalidad2_input, "Nacionalidad del Competidor 2"),
            (self.peto_azul_input, "Peto Azul ID"),
            (self.area_input, "Área de Combate"),
            (self.arbitro_nombre_input, "Nombre(s) del Árbitro Central"),
            (self.arbitro_Apellidos_input, "Apellidos del Árbitro Central"),
            (self.juez1_nombre_input, "Nombre(s) del Juez 1"),
            (self.juez1_Apellidos_input, "Apellidos del Juez 1"),
            (self.juez2_nombre_input, "Nombre(s) del Juez 2"),
            (self.juez2_Apellidos_input, "Apellidos del Juez 2"),
            (self.juez3_nombre_input, "Nombre(s) del Juez 3"),
            (self.juez3_Apellidos_input, "Apellidos del Juez 3")
        ]

        campos_faltantes = [mensaje for campo, mensaje in required_fields if not campo.text.strip()]

        if campos_faltantes:
            self.mostrar_popup_campos_faltantes(campos_faltantes)
            return

        try:
            float(self.peso1_input.text)
            float(self.peso2_input.text)
        except ValueError:
            self.mostrar_mensaje("Error", "Los pesos deben ser números válidos")
            return

        try:
            float(self.altura1_input.text)
            float(self.altura2_input.text)
        except ValueError:
            self.mostrar_mensaje("Error", "Las alturas deben ser números válidos")
            return

        fecha_combate = self.fecha_combate_selector.get_formatted_date()
        hora_combate = self.hora_combate_selector.get_formatted_time()
        categoria_peso = self.categoria_peso_selector.get_selected_category()
        num_rounds = self.rounds_selector.get_selected_rounds()
        duracion_round = self.duracion_round_selector.get_formatted_duration()
        duracion_descanso = self.duracion_descanso_selector.get_formatted_duration()

        self.mostrar_mensaje(
            "¡Combate creado!",
            f"El combate entre {self.competidor1_input.text} y {self.competidor2_input.text} ha sido creado con éxito\n"
            f"Categoría de peso: {categoria_peso}\n"
            f"Número de rounds: {num_rounds}\n"
            f"Duración round: {duracion_round}\n"
            f"Duración descanso: {duracion_descanso}\n"
            f"Fecha: {fecha_combate} a las {hora_combate}\n"
            f"Área: {self.area_input.text}\n"
            f"La contraseña que debes compartir es 36782398"
        )

        for widget in self.walk():
            if isinstance(widget, TextInput):
                widget.text = ""

    def volver_a_principal(self, instance):
        App.get_running_app().root.current = 'ini'