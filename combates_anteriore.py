from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.textinput import TextInput

class LightBlueButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.2, 0.6, 1, 1)
        self.color = (1, 1, 1, 1)
        self.size_hint_y = None
        self.height = dp(50)
        self.font_size = sp(16)
        self.bold = True
        self.border_radius = dp(10)

        with self.canvas.before:
            Color(*self.background_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.border_radius])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class SuccessPopup(Popup):
    message = StringProperty('')
    
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.title = 'Éxito'
        self.title_color = (0.2, 0.6, 1, 1)
        self.title_size = sp(22)
        self.title_align = 'center'
        self.size_hint = (None, None)
        self.size = (dp(400), dp(200))
        self.background = ''
        self.separator_height = 0
        self.auto_dismiss = True

        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        message_label = Label(
            text=self.message,
            font_size=sp(20),
            color=(0.2, 0.6, 1, 1),
            halign='center',
            valign='middle'
        )
        content.add_widget(message_label)
        
        btn_ok = Button(
            text='OK',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))
        btn_ok.bind(on_press=self.dismiss)
        
        content.add_widget(btn_ok)
        self.content = content

        with self.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(15)]
            )

        self.bind(
            pos=lambda instance, value: setattr(self.rect, 'pos', value),
            size=lambda instance, value: setattr(self.rect, 'size', value)
        )

class PasswordInputPopup(Popup):
    def __init__(self, on_verify, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Ingresar Contraseña'
        self.title_color = (0.2, 0.6, 1, 1)
        self.title_size = sp(22)
        self.title_align = 'center'
        self.size_hint = (None, None)
        self.size = (dp(400), dp(250))
        self.on_verify = on_verify
        self.background = ''
        self.separator_height = 0
        self.auto_dismiss = False

        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        self.password_input = TextInput(
            password=True,
            multiline=False,
            font_size=sp(20),
            size_hint_y=None,
            height=dp(50),
            hint_text='Ingrese su contraseña'
        )
        content.add_widget(self.password_input)
        
        buttons = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        btn_cancel = Button(
            text='CANCELAR',
            size_hint_x=0.5,
            background_normal='',
            background_color=(0.7, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))
        btn_cancel.bind(on_press=self.dismiss)
        
        btn_verify = Button(
            text='VERIFICAR',
            size_hint_x=0.5,
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))
        btn_verify.bind(on_press=self.verify_password)
        
        buttons.add_widget(btn_cancel)
        buttons.add_widget(btn_verify)
        content.add_widget(buttons)
        
        self.content = content

        with self.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(15)]
            )

        self.bind(
            pos=lambda instance, value: setattr(self.rect, 'pos', value),
            size=lambda instance, value: setattr(self.rect, 'size', value)
        )

    def verify_password(self, instance):
        if self.password_input.text == "petotech123":
            self.on_verify(True)
            self.dismiss()
        else:
            self.password_input.text = ''
            self.password_input.hint_text = 'Contraseña incorrecta, intente de nuevo'
            self.password_input.hint_text_color = (1, 0, 0, 1)

class PasswordDisplayPopup(Popup):
    def __init__(self, combate_numero, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Contraseña del Combate'
        self.title_color = (0.2, 0.6, 1, 1)
        self.title_size = sp(22)
        self.title_align = 'center'
        self.size_hint = (None, None)
        self.size = (dp(400), dp(250))
        self.background = ''
        self.separator_height = 0
        self.auto_dismiss = True

        self.combate_password = self._generate_password(combate_numero)

        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        message = Label(
            text=f'Contraseña para:\n[b]Combate #{combate_numero}[/b]',
            font_size=sp(18),
            color=(0.2, 0.6, 1, 1),
            halign='center',
            markup=True
        )
        content.add_widget(message)
        
        password_display = Label(
            text=f'[b]{self.combate_password}[/b]',
            font_size=sp(24),
            color=(0.1, 0.4, 0.7, 1),
            halign='center',
            markup=True
        )
        content.add_widget(password_display)
        
        btn_ok = Button(
            text='OK',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))
        btn_ok.bind(on_press=self.dismiss)
        
        content.add_widget(btn_ok)
        self.content = content

        with self.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(15)]
            )

        self.bind(
            pos=lambda instance, value: setattr(self.rect, 'pos', value),
            size=lambda instance, value: setattr(self.rect, 'size', value)
        )

    def _generate_password(self, combate_numero):
        import hashlib
        hash_obj = hashlib.md5(str(combate_numero).encode())
        return hash_obj.hexdigest()[:8].upper()

