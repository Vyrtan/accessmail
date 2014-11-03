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

    """
    This method is used to handle the writing and sending of an e-mail.

    :param kwargs:
    """
    sendTo = ObjectProperty(None)
    subject = ObjectProperty(None)
    message = ObjectProperty(None)
    email = ObjectProperty()

    def __init__(self, **kwargs):
        super(WriteLayout, self).__init__(**kwargs)
        self.email = None

    def on_email(self, instance, value):
        if self.email:
            self.display_email(value)
        else:
            self.sendTo.text = ""
            self.subject.text = ""
            self.message.text = ""

    def display_email(self, email):
        self.sendTo.text = email._from
        if len(email.subject) > 0:
            if not email.subject.startswith("Re:"):
                self.subject.text = "Re: " + email.subject
            else:
                self.subject.text = email.subject
        else:
            self.subject.text = ""
        self.message.text = self.format_reply_message(email) if len(email.message) > 0 else ""

    @staticmethod
    def format_reply_message(email):
        '''
        This method takes the message of the displayed e-mail and converts it to the usual Reply-Mail format.
        :return:
        '''
        if len(email.message) > 0:
            replyString = email.message.split("\n")
        else:
            replyString = ""
        if len(email._from) > 0:
            replyHeader = "\n>" + email._from + " wrote on " + email.date + ":\n>"
        else:
            replyHeader = ""
        return replyHeader +'\n>'.join(replyString)

    def send_mail(self):
        '''
        This method is used to get the information necessary to send an e-mail from the inbox,
        connects to the database and sends the information to the remote server. We have to differ
        between the offered providers.

        :return:
        '''
        if self.sendTo.text == "":
            content = GridLayout(cols=1)
            content.add_widget(Label(text="Please enter a message"))
            content.add_widget(Button(background_normal="GUI/Icons/iConfirm.png", size_hint=[None, None]))
            popup = Popup(title='Error!', content=content,
                          size_hint=(None, None), size=(400, 400),
                          background="GUI/Icons/white_bg_400x400.png",
                          title_color=(0,0,0,1))
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
                test.send_mail(inbox.userMail, self.sendTo.text, self.subject.text, self.message.text, None)
                box = GridLayout(cols=1)
                anch1 = AnchorLayout(anchor_h="center")
                lbl = Label(text="Message successfully sent!", font_size=22, bold=True)
                anch1.add_widget(lbl)
                anch2 = AnchorLayout(anchor_h="center")
                butt = Button(background_normal="GUI/Icons/iConfirm.png", size_hint=[None, None])
                anch2.add_widget(butt)
                box.add_widget(anch1)
                box.add_widget(anch2)

                content = box
                popup = Popup(title='Success!', content=content,
                              size_hint=(None, None), size=(400, 400),
                              background="GUI/Icons/white_bg_400x400.png",
                              title_color=(0,0,0,1))
                content.bind(on_release=popup.dismiss)
                butt.bind(on_release=popup.dismiss)
                popup.open()
                self.message.text = ""
            except Exception as e:
                print e
                # probably make this Popup an own kv and class (reusable everytime something goes wrong?)
                content = GridLayout(cols=1)
                content.add_widget(Label(text="An error occurred.\nPlease try again"))
                butt = Button(background_normal="GUI/Icons/iConfirm.png", size_hint=[None, None])
                anch = AnchorLayout(align_h="center", size_hint=[None, None])
                anch.add_widget(butt)
                content.add_widget(anch)
                popup = Popup(title='Error!', content=content,
                              size_hint=(None, None), size=(400, 400),
                              background="GUI/Icons/white_bg_400x400.png",
                              title_color=(0,0,0,1))
                butt.bind(on_release=popup.dismiss)
                popup.open()
