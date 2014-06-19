import kivy

kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder

from kivy.core.window import Window

from .firstStartLayout import FirstStartLayout

Builder.load_file("GUI/exitPopup.kv")


class Catalog(BoxLayout):
    screen_manager = ObjectProperty()
    buttons = ListProperty()

    def __init__(self, **kwargs):
        super(Catalog, self).__init__(**kwargs)
        self.current_butt = 0
        Window.bind(on_key_down=self.rotate_buttons)
        print("catalog init called")

    def show_layout(self, value):
        self.screen_manager.current = value
        return

    def rotate_buttons(self, keyboard, key,  *args):
        # print("enter rotate button")
        # print("current_butt: %d" %(self.current_butt))
        # print("current button: %s" %self.buttons[self.current_butt].text)
        if key == 9:
            if self.current_butt < len(self.buttons)-1:
                self.current_butt += 1
            else:
                self.current_butt = 0
        if key == 13:
            # print("Return pressed")
            self.buttons[self.current_butt].trigger_action(duration=0)
            # Set current_butt to 0?
            # current_butt = 0
        # print("leaving rotate buttons")

    def on_exit_press(self):
        p = ExitPopup()
        p.open()


class ExitPopup(Popup):
    pass


class MainApp(App):
    def build(self):
        self.title = "Accessmail"

        #set the background colour of the application
        Window.clearcolor = (1, 1, 1, 1)

        #this starts the application in fullscreen, it doesn't look good though
        #Window.fullscreen = True
        return Catalog()


# input form for email settings
class FirstStartApp(App):
    def build(self):
        return FirstStartLayout()

firstStart_bool = False

if __name__ == "__main__":
    if firstStart_bool:
        FirstStartApp().run()
    else:
        MainApp().run()

# holy shit right click draws red circles!!