class ConfirmDeleteCombatePopup(Popup):
    def __init__(self, combate_data, on_confirm, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Confirmar Eliminación'
        self.title_color = (0.2, 0.6, 1, 1)
        self.title_size = sp(22)
        self.title_align = 'center'
        self.size_hint = (None, None)
        self.size = (dp(450), dp(250))
        self.combate_data = combate_data
        self.on_confirm = on_confirm
        self.background = ''
        self.separator_height = 0
        self.auto_dismiss = False

        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        message = Label(
            text=f'¿Estás seguro que deseas eliminar\nel combate #{combate_data["numero"]}?\nCategoría: {combate_data["categoria"]}',
            font_size=sp(20),
            color=(0.2, 0.6, 1, 1),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80),
            text_size=(dp(400), None),
            shorten=False,
            markup=True
        )
        content.add_widget(message)

        buttons = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        btn_cancel = Button(
            text='CANCELAR',
            size_hint_x=0.5,
            background_normal='',
            background_color=(0.7, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))
        btn_cancel.bind(on_press=self.dismiss)
        
        btn_confirm = Button(
            text='ELIMINAR',
            size_hint_x=0.5,
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))
        btn_confirm.bind(on_press=self.confirm_delete)
        
        buttons.add_widget(btn_cancel)
        buttons.add_widget(btn_confirm)
        content.add_widget(buttons)

        self.content = content

        with self.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(15)]
            )

        self.bind(
            pos=lambda instance, value: setattr(self.rect, 'pos', value),
            size=lambda instance, value: setattr(self.rect, 'size', value)
        )

    def confirm_delete(self, instance):
        self.on_confirm(self.combate_data)
        self.dismiss()

class CombateCard(BoxLayout):
    bg_color = ListProperty([0.1, 0.4, 0.7, 1])

    def __init__(self, combate_data, on_delete, on_edit, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = [dp(30), dp(20)]
        self.size_hint = (0.6, None)
        self.height = dp(320)  # Aumenté la altura para acomodar los botones
        self.combate_data = combate_data
        self.on_delete_callback = on_delete
        self.on_edit_callback = on_edit

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
            self.bind(pos=self.update_rect, size=self.update_rect)

        # Título
        self.title_label = Label(
            text=f"[b]Combate {combate_data['numero']}[/b]",
            markup=True,
            font_size=sp(22),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(40),
            halign='left',
            text_size=(Window.width - dp(60), None)
        )
        self.add_widget(self.title_label)

        # Información del combate
        self.info_layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(5),
            padding=[dp(10), 0, dp(10), 0]
        )
        
        self.add_info_row("Fecha:", combate_data['fecha'])
        self.add_info_row("Hora:", combate_data.get('hora', 'No disponible'))
        self.add_info_row("Categoría:", combate_data['categoria'])

        # Formatear los participantes con el segundo competidor en rojo
        participantes_text = (
            f"{combate_data.get('competidor1', 'No disponible')} vs "
            f"[color=ff3333]{combate_data.get('competidor2', 'No disponible')}[/color]"
        )
        self.add_info_row("Participantes:", participantes_text, is_participants=True)

        self.add_widget(self.info_layout)

        # Contenedor principal para los botones
        self.buttons_main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(110)
        )

        # Primera fila de botones (EDITAR y ELIMINAR)
        self.button_row1 = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        self.edit_button = LightBlueButton(text='EDITAR')
        self.edit_button.bind(on_press=self.open_edit_screen)
        
        self.delete_button = LightBlueButton(text='ELIMINAR')
        self.delete_button.bind(on_press=self.open_delete_popup)
        
        self.button_row1.add_widget(self.edit_button)
        self.button_row1.add_widget(self.delete_button)

        # Segunda fila de botones (CONTRASEÑA y TABLERO)
        self.button_row2 = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        self.password_button = LightBlueButton(text='CONTRASEÑA')
        self.password_button.bind(on_press=self.open_password_flow)
        
        self.tablero_button = LightBlueButton(text='TABLERO')
        self.tablero_button.bind(on_press=self.navigate_to_tablero)
        
        self.button_row2.add_widget(self.password_button)
        self.button_row2.add_widget(self.tablero_button)

        # Agregar ambas filas al layout principal
        self.buttons_main_layout.add_widget(self.button_row1)
        self.buttons_main_layout.add_widget(self.button_row2)
        
        # Agregar el contenedor principal de botones a la tarjeta
        self.add_widget(self.buttons_main_layout)

    def add_info_row(self, label, value, is_participants=False):
        row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(5)
        )
        
        lbl_label = Label(
            text=label,
            font_size=sp(16),
            color=(0.95, 0.95, 0.95, 1),
            halign='left',
            valign='middle',
            size_hint_x=0.3,
            text_size=(None, None)
        )
        
        lbl_value = Label(
            text=value,
            font_size=sp(16),
            color=(0.95, 0.95, 0.95, 1) if not is_participants else (1, 1, 1, 1),
            halign='left',
            valign='middle',
            size_hint_x=0.7,
            text_size=(Window.width * 0.5, None),
            shorten=False,
            markup=is_participants  # Habilitar markup solo para participantes
        )
        
        row.add_widget(lbl_label)
        row.add_widget(lbl_value)
        self.info_layout.add_widget(row)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def open_delete_popup(self, instance):
        ConfirmDeleteCombatePopup(
            combate_data=self.combate_data,
            on_confirm=self.on_delete_callback
        ).open()

    def open_edit_screen(self, instance):
        app = App.get_running_app()
        
        if not app.root.has_screen('actualizar_combate'):
            from actualizar_combate import ActualizarCombateScreen
            app.root.add_widget(ActualizarCombateScreen(
                name='actualizar_combate',
                combate_data=self.combate_data,
                on_save=self.on_edit_callback
            ))
        
        app.root.current = 'actualizar_combate'

    def open_password_flow(self, instance):
        PasswordInputPopup(
            on_verify=lambda success: self.show_combate_password() if success else None
        ).open()

    def show_combate_password(self):
        PasswordDisplayPopup(
            combate_numero=self.combate_data['numero']
        ).open()

    def navigate_to_tablero(self, instance):
        app = App.get_running_app()
        if not app.root.has_screen('tablero'):
            from tablero import MainScreentab
            app.root.add_widget(MainScreentab(name='tablero'))
        
        tablero_screen = app.root.get_screen('tablero')
        tablero_screen.com1_panel.name = self.combate_data.get('competidor1', 'COM1')
        tablero_screen.com2_panel.name = self.combate_data.get('competidor2', 'COM2')
        tablero_screen.com1_panel.nationality = self.combate_data.get('nacionalidad1', '')
        tablero_screen.com2_panel.nationality = self.combate_data.get('nacionalidad2', '')
        
        app.root.current = 'tablero'

