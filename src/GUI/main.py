import kivy

kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivy.core.window import Window

from src.GUI.addressLayout import AddressLayout
from src.GUI.writeLayout import WriteLayout
from src.GUI.overviewLayout import OverviewLayout
from src.GUI.readLayout import ReadLayout
from src.GUI.menuLayout import MenuLayout
from src.GUI.firstStartLayout import FirstStartLayout


class Catalog(BoxLayout):

    def __init__(self, **kwargs):
        super(Catalog, self).__init__(**kwargs)
        screen_manager = ObjectProperty()
        buttons = ListProperty()
        self.current_butt = 0
        Window.bind(on_key_down=self.rotate_buttons)

    def show_layout(self, value):
        print(type(self.buttons))
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


class MainApp(App):
    def build(self):
        return Catalog()


class FirstStartApp(App):
    def build(self):
        return FirstStartLayout()

firstStart_bool = False

if __name__ == "__main__":
    if firstStart_bool:
        FirstStartApp().run()
    else:
        MainApp().run()