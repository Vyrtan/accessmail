import imaplib
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import Canvas
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from src.database import Database
from functools import partial
import string
from kivy.core.window import Window
from kivy.properties import ObjectProperty

__author__ = 'ubuntu'

clunkyConfig = {
    2: {
        "IMAP": {
            "host": "imap.gmail.com",
            "port": 993,
            "ssl": True
        },
        "SMTP": {
            "host": "smtp.gmail.com",
            "port": 465,
            "ssl": True,
            "auth": True
        }
    },
    0: {
        "IMAP": {
            "host": "imap.gmx.net",
            "port": 993,
            "ssl": True
        },
        "SMTP": {
            "host": "mail.gmx.net",
            "port": 465,
            "ssl": True,
            "auth": True
        }
    },
    1: {
        "IMAP": {
            "host": "imap.web.de",
            "port": 993,
            "ssl": True
        },
        "SMTP": {
            "host": "smtp.web.de",
            "port": 587,
            "ssl": False,
            "auth": True
        }
    }
}

Builder.load_file("GUI/providerDataLayout.kv")


class ProviderDataLayout(GridLayout):

    """
    This class is the controller which manages the first start of the program.
    If no data are available yet, the user is asked to fill in his e-mail address and password.
    This class then connects to the server using the filled in information and (if valid)
    stores them in the database for future use.

    :param provider: The provider handed over by the previous widget (firstStartLayout)
    :param kwargs:
    """
    emailAddress = ObjectProperty()
    password = ObjectProperty()
    submitButt = ObjectProperty()

    def __init__(self, provider, **kwargs):
        super(ProviderDataLayout, self).__init__(**kwargs)
        self.provider = provider
        self.submitButt.bind(on_release=self.save_credentials)
        print self.provider

    def save_credentials(self, event):
        '''
        This method tries to connect to the server using the given information and (if successful)
        stores the gained data in the Inbox table of the database. This is used by the program to
        communicate with the server.

        :param event: no used, still passed by the callback
        :return:
        '''
        email = self.emailAddress.text
        password = self.password.text

        try:
            imapCon = imaplib.IMAP4_SSL(clunkyConfig[self.provider]["IMAP"]["host"])
            account = string.split(email, '@')[0]
            if(self.provider == 1):
                imapCon.login(account, password)
            else:
                imapCon.login(email, password)
            db = Database()
            db.create_inbox("test", "test", email, account, password,
                           clunkyConfig[self.provider]["IMAP"]["host"], clunkyConfig[self.provider]["SMTP"]["host"],
                           clunkyConfig[self.provider]["IMAP"]["port"], clunkyConfig[self.provider]["SMTP"]["port"],
                           clunkyConfig[self.provider]["IMAP"]["ssl"], clunkyConfig[self.provider]["SMTP"]["ssl"],
                           clunkyConfig[self.provider]["SMTP"]["auth"])
            db.close()
            imapCon.logout()
            self.parent.killMe()
            # we are still logged in, right?
        except imaplib.IMAP4.error as e:
            content = Button(text='Ein Fehler ist aufgetreten. \n Hier klicken, um es nocheinmal zu versuchen')
            popup = Popup(title='Error!', content=content,
                          size_hint=(None, None), size=(400, 400),
                          background="GUI/Icons/white_bg_400x400.png",
                          title_color=(0,0,0,1))
            content.bind(on_press=popup.dismiss)
            popup.open()
            print(e)