class CombatesScreen(Screen):
    torneo_nombre = StringProperty('')
    torneo_id = NumericProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.combates = []
        self.layout = BoxLayout(orientation='vertical')
        
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(pos=self.layout.pos, size=self.layout.size)
            self.layout.bind(pos=self.update_rect, size=self.update_rect)

        self.add_widget(self.layout)
        self.build_ui()

    def update_rect(self, *args):
        self.rect.pos = self.layout.pos
        self.rect.size = self.layout.size

    def build_ui(self):
        self.layout.clear_widgets()

        header = BoxLayout(size_hint_y=None, height=dp(80), padding=[dp(20), dp(10)])
        titulo = Label(
            text=f"[b]Combates del Torneo:[/b] {self.torneo_nombre}",
            markup=True,
            font_size=sp(22),
            color=(0.2, 0.2, 0.3, 1),
            halign='center',
            valign='middle',
            text_size=(Window.width - dp(40), None),
            shorten=False
        )
        header.add_widget(titulo)
        self.layout.add_widget(header)
        
        scroll = ScrollView(
            size_hint=(1, 1),
            scroll_type=['bars', 'content'],
            bar_width=dp(10),
            bar_color=(0.2, 0.6, 1, 0.7),
            bar_inactive_color=(0.2, 0.6, 1, 0.3),
            do_scroll_x=False
        )
        
        self.grid = GridLayout(
            cols=1,
            spacing=dp(20),
            padding=[dp(10), dp(20), dp(10), dp(20)],
            size_hint=(1, None),
            size_hint_y=None,
            row_default_height=dp(320)  # Ajustado para la nueva altura de la tarjeta
        )
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        self.load_combates()
        
        scroll.add_widget(self.grid)
        self.layout.add_widget(scroll)

        footer = BoxLayout(
            size_hint_y=None, 
            height=dp(60), 
            padding=[dp(30), dp(10), dp(30), dp(10)]
        )
        btn_volver = Button(
            text="Volver",
            font_size=sp(18),
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            on_press=lambda x: setattr(self.manager, 'current', 'torneos_anteriores')
        )
        footer.add_widget(btn_volver)
        self.layout.add_widget(footer)

    def load_combates(self):
        self.grid.clear_widgets()
        
        combates_data = [
            {
                "id": 1,
                "numero": 1,
                "fecha": "2024-01-15",
                "hora": "10:30",
                "categoria": "Peso Medio Masculino Senior",
                "competidor1": "Juan Pérez",
                "fecha_nac1": "15/05/1990",
                "peso1": 70.5,
                "altura1": 175,
                "sexo1": "Masculino",
                "nacionalidad1": "Mexicana",
                "peto_rojo": "ROJO123",
                "competidor2": "Carlos Gómez",
                "fecha_nac2": "22/08/1992",
                "peso2": 72.0,
                "altura2": 178,
                "sexo2": "Masculino",
                "nacionalidad2": "Mexicana",
                "peto_azul": "AZUL456",
                "area": "Área A",
                "Sede": "Tatami 1",
                "categoria_peso": "-70kg",
                "num_rounds": 3,
                "duracion_round": 3,
                "duracion_descanso": 1,
                "arbitro_nombre": "Luis Martínez",
                "arbitro_Apellidos": "García",
                "juez1_nombre": "Ana",
                "juez1_Apellidos": "Rodríguez",
                "juez2_nombre": "Pedro",
                "juez2_Apellidos": "Sánchez",
                "juez3_nombre": "María",
                "juez3_Apellidos": "López",
                "torneo_id": self.torneo_id
            },
            {
                "id": 2,
                "numero": 2,
                "fecha": "2024-01-15",
                "hora": "11:45",
                "categoria": "Peso Pesado Femenino Junior",
                "competidor1": "María López",
                "fecha_nac1": "10/03/1995",
                "peso1": 68.0,
                "altura1": 170,
                "sexo1": "Femenino",
                "nacionalidad1": "Mexicana",
                "peto_rojo": "ROJO456",
                "competidor2": "Ana Martínez",
                "fecha_nac2": "05/07/1994",
                "peso2": 67.5,
                "altura2": 169,
                "sexo2": "Femenino",
                "nacionalidad2": "Mexicana",
                "peto_azul": "AZUL789",
                "area": "Área B",
                "Sede": "Tatami 2",
                "categoria_peso": "-68kg",
                "num_rounds": 5,
                "duracion_round": 3,
                "duracion_descanso": 1,
                "arbitro_nombre": "Jorge Hernández",
                "arbitro_Apellidos": "López",
                "juez1_nombre": "Carlos",
                "juez1_Apellidos": "Gómez",
                "juez2_nombre": "Luisa",
                "juez2_Apellidos": "Fernández",
                "juez3_nombre": "Roberto",
                "juez3_Apellidos": "Díaz",
                "torneo_id": self.torneo_id
            }
        ]
        
        for combate in combates_data:
            card = CombateCard(
                combate_data=combate,
                on_delete=self.delete_combate,
                on_edit=self.edit_combate
            )
            self.grid.add_widget(card)

    def delete_combate(self, combate_data):
        print(f"Eliminando combate #{combate_data['numero']} - ID: {combate_data['id']}")
        self.show_message("Éxito", f"Combate #{combate_data['numero']} eliminado correctamente")
        self.load_combates()

    def edit_combate(self, combate_original, nuevos_datos):
        print(f"Actualizando combate #{combate_original['numero']} con:", nuevos_datos)
        for key, value in nuevos_datos.items():
            combate_original[key] = value
        
        self.show_message("Éxito", f"Combate #{combate_original['numero']} actualizado correctamente")
        self.load_combates()

    def show_message(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        lbl_mensaje = Label(
            text=message,
            color=(0.2, 0.6, 1, 1),
            font_size=sp(18),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80),
            text_size=(dp(400), None),
            shorten=False
        )
        content.add_widget(lbl_mensaje)

        btn_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        btn_aceptar = Button(
            text='ACEPTAR',
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=sp(18))
        btn_aceptar.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(btn_aceptar)

        content.add_widget(btn_layout)

        popup = Popup(
            title=title,
            title_color=(0.2, 0.6, 1, 1),
            title_size=sp(20),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=(dp(500), dp(250)),
            separator_height=0,
            background='',
            auto_dismiss=False
        )

        with popup.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            popup.rect = RoundedRectangle(
                pos=popup.pos,
                size=popup.size,
                radius=[dp(15)]
            )

        popup.bind(
            pos=lambda instance, value: setattr(popup.rect, 'pos', value),
            size=lambda instance, value: setattr(popup.rect, 'size', value)
        )

        popup.open()