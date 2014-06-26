from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from src.Service.smtpsender import SMTPSender
from src.database import Database
from kivy.uix.gridlayout import GridLayout

__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('GUI/writelayout.kv')


class WriteLayout(Screen):

    sendTo = ObjectProperty(None)
    subject = ObjectProperty(None)
    message = ObjectProperty(None)
    strSendTo = StringProperty()
    strSubject = StringProperty()
    strMessage = StringProperty()

    def __init__(self, **kwargs):
        super(WriteLayout, self).__init__(**kwargs)

    def on_strSendTo(self, instance, value):
        self.sendTo.text = value

    def on_strSubject(self, instance, value):
        self.subject.text = value

    def on_strMessage(self, instance, value):
        self.message.text = value


    def send_mail(self):
        if self.sendTo.text == "":
            content = GridLayout(cols=1)
            content.add_widget(Label(text="Bitte eine Nachricht eingeben"))
            content.add_widget(Button(background_normal="GUI/Icons/iConfirm.png", size_hint=[None, None]))
            popup = Popup(title='Fehler!', content=content,
                          size_hint=(None, None), size=(400, 400))
            content.bind(on_release=popup.dismiss)
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
                content.bind(on_release=popup.dismiss)
                popup.open()
                self.mailText = ""
            except Exception as e:
                print e
                # probably make this Popup an own kv and class (reusable everytime something goes wrong?)
                content = GridLayout(cols=1)
                content.add_widget(Label(text="Es ist ein Fehler aufgetreten"))
                butt = Button(background_normal="GUI/Icons/iConfirm.png", size_hint=[None, None])
                anch = AnchorLayout(align_h="center", size_hint=[None, None])
                anch.add_widget(butt)
                content.add_widget(anch)
                popup = Popup(title='Fehler!', content=content,
                              size_hint=(None, None), size=(400, 400))
                butt.bind(on_release=popup.dismiss)
                popup.open()
