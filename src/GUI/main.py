import kivy

kivy.require('1.7.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.lang import Builder


#from kivy.core.window import Window


from src.GUI.addressLayout import AddressLayout
from src.GUI.writeLayout import WriteLayout
from src.GUI.overviewLayout import OverviewLayout
from src.GUI.readLayout import ReadLayout
from src.GUI.menuLayout import MenuLayout


class MenuLayout(BoxLayout):
    pass


class Catalog(BoxLayout):
    pass


# def rotate_buttons(keyboard, key,  *args):
#     print("rotate buttons entered")
#     # global current_butt
#     if key == 9:
#         current_butt += 1
#         print("Nachher %s" %(current_butt))
#     if key == 13:
#         print("Return pressed")
#         sm.current_screen.mn.buttons[current_butt].on_press()
#     print("leaving rotate buttons")
#     return
# Window.bind(on_key_down=rotate_buttons)


class MainApp(App):
    def build(self):
        return Catalog()

if __name__ == "__main__":
    MainApp().run()