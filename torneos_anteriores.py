from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp, sp
from kivy.properties import ListProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class HoverButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.1, 0.4, 0.7, 1)
        self.color = (1, 1, 1, 1)
        self.size_hint_y = None
        self.height = dp(50)
        self.font_size = sp(22)
        self.bold = True
        self.border_radius = dp(12)

        with self.canvas.before:
            Color(*self.background_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.border_radius])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

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

class ConfirmDeletePopup(Popup):
    def __init__(self, torneo_data, on_confirm, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Confirmar Eliminación'
        self.title_color = (0.2, 0.6, 1, 1)
        self.title_size = sp(22)
        self.title_align = 'center'
        self.size_hint = (None, None)
        self.size = (dp(450), dp(250))
        self.torneo_data = torneo_data
        self.on_confirm = on_confirm
        self.background = ''
        self.separator_height = 0
        self.auto_dismiss = False

        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        message = Label(
            text=self._format_message(torneo_data["nombre"]),
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

    def _format_message(self, nombre_torneo):
        max_len = 25
        if len(nombre_torneo) > max_len:
            mid_point = len(nombre_torneo) // 2
            split_point = nombre_torneo.rfind(' ', 0, mid_point + 10)
            if split_point == -1:
                split_point = mid_point
            nombre_formateado = (nombre_torneo[:split_point] + '\n' + 
                                nombre_torneo[split_point:])
        else:
            nombre_formateado = nombre_torneo
        
        return f'¿Estás seguro que deseas eliminar\nel torneo:\n"[b]{nombre_formateado}[/b]"?'

    def confirm_delete(self, instance):
        self.on_confirm(self.torneo_data)
        self.dismiss()

class TorneoCard(BoxLayout):
    bg_color = ListProperty([0.1, 0.4, 0.7, 1])

    def __init__(self, torneo_data, on_delete, on_edit, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(30)
        self.size_hint = (1, None)
        self.height = dp(300)
        self.torneo_data = torneo_data
        self.on_delete_callback = on_delete
        self.on_edit_callback = on_edit

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
            self.bind(pos=self.update_rect, size=self.update_rect)

        self.title_label = Label(
            text=f"[b]{torneo_data['nombre']}[/b]",
            markup=True,
            font_size=sp(22),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        self.add_widget(self.title_label)

        self.info_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        self.info_layout.add_widget(self.create_info_row(f"Fecha: {torneo_data['fecha']}"))
        self.info_layout.add_widget(self.create_info_row(f"Horario: {torneo_data['hora_inicio']} - {torneo_data['hora_fin']}"))
        self.info_layout.add_widget(self.create_info_row(f"Sede: {torneo_data['Sede']}"))
        self.add_widget(self.info_layout)

        self.button_layout = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=dp(50), 
            spacing=dp(10),
            padding=[0, dp(10), 0, 0]
        )
        
        self.edit_button = LightBlueButton(text='EDITAR', size_hint_x=0.5)
        self.edit_button.bind(on_press=self.open_edit_screen)
        
        self.delete_button = LightBlueButton(text='ELIMINAR', size_hint_x=0.5)
        self.delete_button.bind(on_press=self.open_delete_popup)
        
        self.button_layout.add_widget(self.edit_button)
        self.button_layout.add_widget(self.delete_button)
        self.add_widget(self.button_layout)

        self.bind(on_touch_down=self.navigate_to_combates)

    def create_info_row(self, text):
        return Label(
            text=text,
            font_size=sp(18),
            color=(0.95, 0.95, 0.95, 1),
            halign='left',
            size_hint_y=None,
            height=dp(25)
        )

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def open_delete_popup(self, instance):
        ConfirmDeletePopup(
            torneo_data=self.torneo_data,
            on_confirm=self.on_delete_callback
        ).open()

    def open_edit_screen(self, instance):
        app = App.get_running_app()
        if not app.root.has_screen('actualizar_torneos'):
            from actualizar_torneos import ActualizarTorneoScreen
            app.root.add_widget(ActualizarTorneoScreen(
                name='actualizar_torneos',
                torneo_data=self.torneo_data,
                on_save=self.on_edit_callback
            ))
        
        app.root.current = 'actualizar_torneos'

    def navigate_to_combates(self, instance, touch):
        if self.collide_point(*touch.pos) and not any(child.collide_point(*touch.pos) for child in self.children):
            app = App.get_running_app()
            if not app.root.has_screen('combates_anteriores'):
                from combates_anteriore import CombatesScreen
                app.root.add_widget(CombatesScreen(name='combates_anteriores'))
            
            combates_screen = app.root.get_screen('combates_anteriores')
            combates_screen.torneo_nombre = self.torneo_data['nombre']
            combates_screen.torneo_id = 1  
            combates_screen.build_ui()
            app.root.current = 'combates_anteriores'
            return True
        return False

class TorneosAnterioresScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        Window.bind(on_resize=self.update_columns)

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(pos=self.layout.pos, size=self.layout.size)
            self.layout.bind(pos=self.update_rect, size=self.update_rect)

        self.header = BoxLayout(size_hint_y=None, height=dp(100))
        self.title_label = Label(
            text='Administrar Torneos',
            font_size=sp(40),
            bold=True,
            color=(0.1, 0.1, 0.2, 1)
        )
        self.header.add_widget(self.title_label)
        self.layout.add_widget(self.header)

        self.scroll = ScrollView()
        self.grid = GridLayout(
            cols=4,
            spacing=dp(20),
            padding=dp(20),
            size_hint_y=None,
            row_default_height=dp(320)
        )
        self.grid.bind(minimum_height=self.grid.setter('height'))

        self.torneos_data = [
            {"nombre": "Torneo Internacional 2024", "fecha": "2024-01-15", "hora_inicio": "09:00", "hora_fin": "18:00", "Sede": "Sala de armas"},
            {"nombre": "Copa América 2024", "fecha": "2024-02-20", "hora_inicio": "08:30", "hora_fin": "17:30", "Sede": "Sala de armas"},
            {"nombre": "Euro Championship", "fecha": "2024-03-10", "hora_inicio": "10:00", "hora_fin": "19:00", "Sede": "Sala de armas"},
            {"nombre": "Asia Open 2024", "fecha": "2024-04-05", "hora_inicio": "08:00", "hora_fin": "16:00", "Sede": "Sala de armas"},
        ]
        self.populate_torneos()

        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)

        self.footer = BoxLayout(
            size_hint_y=None,
            height=dp(80),
            padding=dp(20))

        self.btn_volver = Button(
            text='Volver',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size=sp(22),
            size_hint=(0.5, 1),
            pos_hint={'center_x': 0.5},
            on_press=lambda x: setattr(self.manager, 'current', 'ini')
        )
        self.footer.add_widget(self.btn_volver)
        self.layout.add_widget(self.footer)

        self.add_widget(self.layout)
        self.update_columns()

    def populate_torneos(self):
        self.grid.clear_widgets()
        for torneo in self.torneos_data:
            card = TorneoCard(
                torneo_data=torneo,
                on_delete=self.delete_torneo,
                on_edit=self.edit_torneo
            )
            self.grid.add_widget(card)

    def delete_torneo(self, torneo_a_eliminar):
        self.torneos_data = [torneo for torneo in self.torneos_data if torneo['nombre'] != torneo_a_eliminar['nombre']]
        self.populate_torneos()

    def edit_torneo(self, torneo_original, nuevos_datos):
        for i, torneo in enumerate(self.torneos_data):
            if torneo['nombre'] == torneo_original['nombre']:
                self.torneos_data[i] = nuevos_datos
                break
        self.populate_torneos()

    def update_rect(self, *args):
        self.rect.pos = self.layout.pos
        self.rect.size = self.layout.size

    def update_columns(self, *args):
        width = Window.width
        if width > 1200:
            cols = 4
        elif width > 900:
            cols = 3
        elif width > 600:
            cols = 2
        else:
            cols = 1

        self.grid.cols = cols
        self.grid.spacing = dp(20) if cols > 1 else dp(10)
        self.grid.padding = dp(20) if cols > 1 else dp(10)

class TorneosApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TorneosAnterioresScreen(name='torneos_anteriores'))
        return sm

if __name__ == '__main__':
    TorneosApp().run()