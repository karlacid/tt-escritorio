from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.widget import Widget
from kivy.utils import platform
from threading import Thread
from api_client import api  


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
        """Retorna el ancho del formulario según el tamaño de ventana"""
        width = Window.width
        if width < 600:
            return 0.95
        elif width < 900:
            return 0.85
        elif width < 1200:
            return 0.7
        else:
            return 0.5
    
    @staticmethod
    def get_font_size(base_size):
        """Retorna tamaño de fuente responsive"""
        width = Window.width
        if width < 600:
            return sp(base_size * 0.7)
        elif width < 900:
            return sp(base_size * 0.85)
        return sp(base_size)
    
    @staticmethod
    def get_popup_size():
        """Retorna tamaño apropiado para popups"""
        width = Window.width
        height = Window.height
        if width < 600:
            return (width * 0.9, min(height * 0.4, dp(300)))
        else:
            return (min(width * 0.6, dp(450)), min(height * 0.35, dp(250)))
    
    @staticmethod
    def get_logo_height():
        """Retorna altura del logo responsive"""
        width = Window.width
        height = Window.height
        if width < 600:
            return dp(80)
        elif width < 900:
            return dp(100)
        return min(dp(120), height * 0.12)


# ------------------ TEXT INPUT REDONDEADO RESPONSIVE ------------------
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
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(12)]
            )
            Color(1, 1, 1, 0.3)
            self.border_rect = RoundedRectangle(
                pos=(self.pos[0]+dp(2), self.pos[1]+dp(2)),
                size=(self.size[0]-dp(4), self.size[1]-dp(4)),
                radius=[dp(10)]
            )

        self.bind(pos=self._update_rects, size=self._update_rects)
        Window.bind(on_resize=self.on_window_resize)

    def _update_rects(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_rect.pos = (self.pos[0]+dp(2), self.pos[1]+dp(2))
        self.border_rect.size = (self.size[0]-dp(4), self.size[1]-dp(4))
    
    def on_window_resize(self, instance, width, height):
        self.font_size = ResponsiveHelper.get_font_size(18)
        self.height = dp(55)

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
                    radius=[dp(10)]
                )
        else:
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
                    radius=[dp(10)]
                )
            self._update_rects()


# ------------------ BOTÓN HOVER RESPONSIVE ------------------
class HoverButton(Button):
    def __init__(self, **kwargs):
        bg_color = kwargs.pop('bg_color', None)
        super().__init__(**kwargs)
        
        if bg_color is None:
            bg_color = self.background_color if hasattr(self, 'background_color') else (0.1, 0.4, 0.7, 1)
        
        self.background_normal = ''
        self.background_color = bg_color
        self.color = (1, 1, 1, 1)
        self.size_hint_y = None
        self.height = dp(50)
        self.font_size = ResponsiveHelper.get_font_size(18)
        self.bold = True
        self.border_radius = dp(12)

        with self.canvas.before:
            Color(*self.background_color)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.border_radius]
            )
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        Window.bind(on_resize=self.on_window_resize)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_window_resize(self, instance, width, height):
        self.font_size = ResponsiveHelper.get_font_size(18)
        self.height = dp(50)


