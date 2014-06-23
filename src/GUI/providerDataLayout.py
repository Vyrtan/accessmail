import imaplib
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import Canvas
from kivy.graphics.vertex_instructions import Rectangle, Line
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

class ProviderDataLayout(GridLayout):

    def __init__(self, provider, **kwargs):
        super(ProviderDataLayout, self).__init__(**kwargs)

        self.selectable = []
        self.current_butt = 0

        self.cols = 1
        self.rows = 6
        self.row_default_height = .5
        self.padding = [10, 10]

        self.descriptionLabel = Label(text='Now you have to enter your user credentials,\n so we can get your mails', size_hint=(.1, .1), font_size=30)

        self.mailInputLabel = Label(text='Please enter your Email', size_hint=(.1, .1), font_size=40)
        self.mailInput = TextInput(text='', multiline=False, size_hint=(.1, .1), font_size=40, focus=True)

        self.pwInputLabel = Label(text='Please enter your Password', size_hint=(.1, .1), font_size=40)
        self.pwInput = TextInput(text='', multiline=False, size_hint=(.1, .1), font_size=40, password=True)

        self.add_widget(self.descriptionLabel)
        self.add_widget(self.mailInputLabel)
        self.add_widget(self.mailInput)
        self.add_widget(self.pwInputLabel)
        self.add_widget(self.pwInput)

        submitButton = Button(text='Save', size_hint=(.2, .1))
        submitButton.bind(on_press=partial(self.save_credentials, provider))
        self.add_widget(submitButton)

        self.selectable += [self.mailInput, self.pwInput, submitButton]

    def save_credentials(self, provider, event):
        print(self.pwInput.text)
        print(self.mailInput.text)


        try:
            imapCon = imaplib.IMAP4_SSL(clunkyConfig[provider]["IMAP"]["host"])
            email = self.mailInput.text
            account = string.split(email, '@')[0]
            if(provider == 1):
                imapCon.login(account, self.pwInput.text)
            else:
                imapCon.login(email, self.pwInput.text)
            db = Database()
            db.createInbox("test", "test", email, account, self.pwInput.text,
                           clunkyConfig[provider]["IMAP"]["host"], clunkyConfig[provider]["SMTP"]["host"],
                           clunkyConfig[provider]["IMAP"]["port"], clunkyConfig[provider]["SMTP"]["port"],
                           clunkyConfig[provider]["IMAP"]["ssl"], clunkyConfig[provider]["SMTP"]["ssl"],
                           clunkyConfig[provider]["SMTP"]["auth"])
            db.close()
            imapCon.logout()
            self.parent.killMe()
            # we are still logged in, right?
        except imaplib.IMAP4.error as e:
            content = Button(text='An error occurred! Click here to try again')
            popup = Popup(title='Error!', content=content,
                          size_hint=(None, None), size=(400, 400))
            content.bind(on_press=popup.dismiss)
            popup.open()
            print(e)

