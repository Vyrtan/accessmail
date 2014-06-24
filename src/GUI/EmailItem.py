__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from src.database import Database
from src.Controller.CommunicationController import CommunicationController
import string


Builder.load_file("GUI/EmailItem.kv")
Builder.load_file("GUI/deletePopup.kv")


class EmailItem(BoxLayout):
    name = StringProperty()
    email = StringProperty()
    subject = StringProperty()
    root = ObjectProperty()
    oMail = ObjectProperty()

    def __init__(self, email, **kwargs):
        super(EmailItem, self).__init__(**kwargs)
        self.oMail = email
        # TODO: get Name from Contactbook
        self.name = string.split(email._from, "@")[0]
        self.email = email._from
        if email.subject:
            self.subject = email.subject if len(email.subject) <= 20 else email.subject[:20] + "..."
        else:
            self.subject = "None"

    # delete email with corresponding id from model
    def trigger_delete(self):
        p = DeletePopup(self.oMail)
        p.open()

    # call this function with some email id to switch to the corresponding email from the model
    def trigger_read(self):
        # best. expression. ever.
        self.root.parent.parent.parent.parent.parent.parent.show_layout("Read", email=self.oMail)

    # get address and subject, create new email
    def trigger_reply(self):
        address = self.email
        subject = self.subject
        self.root.parent.parent.parent.parent.parent.parent.show_layout("Write", address=address, subject=subject)


class DeletePopup(Popup):

    def __init__(self, mail):
        super(DeletePopup, self).__init__()
        self.em = mail

    def deleteMail(self):
        db = Database()
        db.deleteMail(self.em)
        CommunicationController.deleteMail(self.em)