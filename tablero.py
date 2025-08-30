from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager

class CompetitorPanel(BoxLayout):
    score = NumericProperty(0)
    penalty_score = NumericProperty(0)

    def __init__(self, name, color, nationality="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 15
        self.name = name
        self.bg_color = color
        self.nationality = nationality

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        if self.nationality:
            self.add_widget(Label(text=self.nationality.upper(), font_size=20, bold=True, color=(1, 1, 1, 1)))

        self.add_widget(Label(text=name, font_size=30, bold=True, color=(1, 1, 1, 1)))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class CenterPanel(BoxLayout):
    time_str = StringProperty("00:00")
    round_str = StringProperty("Round 1")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 10

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.add_widget(Label(text="RONDA ACTUAL", font_size=20, color=(0, 0, 0, 1)))
        self.round_label = Label(text=self.round_str, font_size=40, color=(0, 0, 0, 1))
        self.add_widget(self.round_label)

        self.add_widget(Label(text="TIEMPO", font_size=20, color=(0, 0, 0, 1)))
        self.time_label = Label(text=self.time_str, font_size=50, color=(0, 0, 0, 1))
        self.add_widget(self.time_label)

       
        self.back_button = Button(text="VOLVER", size_hint=(1, 0.2),
                                  background_color=(0.1, 0.4, 0.7, 1), color=(1, 1, 1, 1),
                                  on_press=self.go_back)
        self.add_widget(self.back_button)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def go_back(self, instance):
        screen_manager = self.parent.parent.parent
        screen_manager.current = 'combates_anteriores'

class MainScreentab(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = BoxLayout(spacing=0)

        self.com1_panel = CompetitorPanel(name="COM1", color=(0.117, 0.533, 0.898), nationality="KOR")
        main_layout.add_widget(self.com1_panel)

        self.center_panel = CenterPanel()
        main_layout.add_widget(self.center_panel)

        self.com2_panel = CompetitorPanel(name="COM2", color=(0.898, 0.2, 0.2), nationality="USA")
        main_layout.add_widget(self.com2_panel)

        self.add_widget(main_layout)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreentab(name='main_screen'))
        sm.add_widget(Screen(name='combates_anteriores'))  
        return sm

if __name__ == '__main__':
    MyApp().run()
