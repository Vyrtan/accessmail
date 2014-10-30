import kivy
import os
from GUI.firstStartRootLayout import FirstStartRootApp
import gtk

kivy.require('1.8.0')

from kivy.app import App
from kivy.config import Config

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder

from kivy.core.window import Window

from .addressLayout import AddressLayout
from .writeLayout import WriteLayout
from .InboxLayout import InboxLayout
from .outboxLayout import OutboxLayout
from .readLayout import ReadLayout
from .menuLayout import MenuLayout
from .EmailItem import EmailItem
from .firstStartLayout import FirstStartLayout
from src.Controller.CommunicationController import CommunicationController
from kivy.clock import Clock
from src.database import Database

from src.models import Mails

Builder.load_file("GUI/exitPopup.kv")
Builder.load_file("GUI/resetPopup.kv")


class Catalog(BoxLayout):
    """
    This method is the main frame. It contains all the other widgets and the screenmanager
    which toggles through the respective layouts.
    This class will be responsible for the handling of keyboard inputs in later use.

    :param kwargs:
    """
    screen_manager = ObjectProperty()
    buttons = ListProperty()

    def __init__(self, **kwargs):
        super(Catalog, self).__init__(**kwargs)
        self.current_butt = 0
        # alternative solution to rotate through buttons: kivy1.8.1 FocusBehaviour
        # Window.bind(on_key_down=self.rotate_buttons)

    # switch between the available layouts like the inbox, write, addressbook, etc.
    def show_layout(self, value, **param):
        '''
        This method takes a parameter value which contains the name of the to-be displayed layout.
        It calles the screenmanager and (if necessary) hands over information about the called
        layout.

        possible values: Inbox, Outbox, Read, Write, Address

        :param value: The name of the Screen to be displayed
        :param param: Additional information about the layout.
        :return:
        '''
        if self.screen_manager.current == value:
            return
        if value == "Read":
            Window.clearcolor = (1,0.9,0.9,1)
            read = param.get("email", None)
            self.screen_manager.current = value
            if read:
                self.screen_manager.current_screen.email = read
            else:
                self.screen_manager.current_screen.email = self.empty_email()
        elif value == "Write":
            Window.clearcolor = (1,1,0.9,1)
            email = param.get("email", None)
            self.screen_manager.current = value
            if email:
                self.screen_manager.current_screen.email = email
            else:
                self.screen_manager.current_screen.email = self.empty_email()
        else:
            Window.clearcolor = (1,1,1,1)
            self.screen_manager.current = value
        return

    @staticmethod
    def empty_email():
        m = Mails()
        m._from = ""
        m.message = ""
        m.subject = ""
        return m

    # def triggerReset(self):
    #     p = ResetPopup()
    #     p.open()

    # currently not used method to rotate through menu buttons
    # there is no solution yet to get all available buttons in the currently displayed Layout
    # def rotate_buttons(self, keyboard, key,  *args):
    #     if key == 9:
    #         if self.current_butt < len(self.buttons)-1:
    #             self.current_butt += 1
    #         else:
    #             self.current_butt = 0
    #     if key == 13:
    #         print("Return pressed")
    #         .buttons[self.current_butt].trigger_action(duration=0)
    #         Set current_butt to 0?
    #         current_butt = 0
    #     print("leaving rotate buttons")

    def on_exit_press(self):
        '''
        This method opens up a confirmation popup to close the program.

        :return:
        '''
        p = ExitPopup()
        p.open()


class ExitPopup(Popup):
    pass


class ResetPopup(Popup):
    pass


class MainApp(App):
    '''
    This class is the main construct behind the kivy framework application.
    It is responsible for calling the containing widgets/layouts and for setting a few basic parameters.

    '''

    def build(self):
        '''
        This method is called when an instance of the MainApp is run.

        :return:
        '''
        self.title = "Accessmail"
        Config.set("input","mouse","mouse,disable_multitouch")

        # get the screen resolution
        window = gtk.Window()
        screen = window.get_screen()
        width =  screen.get_width()
        height = screen.get_height()

        # set the background color to white
        Window.clearcolor = (1, 1, 1, 1)

        # set the window size to the previously calculated screen resolution
        Window.size = width, height

        return Catalog()


# input form for email settings
class FirstStartApp(App):

    def build(self):
        return FirstStartLayout()
