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

    emailAddress = ObjectProperty()
    password = ObjectProperty()
    submitButt = ObjectProperty()

    def __init__(self, provider, **kwargs):
        super(ProviderDataLayout, self).__init__(**kwargs)
        self.provider = provider
        self.submitButt.bind(on_release=self.save_credentials)
        print self.provider

    def save_credentials(self, event):
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
            db.createInbox("test", "test", email, account, password,
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

