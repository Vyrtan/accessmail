from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from Service import smtpsender
from Service.smtpsender import SMTPSender
from database import Database

__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('GUI/writelayout.kv')


class WriteLayout(Screen):

    mailText = ObjectProperty(None)
    sendTo = ObjectProperty(None)

    def send_mail(self):
        if self.sendTo.text == "":
            content = Button(text='An error occurred! Click here to try again')
            popup = Popup(title='Error!', content=content,
                          size_hint=(None, None), size=(400, 400))
            content.bind(on_press=popup.dismiss)
            popup.open()
        else:
            db = Database()
            inbox = db.getInbox()
            dicti = {
                'host': inbox.smtpServer,
                'port': inbox.smtpPort,
                'user': inbox.userMail,
                'pw': inbox.password,
                'ssl': inbox.smtpSSL
            }
            try:
                test = SMTPSender(dicti)
                test.connect()
                test.send_mail(inbox.userMail, self.sendTo.text, "test", self.mailText.text, None)
                content = Button(text='Worked!')
                popup = Popup(title='Worked!', content=content,
                              size_hint=(None, None), size=(400, 400))
                content.bind(on_press=popup.dismiss)
                popup.open()
            except Exception:
                content = Button(text='An error occurred! Click here to try again')
                popup = Popup(title='Error!', content=content,
                              size_hint=(None, None), size=(400, 400))
                content.bind(on_press=popup.dismiss)
                popup.open()
