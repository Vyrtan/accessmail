import kivy
import os
from GUI.firstStartRootLayout import FirstStartRootApp

kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder

from kivy.core.window import Window

from .addressLayout import AddressLayout
from .writeLayout import WriteLayout
from .overviewLayout import OverviewLayout
from .readLayout import ReadLayout
from .menuLayout import MenuLayout
from .EmailItem import EmailItem
from .firstStartLayout import FirstStartLayout
from src.Controller.CommunicationController import CommunicationController
from kivy.clock import Clock

Builder.load_file("GUI/exitPopup.kv")


class Catalog(BoxLayout):
    screen_manager = ObjectProperty()
    buttons = ListProperty()

    def __init__(self, **kwargs):
        super(Catalog, self).__init__(**kwargs)
        self.current_butt = 0
        # alternative solution to rotate through buttons: kivy1.8.1 FocusBehaviour
        # Window.bind(on_key_down=self.rotate_buttons)
        # load emails from webserver here
        Clock.schedule_once(self.checkMails, 0)
        Clock.schedule_interval(self.checkMails, 300)


    def checkMails(self,_):
        CommunicationController.getEmailsFromServer()


    def show_layout(self, value, **param):
        if self.screen_manager.current == value:
            return
        if value == "Read":
            # read then contains the id for the email to be displayed
            param.setdefault("email", None)
            read = param["email"]
            self.screen_manager.current = value
            if read:
                self.screen_manager.current_screen.email = read
        elif value == "Write":
            param.setdefault("address", "None")
            param.setdefault("subject", "None")
            address = param["address"]
            if param["subject"] == "None":
                subject = "None"
            else:
                subject = "Re:" + param["subject"]
            self.screen_manager.current = value
            self.screen_manager.current_screen.strSendTo = address
            self.screen_manager.current_screen.strSubject = subject
        else:
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
        #if key == 13:
            # print("Return pressed")
            #.buttons[self.current_butt].trigger_action(duration=0)
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


# holy shit right click draws red circles!!