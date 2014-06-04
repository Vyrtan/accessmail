import kivy
kivy.require('1.7.0')


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from GUI.addressLayout import AddressLayout
from GUI.writeLayout import WriteLayout
from GUI.overviewLayout import OverviewLayout
from GUI.readLayout import ReadLayout



def switch_to(str):
    sm.current = str


def doSomething(keyboard, key, *args):
    print(key)


def close_keyboard():
    print("Keyboard closed now.")


sm = ScreenManager()
sm.add_widget(OverviewLayout(name='overview'))
sm.add_widget(WriteLayout(name='write'))
sm.add_widget(ReadLayout(name='read'))
sm.add_widget(AddressLayout(name='address'))
current_butt = 0


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
        return sm

if __name__ == "__main__":
    MainApp().run()