# ------------------ PANTALLA INICIO SESIÓN JUEZ RESPONSIVE ------------------
class InicioSesionJuezScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'ini_juez'
        
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.screen_bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_screen_bg, pos=self._update_screen_bg)
        
        self.build_ui()
        Window.bind(on_resize=self.on_window_resize)
    
    def _update_screen_bg(self, *args):
        self.screen_bg.size = self.size
        self.screen_bg.pos = self.pos

    def build_ui(self):
        self.clear_widgets()
        
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(10),
            size_hint=(1, 1)
        )

        main_layout.add_widget(Widget(size_hint_y=0.1))

        form_container = BoxLayout(
            orientation='vertical',
            size_hint=(ResponsiveHelper.get_form_width(), None),
            pos_hint={'center_x': 0.5},
            spacing=dp(12)
        )
        form_container.bind(minimum_height=form_container.setter('height'))

        logo_height = ResponsiveHelper.get_logo_height()
        logo = Image(
            source="Imagen5-Photoroom.png",
            size_hint=(1, None),
            height=logo_height,
            fit_mode="contain"
        )
        form_container.add_widget(logo)

        titulo = Label(
            text='INICIO DE SESIÓN',
            font_size=ResponsiveHelper.get_font_size(32),
            color=(0.1, 0.4, 0.7, 1),
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )
        form_container.add_widget(titulo)

        titulo2 = Label(
            text='TABLERO CENTRAL',
            font_size=ResponsiveHelper.get_font_size(40),
            color=(0.7, 0.1, 0.1, 1),
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )
        form_container.add_widget(titulo2)

        form_container.add_widget(Widget(size_hint_y=None, height=dp(8)))

        campos_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            size_hint_y=None
        )
        campos_layout.bind(minimum_height=campos_layout.setter('height'))

        contrasena_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(6),
            size_hint_y=None
        )
        contrasena_layout.bind(minimum_height=contrasena_layout.setter('height'))
        
        contrasena_label = Label(
            text='Contraseña del Combate',
            font_size=ResponsiveHelper.get_font_size(18),
            color=(0.1, 0.1, 0.2, 1),
            size_hint_y=None,
            height=dp(25),
            halign='left'
        )
        contrasena_label.bind(size=contrasena_label.setter('text_size'))
        contrasena_layout.add_widget(contrasena_label)
        
        self.contrasena_input = RoundedTextInput(hint_text='Ingrese contraseña', password=True)
        contrasena_layout.add_widget(self.contrasena_input)
        campos_layout.add_widget(contrasena_layout)

        form_container.add_widget(campos_layout)
        form_container.add_widget(Widget(size_hint_y=None, height=dp(12)))

        botones_layout = BoxLayout(
            orientation='horizontal' if Window.width > 600 else 'vertical',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(50) if Window.width > 600 else dp(110)
        )

        btn_iniciar = HoverButton(
            text='ACCEDER AL COMBATE',
            background_color=(0.1, 0.4, 0.7, 1)
        )
        btn_iniciar.bind(on_press=self.iniciar_sesion)
        botones_layout.add_widget(btn_iniciar)

        btn_volver = HoverButton(
            text='VOLVER',
            background_color=(0.7, 0.1, 0.1, 1)
        )
        btn_volver.canvas.before.clear()
        with btn_volver.canvas.before:
            Color(0.7, 0.1, 0.1, 1)
            btn_volver.rect = RoundedRectangle(
                pos=btn_volver.pos,
                size=btn_volver.size,
                radius=[btn_volver.border_radius]
            )
        btn_volver.bind(on_press=self.volver)
        botones_layout.add_widget(btn_volver)

        form_container.add_widget(botones_layout)
        form_container.add_widget(Widget(size_hint_y=None, height=dp(8)))

        main_layout.add_widget(form_container)
        main_layout.add_widget(Widget(size_hint_y=0.1))

        self.add_widget(main_layout)

    def on_window_resize(self, instance, width, height):
        Clock.schedule_once(lambda dt: self.build_ui(), 0.1)

    def on_enter(self, *args):
        Clock.schedule_once(self.establecer_foco, 0.1)

    def establecer_foco(self, dt):
        if hasattr(self, 'contrasena_input'):
            self.contrasena_input.focus = True

    def iniciar_sesion(self, instance):
        """Valida la contraseña contra el backend usando api_client"""
        contrasena = self.contrasena_input.text.strip()
        
        if not contrasena:
            self.mostrar_mensaje("Error", "Por favor ingrese una contraseña")
            return
        
        self.mostrar_loading()
    
        def hacer_login():
            try:
                print(f"[InicioSesionJuez] 🔐 Intentando login con contraseña: {contrasena}")
                
                # ✅ PASO 1: Login usando api_client
                response = api.session.post(
                    f"{api.base_url}/api/auth/juez/login",
                    json={'password': contrasena},
                    headers={'Content-Type': 'application/json'},
                    timeout=5
                )
                
                if response.status_code == 200:
                    result = response.json()
                    combate_id = result.get('combateId')
                    
                    print(f"[InicioSesionJuez] ✓ Login exitoso - CombateId: {combate_id}")
                    
                    # ✅ PASO 2: Preparar el combate (WebSocket)
                    try:
                        print(f"[InicioSesionJuez] 🔌 Preparando WebSocket para combate {combate_id}...")
                        prepare_response = api.prepare_combate(combate_id)
                        print(f"[InicioSesionJuez] ✓ Combate preparado: {prepare_response}")
                    except Exception as e:
                        print(f"[InicioSesionJuez] ⚠️ Error preparando combate (continuando): {e}")
                    
                    # ✅ PASO 3: Obtener datos del combate usando api_client
                    combate_data = api.get_combate_by_id(combate_id)
                    print(f"[InicioSesionJuez] 📋 Datos del combate: {combate_data}")
                    
                    # ✅ PASO 4: Extraer competidores directamente del combate
                    competidor_rojo = combate_data.get('competidorRojo', {})
                    competidor_azul = combate_data.get('competidorAzul', {})
                
                    # Extraer nombres (pueden venir como 'nombres' o 'nombreAlumno')
                    nombre_rojo = competidor_rojo.get('nombres') or competidor_rojo.get('nombreAlumno', 'ROJO')
                    nombre_azul = competidor_azul.get('nombres') or competidor_azul.get('nombreAlumno', 'AZUL')
                    
                    # Extraer nacionalidades (si existen)
                    nacionalidad_rojo = competidor_rojo.get('nacionalidad', 'MX')
                    nacionalidad_azul = competidor_azul.get('nacionalidad', 'MX')
                    
                    # IDs de los alumnos
                    id_rojo = competidor_rojo.get('id')
                    id_azul = competidor_azul.get('id')
                    
                    # Preparar datos del combate
                    combate_completo = {
                        'idCombate': combate_id,
                        'idAlumnoRojo': id_rojo,
                        'idAlumnoAzul': id_azul,
                        'duracionRound': combate_data.get('duracionRound', '00:03:00'),
                        'duracionDescanso': combate_data.get('duracionDescanso', '00:01:00'),
                        'numeroRounds': combate_data.get('numeroRound', 3)
                    }
                    
                    print(f"[InicioSesionJuez] ✅ Datos completos:")
                    print(f"  Combate ID: {combate_id}")
                    print(f"  🔴 ROJO: {nombre_rojo} (ID: {id_rojo})")
                    print(f"  🔵 AZUL: {nombre_azul} (ID: {id_azul})")
                    
                    # Programar la transición
                    Clock.schedule_once(lambda dt: self.ir_a_tablero(
                        nombre_rojo,
                        nacionalidad_rojo,
                        nombre_azul,
                        nacionalidad_azul,
                        combate_completo
                    ), 0)
                    
                else:
                    error_msg = "Contraseña incorrecta"
                    try:
                        error_data = response.json()
                        error_msg = error_data.get('message', error_msg)
                    except:
                        pass
                    
                    print(f"[InicioSesionJuez] ✗ Login fallido: {error_msg}")
                    Clock.schedule_once(lambda dt: self.mostrar_mensaje("Error", error_msg), 0)
                    
            except Exception as e:
                print(f"[InicioSesionJuez] ✗ Error inesperado: {e}")
                import traceback
                traceback.print_exc()
                Clock.schedule_once(lambda dt: self.mostrar_mensaje(
                    "Error", 
                    f"Error de conexión: {str(e)}"
                ), 0)
            finally:
                Clock.schedule_once(lambda dt: self.cerrar_loading(), 0)
    
        login_thread = Thread(target=hacer_login)
        login_thread.daemon = True
        login_thread.start()

    def ir_a_tablero(self, nombre_rojo, nat_rojo, nombre_azul, nat_azul, combate_data):
        """Navega al tablero central con los datos del combate"""
        try:
            print("[InicioSesionJuez] 🎯 Navegando al tablero central...")
            
            # Obtener la pantalla del tablero
            tablero_screen = self.manager.get_screen('tablero_central')
            
            # Configurar los competidores
            tablero_screen.set_competitors(
                name1=nombre_rojo,
                nat1=nat_rojo,
                name2=nombre_azul,
                nat2=nat_azul,
                combate_data=combate_data
            )
            
            # Cambiar a la pantalla del tablero
            self.manager.current = 'tablero_central'
            
            print("[InicioSesionJuez] ✓ Navegando al tablero central")
            
        except Exception as e:
            print(f"[InicioSesionJuez] ✗ Error navegando al tablero: {e}")
            import traceback
            traceback.print_exc()
            self.mostrar_mensaje("Error", f"No se pudo acceder al tablero: {str(e)}")

    def volver(self, instance):
        """Regresa a la pantalla principal"""
        try:
            # Limpiar el input de contraseña
            if hasattr(self, 'contrasena_input'):
                self.contrasena_input.text = ""
            
            # Navegar a la pantalla principal
            self.manager.current = 'main'
            print("[InicioSesionJuez] 👈 Volviendo a pantalla principal")
        except Exception as e:
            print(f"[InicioSesionJuez] ✗ Error al volver: {e}")

    def mostrar_loading(self):
        """Muestra un popup de carga"""
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(30)
        )
        
        lbl_mensaje = Label(
            text="Verificando contraseña...",
            color=(0.1, 0.4, 0.7, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            halign='center',
            valign='middle'
        )
        content.add_widget(lbl_mensaje)
        
        popup_size = ResponsiveHelper.get_popup_size()
        self.loading_popup = Popup(
            title="Cargando",
            title_color=(1, 1, 1, 1),
            title_size=ResponsiveHelper.get_font_size(22),
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=(popup_size[0], dp(150)),
            separator_height=0,
            background='',
            auto_dismiss=False
        )
        
        with self.loading_popup.canvas.before:
            Color(0.1, 0.4, 0.7, 1)
            self.loading_popup.rect = RoundedRectangle(
                pos=self.loading_popup.pos,
                size=self.loading_popup.size,
                radius=[dp(15)]
            )
        
        def update_popup_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        
        self.loading_popup.bind(pos=update_popup_rect, size=update_popup_rect)
        self.loading_popup.open()
    
    def cerrar_loading(self):
        """Cierra el popup de carga"""
        if hasattr(self, 'loading_popup'):
            self.loading_popup.dismiss()

    def mostrar_mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente"""
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20)
        )
        
        lbl_mensaje = Label(
            text=mensaje,
            color=(0.1, 0.4, 0.7, 1),
            font_size=ResponsiveHelper.get_font_size(18),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80)
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


# ------------------ APP DE PRUEBA ------------------
if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager
    
    class TestApp(App):
        def build(self):
            sm = ScreenManager()
            sm.add_widget(InicioSesionJuezScreen(name='ini_juez'))
            return sm
    
    TestApp().run()