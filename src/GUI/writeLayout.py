from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from Service.smtpsender import SMTPSender
from src.database import Database

__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('GUI/writelayout.kv')


class WriteLayout(Screen):

    mailText = ObjectProperty(None)
    sendTo = ObjectProperty(None)
    subject = ObjectProperty(None)
    strSendTo = StringProperty()
    strSubject = StringProperty()

    def on_strSendTo(self, instance, value):
        self.sendTo.text = value

    def on_strSubject(self, instance, value):
        self.subject.text = value

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
            if(inbox.smtpServer=="smtp.web.de"):
                dicti = {
                    'host': inbox.smtpServer,
                    'port': inbox.smtpPort,
                    'user': inbox.account,
                    'pw': inbox.password,
                    'ssl': inbox.smtpSSL
                }
            else:
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
                test.send_mail(inbox.userMail, self.sendTo.text, self.subject.text, self.mailText.text, None)
                content = Button(text='Erfolgreich verschickt!')
                popup = Popup(title='Erfolgreich!', content=content,
                              size_hint=(None, None), size=(400, 400))
                content.bind(on_press=popup.dismiss)
                popup.open()
            except Exception as e:
                print e
                content = Button(text='Ein Fehler ist aufgetreten. Bitte versuchen Sie es nocheinmal.')
                popup = Popup(title='Fehler!', content=content,
                              size_hint=(None, None), size=(400, 400))
                content.bind(on_press=popup.dismiss)
                popup.open()
