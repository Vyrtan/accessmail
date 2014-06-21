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
from database import Database

__author__ = 'ubuntu'

clunkyConfig = {
    0: {
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
    }
}


class ProviderDataLayout(GridLayout):

    def __init__(self, **kwargs):
        super(ProviderDataLayout, self).__init__(**kwargs)

        self.cols = 1
        self.rows = 6
        self.row_default_height = .5
        self.padding = [10, 10]

        self.descriptionLabel = Label(text='Now you have to enter your user credentials,\n so we can get your mails', size_hint=(.1, .1), font_size=30)

        self.mailInputLabel = Label(text='Please enter you Email', size_hint=(.1, .1), font_size=40)
        self.mailInput = TextInput(text='Hello world', multiline=False, size_hint=(.1, .1), font_size=40)

        self.pwInputLabel = Label(text='Please enter you Password', size_hint=(.1, .1), font_size=40)
        self.pwInput = TextInput(text='', multiline=False, size_hint=(.1, .1), font_size=40, password=True)

        self.add_widget(self.descriptionLabel)
        self.add_widget(self.mailInputLabel)
        self.add_widget(self.mailInput)
        self.add_widget(self.pwInputLabel)
        self.add_widget(self.pwInput)

        submitButton = Button(text='Save', size_hint=(.2, .1))
        submitButton.bind(on_press=self.save_credentials)
        self.add_widget(submitButton)

    def save_credentials(self, event):
        print(self.pwInput.text)
        print(self.mailInput.text)

        imapCon = None
        if(clunkyConfig[0]["SMTP"]["ssl"]):
            imapCon = imaplib.IMAP4_SSL(clunkyConfig[0]["IMAP"]["host"])

        try:
            imapCon.login(self.mailInput.text, self.pwInput.text)
            db = Database()
            db.createInbox("test", "test", self.mailInput.text, "hans", self.pwInput.text,
                           clunkyConfig[0]["IMAP"]["host"], clunkyConfig[0]["SMTP"]["host"],
                           clunkyConfig[0]["IMAP"]["port"], clunkyConfig[0]["SMTP"]["port"],
                           clunkyConfig[0]["IMAP"]["ssl"], clunkyConfig[0]["SMTP"]["ssl"],
                           clunkyConfig[0]["SMTP"]["auth"])
            db.close()
            self.parent.killMe()
        except imaplib.IMAP4.error as e:
            content = Button(text='An error occurred! Click here to try again')
            popup = Popup(title='Error!', content=content,
                          size_hint=(None, None), size=(400, 400))
            content.bind(on_press=popup.dismiss)
            popup.open()
            print(e)


