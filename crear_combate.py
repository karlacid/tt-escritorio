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
from datetime import datetime, date
import calendar


class DateSelector(BoxLayout):
    selected_date = ObjectProperty(date.today())
    
    def __init__(self, initial_date=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(55)
        
        # Parsear fecha inicial si se proporciona
        if initial_date:
            try:
                day, month, year = map(int, initial_date.split('/'))
                initial_date = date(year, month, day)
            except:
                initial_date = date.today()
        else:
            initial_date = date.today()
        
        # Años (desde el actual hasta 10 años atrás para fechas de nacimiento)
        current_year = initial_date.year
        self.year_spinner = Spinner(
            text=str(current_year),
            values=[str(y) for y in range(current_year - 100, current_year + 1)],
            size_hint=(0.3, 1),
            font_size=sp(20),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1)
        )
        
        # Meses en español
        meses_espanol = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        self.month_spinner = Spinner(
            text=meses_espanol[initial_date.month - 1],
            values=meses_espanol,
            size_hint=(0.4, 1),
            font_size=sp(20),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        # Días (se actualizará según mes y año)
        self.day_spinner = Spinner(
            text=str(initial_date.day),
            values=[],
            size_hint=(0.3, 1),
            font_size=sp(20),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        self.add_widget(self.day_spinner)
        self.add_widget(self.month_spinner)
        self.add_widget(self.year_spinner)
        
       
        self.update_days()
        
       
        self.month_spinner.bind(text=self.update_days_on_change)
        self.year_spinner.bind(text=self.update_days_on_change)
        
    def update_days_on_change(self, *args):
        self.update_days()
        self.get_selected_date()
        
    def update_days(self):
        month = self.month_spinner.text
        year = self.year_spinner.text
        
        if month and year:
            # Convertir mes en español a número
            meses_espanol = [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ]
            month_num = meses_espanol.index(month) + 1
            year_num = int(year)
            _, num_days = calendar.monthrange(year_num, month_num)
            
            current_day = int(self.day_spinner.text) if self.day_spinner.text.isdigit() else 1
            days = [str(d) for d in range(1, num_days + 1)]
            self.day_spinner.values = days
            
            # Asegurarse de que el día seleccionado sea válido
            if str(current_day) not in days:
                current_day = 1
            self.day_spinner.text = str(current_day)
            
    def get_selected_date(self):
        try:
            meses_espanol = [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ]
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
        
        # Parsear hora inicial si se proporciona
        if initial_time:
            try:
                hour, minute = map(int, initial_time.split(':'))
                initial_time = datetime.now().replace(hour=hour, minute=minute).time()
            except:
                initial_time = datetime.now().time()
        else:
            initial_time = datetime.now().time()
        
        # Horas
        self.hour_spinner = Spinner(
            text=f"{initial_time.hour:02d}",
            values=[f"{h:02d}" for h in range(0, 24)],
            size_hint=(0.45, 1),
            font_size=sp(20),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        # Minutos
        minute = (initial_time.minute // 5) * 5  # Redondear a múltiplos de 5
        self.minute_spinner = Spinner(
            text=f"{minute:02d}",
            values=[f"{m:02d}" for m in range(0, 60, 5)],
            size_hint=(0.45, 1),
            font_size=sp(20),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        self.add_widget(self.hour_spinner)
        self.add_widget(Label(text=":", size_hint=(0.1, 1)))
        self.add_widget(self.minute_spinner)
        
        # Configurar hora inicial
        self.get_selected_time()
        
        # Bind para actualizar cuando cambia
        self.hour_spinner.bind(text=self.update_time)
        self.minute_spinner.bind(text=self.update_time)
        
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
        self.size_hint = (1, None)  # Asegura que ocupe todo el ancho disponible
        self.height = dp(55)
       
        # Selector de número de rounds (1-5)
        self.rounds_spinner = Spinner(
            text=str(initial_rounds),
            values=[str(r) for r in range(1, 6)],
            size_hint=(1, 1),  # 60% del ancho para el spinner
            font_size=sp(20),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1)
        )
        
        
        
        self.add_widget(self.rounds_spinner)

        
        # Configurar valor inicial
        self.get_selected_rounds()
        
        # Bind para actualizar cuando cambia
        self.rounds_spinner.bind(text=self.update_rounds)
        
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
        self.height = dp(55)  # Misma altura que el selector de hora
        
        # Minutos (0-10)
        self.minutes_spinner = Spinner(
            text=str(initial_minutes),
            values=[str(m) for m in range(0, 11)],
            size_hint=(0.3, 1),  # Ajustado para igualar selector de hora
            font_size=sp(20),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1)
        )
        
        # Separador
        self.add_widget(Label(text=":", size_hint=(0.1, 1), font_size=sp(20)))
        
        # Segundos (0-59, en intervalos de 5)
        self.seconds_spinner = Spinner(
            text=f"{initial_seconds:02d}",
            values=[f"{s:02d}" for s in range(0, 60, 5)],
            size_hint=(0.3, 1),  # Ajustado para igualar selector de hora
            font_size=sp(20),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1)
        )
        
        # Etiqueta de minutos
        self.add_widget(self.minutes_spinner)
        self.add_widget(Label(text="min", size_hint=(0.1, 1), font_size=sp(16)))
        self.add_widget(self.seconds_spinner)
        self.add_widget(Label(text="seg", size_hint=(0.1, 1), font_size=sp(16)))
        
        # Configurar valores iniciales
        self.get_selected_duration()
        
        # Bind para actualizar cuando cambia
        self.minutes_spinner.bind(text=self.update_duration)
        self.seconds_spinner.bind(text=self.update_duration)
        
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
        
        # Categorías de peso
        categorias = [
            "Fin", 
            "Fly", 
            "Bantam", 
            "Feather", 
            "Light", 
            "Welter", 
            "Middle", 
            "Heavy"
        ]
        
        self.category_spinner = Spinner(
            text=initial_category if initial_category else categorias[0],
            values=categorias,
            size_hint=(1, 1),
            font_size=sp(20),
            background_color=(0.1, 0.4, 0.7, 0.9),
            color=(1, 1, 1, 1))
        
        self.add_widget(self.category_spinner)
        
        # Configurar valor inicial
        self.get_selected_category()
        
        # Bind para actualizar cuando cambia
        self.category_spinner.bind(text=self.update_category)
        
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
        self.height = dp(50)
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


class CrearCombateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(10)],
            spacing=dp(10)
        )

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
            bar_width=dp(10),
            scroll_type=['bars', 'content']
        )

        # Contenedor del formulario
        form_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            spacing=dp(12),
            padding=[dp(30), dp(20), dp(30), dp(20)],
            pos_hint={'center_x': 0.5}
        )
        form_container.bind(minimum_height=form_container.setter('height'))

        # Título
        titulo = Label(
            text='CREAR COMBATE',
            font_size=dp(32),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )
        form_container.add_widget(titulo)

        # Función para crear campos de entrada con etiqueta
        def crear_campo(texto, hint_text=None, widget=None):
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
            if widget:
                campo_layout.add_widget(widget)
            else:
                input_field = RoundedTextInput(hint_text=hint_text)
                campo_layout.add_widget(input_field)
                return campo_layout, input_field
            return campo_layout, widget

        # Sección 1: Competidores
        competidores_label = Label(
            text='Datos de los Competidores',
            font_size=dp(26),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )
        form_container.add_widget(competidores_label)

        # Competidor 1
        competidor1_label = Label(
            text='COMPETIDOR 1',
            font_size=dp(22),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        form_container.add_widget(competidor1_label)

        competidor1_layout, self.competidor1_input = crear_campo('Nombre(s) ', 'Nombre(s) ')
        form_container.add_widget(competidor1_layout)

        # Selector de fecha de nacimiento para competidor 1
        self.fecha_nac1_selector = DateSelector()
        fecha_nac1_layout, _ = crear_campo('Fecha de Nacimiento', widget=self.fecha_nac1_selector)
        form_container.add_widget(fecha_nac1_layout)

        peso1_layout, self.peso1_input = crear_campo('Peso (kg)', 'Peso')
        form_container.add_widget(peso1_layout)

        altura1_layout, self.altura1_input = crear_campo('Altura (cm)', 'Altura')
        form_container.add_widget(altura1_layout)

        sexo1_layout, self.sexo1_input = crear_campo('Sexo', 'Sexo')
        form_container.add_widget(sexo1_layout)

        nacionalidad1_layout, self.nacionalidad1_input = crear_campo('Nacionalidad', 'Nacionalidad')
        form_container.add_widget(nacionalidad1_layout)

        peto_rojo_layout, self.peto_rojo_input = crear_campo('Peto Rojo ID', 'ID del peto rojo')
        form_container.add_widget(peto_rojo_layout)

        # Separador
        form_container.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Competidor 2
        competidor2_label = Label(
            text='COMPETIDOR 2',
            font_size=dp(22),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        form_container.add_widget(competidor2_label)

        competidor2_layout, self.competidor2_input = crear_campo('Nombre(s) ', 'Nombre(s) ')
        form_container.add_widget(competidor2_layout)

        # Selector de fecha de nacimiento para competidor 2
        self.fecha_nac2_selector = DateSelector()
        fecha_nac2_layout, _ = crear_campo('Fecha de Nacimiento', widget=self.fecha_nac2_selector)
        form_container.add_widget(fecha_nac2_layout)

        peso2_layout, self.peso2_input = crear_campo('Peso (kg)', 'Peso')
        form_container.add_widget(peso2_layout)

        altura2_layout, self.altura2_input = crear_campo('Altura (cm)', 'Altura')
        form_container.add_widget(altura2_layout)

        sexo2_layout, self.sexo2_input = crear_campo('Sexo', 'Sexo')
        form_container.add_widget(sexo2_layout)

        nacionalidad2_layout, self.nacionalidad2_input = crear_campo('Nacionalidad', 'Nacionalidad')
        form_container.add_widget(nacionalidad2_layout)

        peto_azul_layout, self.peto_azul_input = crear_campo('Peto Azul ID', 'ID del peto azul')
        form_container.add_widget(peto_azul_layout)

        # Separador
        form_container.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Sección 2: Datos del Combate
        combate_label = Label(
            text='Datos del Combate',
            font_size=dp(26),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )
        form_container.add_widget(combate_label)

        # Selector de fecha del combate
        self.fecha_combate_selector = DateSelector()
        fecha_combate_layout, _ = crear_campo('Fecha del Combate', widget=self.fecha_combate_selector)
        form_container.add_widget(fecha_combate_layout)

        # Selector de hora del combate
        self.hora_combate_selector = TimeSelector()
        hora_combate_layout, _ = crear_campo('Hora del Combate', widget=self.hora_combate_selector)
        form_container.add_widget(hora_combate_layout)

        area_layout, self.area_input = crear_campo('Área de Combate', 'Ej: Área A, Tatami 1')
        form_container.add_widget(area_layout)

        # Selector de categoría de peso
        self.categoria_peso_selector = CategoriaPesoSelector()
        categoria_peso_layout, _ = crear_campo('Categoría', widget=self.categoria_peso_selector)
        form_container.add_widget(categoria_peso_layout)

        # Selector de número de rounds
        self.rounds_selector = RoundsSelector(initial_rounds=3)
        rounds_layout, _ = crear_campo('Número de Rounds', widget=self.rounds_selector)
        form_container.add_widget(rounds_layout)

        # Selector de duración del round (minutos y segundos)
        self.duracion_round_selector = DurationSelector(initial_minutes=3, initial_seconds=0)
        duracion_round_layout, _ = crear_campo('Duración del Round', widget=self.duracion_round_selector)
        form_container.add_widget(duracion_round_layout)

        # Selector de duración del descanso (minutos y segundos)
        self.duracion_descanso_selector = DurationSelector(initial_minutes=1, initial_seconds=0)
        duracion_descanso_layout, _ = crear_campo('Duración del Descanso', widget=self.duracion_descanso_selector)
        form_container.add_widget(duracion_descanso_layout)

        # Separador
        form_container.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Sección 3: Jueces
        jueces_label = Label(
            text='Jueces',
            font_size=dp(26),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )
        form_container.add_widget(jueces_label)

        # Juez Central
        arbitro_label = Label(
            text='JUEZ CENTRAL',
            font_size=dp(22),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        form_container.add_widget(arbitro_label)

        arbitro_nombre_layout, self.arbitro_nombre_input = crear_campo('Nombre(s)', 'Nombre(s) del árbitro')
        form_container.add_widget(arbitro_nombre_layout)

        arbitro_Apellidos_layout, self.arbitro_Apellidos_input = crear_campo('Apellidos', 'Apellidos del árbitro')
        form_container.add_widget(arbitro_Apellidos_layout)

        # Juez 1
        juez1_label = Label(
            text='JUEZ 1',
            font_size=dp(22),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        form_container.add_widget(juez1_label)

        juez1_nombre_layout, self.juez1_nombre_input = crear_campo('Nombre(s)', 'Nombre(s) del juez 1')
        form_container.add_widget(juez1_nombre_layout)

        juez1_Apellidos_layout, self.juez1_Apellidos_input = crear_campo('Apellidos', 'Apellidos del juez 1')
        form_container.add_widget(juez1_Apellidos_layout)

        # Juez 2
        juez2_label = Label(
            text='JUEZ 2',
            font_size=dp(22),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        form_container.add_widget(juez2_label)

        juez2_nombre_layout, self.juez2_nombre_input = crear_campo('Nombre(s)', 'Nombre(s) del juez 2')
        form_container.add_widget(juez2_nombre_layout)

        juez2_Apellidos_layout, self.juez2_Apellidos_input = crear_campo('Apellidos', 'Apellidos del juez 2')
        form_container.add_widget(juez2_Apellidos_layout)

        # Juez 3
        juez3_label = Label(
            text='JUEZ 3',
            font_size=dp(22),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        form_container.add_widget(juez3_label)

        juez3_nombre_layout, self.juez3_nombre_input = crear_campo('Nombre(s)', 'Nombre(s) del juez 3')
        form_container.add_widget(juez3_nombre_layout)

        juez3_Apellidos_layout, self.juez3_Apellidos_input = crear_campo('Apellidos', 'Apellidos del juez 3')
        form_container.add_widget(juez3_Apellidos_layout)

        # Botones
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(50),
            padding=[0, dp(20), 0, 0]
        )

        btn_crear = HoverButton(text='CREAR COMBATE')
        btn_crear.bind(on_press=self.crear_combate)
        botones_layout.add_widget(btn_crear)

        btn_volver = HoverButton(text='VOLVER', background_color=(0.7, 0.1, 0.1, 1))
        btn_volver.bind(on_press=self.volver_a_principal)
        botones_layout.add_widget(btn_volver)

        form_container.add_widget(botones_layout)

        scroll_view.add_widget(form_container)
        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

    def update_background(self, *args):
        self.background_rect.size = Window.size
        self.background_rect.pos = self.pos

    def mostrar_mensaje(self, titulo, mensaje):
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        popup_width = dp(450) - 2 * dp(20)  # Ancho del popup menos el padding horizontal

        lbl_mensaje = Label(
            text=mensaje,
            color=(0.2, 0.6, 1, 1),
            font_size=sp(20),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80),
            text_size=(popup_width, None),
            shorten=False,
            mipmap=True,
            line_height=1.2
        )
        lbl_mensaje.bind(texture_size=lbl_mensaje.setter('size'))
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
            title_color=(0.2, 0.6, 1, 1),
            title_size=sp(22),
            title_align='center',
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

    def mostrar_popup_campos_faltantes(self, campos_faltantes):
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

        for campo in campos_faltantes:
            label_campo = Label(
                text=f"• {campo}",
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

    def crear_combate(self, instance):
        # Lista de campos obligatorios con sus widgets y mensajes
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

        # Encontrar campos vacíos y crear una lista de mensajes
        campos_faltantes = [mensaje for campo, mensaje in required_fields if not campo.text.strip()]

        # Si hay campos faltantes, mostrar el popup con la lista
        if campos_faltantes:
            self.mostrar_popup_campos_faltantes(campos_faltantes)
            return

        # Validar pesos numéricos
        try:
            float(self.peso1_input.text)
            float(self.peso2_input.text)
        except ValueError:
            self.mostrar_mensaje("Error", "Los pesos deben ser números válidos")
            return

        # Validar alturas numéricas
        try:
            float(self.altura1_input.text)
            float(self.altura2_input.text)
        except ValueError:
            self.mostrar_mensaje("Error", "Las alturas deben ser números válidos")
            return

        # Obtener todos los datos seleccionados
        fecha_combate = self.fecha_combate_selector.get_formatted_date()
        hora_combate = self.hora_combate_selector.get_formatted_time()
        categoria_peso = self.categoria_peso_selector.get_selected_category()
        num_rounds = self.rounds_selector.get_selected_rounds()
        duracion_round = self.duracion_round_selector.get_formatted_duration()
        duracion_descanso = self.duracion_descanso_selector.get_formatted_duration()

        # Mostrar mensaje de éxito con todos los datos
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

        # Limpiar campos después de creación exitosa
        for widget in self.walk():
            if isinstance(widget, TextInput):
                widget.text = ""

    def volver_a_principal(self, instance):
        App.get_running_app().root.current = 'ini'