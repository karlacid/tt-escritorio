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
from kivy.metrics import dp, sp
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
        
        # Años (desde el actual hasta 10 años adelante)
        current_year = initial_date.year
        self.year_spinner = Spinner(
            text=str(current_year),
            values=[str(y) for y in range(current_year, current_year + 11)],
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
        
        # Actualizar días iniciales
        self.update_days()
        
        # Bind para actualizar días cuando cambia mes o año
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
            color=(1, 1, 1, 1)
        )
        
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


class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_active = ""
        self.background_color = (0, 0, 0, 0)  # Fondo transparente
        self.multiline = False
        self.size_hint_y = None
        self.height = dp(55)
        self.padding = [dp(8), dp(8), dp(8), dp(8)]
        self.font_size = sp(24)
        self.color = (1, 1, 1, 1)  # Texto blanco
        self.hint_text_color = (0.9, 0.9, 0.9, 0.9)  # Hint semi-transparente
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


class ActualizarTorneoScreen(Screen):
    def __init__(self, torneo_data, on_save, **kwargs):
        super().__init__(**kwargs)
        self.torneo_data = torneo_data
        self.on_save = on_save
        
        main_layout = BoxLayout(orientation='vertical', padding=[dp(20), dp(10)], spacing=dp(10))
        
        with main_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.background_rect = Rectangle(size=Window.size, pos=self.pos)
        
        self.bind(size=self.update_background, pos=self.update_background)

        logo = Image(
            source="Imagen5-Photoroom.png",
            size_hint=(1, None),
            height=dp(120),
            pos_hint={'center_x': 0.5}
        )
        main_layout.add_widget(logo)

        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            bar_width=dp(10),
            scroll_type=['bars', 'content']
        )

        form_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            spacing=dp(15),
            padding=[dp(40), dp(20), dp(40), dp(20)],
            pos_hint={'center_x': 0.5}
        )
        form_container.bind(minimum_height=form_container.setter('height'))

        titulo = Label(
            text='EDITAR TORNEO',
            font_size=dp(32),
            color=(0.1, 0.4, 0.7),
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )
        form_container.add_widget(titulo)

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

        # Campos del formulario
        nombre_torneo_layout, self.nombre_torneo_input = crear_campo(
            'Nombre del Torneo', 'Ingresa el nombre del torneo', 
            RoundedTextInput(text=torneo_data['nombre']))
        form_container.add_widget(nombre_torneo_layout)

        # Selector de fecha con Spinners
        self.date_selector = DateSelector(initial_date=torneo_data.get('fecha'))
        fecha_layout, _ = crear_campo('Fecha', widget=self.date_selector)
        form_container.add_widget(fecha_layout)

        sede_layout, self.sede_input = crear_campo(
            'Sede', 'Lugar del torneo', 
            RoundedTextInput(text=torneo_data['Sede']))
        form_container.add_widget(sede_layout)

        # Selector de hora de inicio
        self.time_start_selector = TimeSelector(initial_time=torneo_data.get('hora_inicio'))
        hora_inicio_layout, _ = crear_campo('Hora de Inicio', widget=self.time_start_selector)
        form_container.add_widget(hora_inicio_layout)

        # Selector de hora de término
        self.time_end_selector = TimeSelector(initial_time=torneo_data.get('hora_fin'))
        hora_termino_layout, _ = crear_campo('Hora de Término', widget=self.time_end_selector)
        form_container.add_widget(hora_termino_layout)

        # Botones
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(50),
            padding=[0, dp(20), 0, 0]
        )

        btn_guardar = HoverButton(text='GUARDAR CAMBIOS')
        btn_guardar.bind(on_press=self.guardar_cambios)
        botones_layout.add_widget(btn_guardar)

        btn_cancelar = HoverButton(text='CANCELAR', background_color=(0.7, 0.1, 0.1, 1))
        btn_cancelar.bind(on_press=self.cancelar)
        botones_layout.add_widget(btn_cancelar)

        form_container.add_widget(botones_layout)

        scroll_view.add_widget(form_container)
        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

    def update_background(self, *args):
        self.background_rect.size = Window.size
        self.background_rect.pos = self.pos

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

        for mensaje in campos_faltantes:
            label_campo = Label(
                text=f"• {mensaje}",
                font_size=sp(18),
                color=(0.1, 0.1, 0.2, 1),
                size_hint_y=None,
                height=dp(30))
        content.add_widget(label_campo)

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

    def guardar_cambios(self, instance):
        # Validar campos obligatorios
        required_fields = [
            (self.nombre_torneo_input, "Nombre del torneo"),
            (self.sede_input, "Sede del torneo")
        ]

        campos_faltantes = []
        for campo, mensaje in required_fields:
            if not campo.text.strip():
                campos_faltantes.append(mensaje)

        if campos_faltantes:
            self.mostrar_popup_campos_faltantes(campos_faltantes)
            return

        # Validar que la hora de término sea posterior a la de inicio
        hora_inicio = self.time_start_selector.get_selected_time()
        hora_termino = self.time_end_selector.get_selected_time()

        if hora_inicio >= hora_termino:
            self.mostrar_mensaje("Error", "La hora de término debe ser posterior a la de inicio")
            return

        nuevos_datos = {
            'nombre': self.nombre_torneo_input.text,
            'fecha': self.date_selector.get_formatted_date(),
            'hora_inicio': self.time_start_selector.get_formatted_time(),
            'hora_fin': self.time_end_selector.get_formatted_time(),
            'Sede': self.sede_input.text
        }
        
        self.on_save(self.torneo_data, nuevos_datos)
        self.manager.current = 'torneos_anteriores'

    def cancelar(self, instance):
        self.manager.current = 'torneos_anteriores'