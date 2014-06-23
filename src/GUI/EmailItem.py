__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from src.Controller import DatabaseController


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
        self.name = email._from
        self.email = email._from
        if email.subject:
            self.subject = email.subject
        else:
            self.subject = "None"

    # delete email with corresponding id from model
    def trigger_delete(self):
        self.deleteMail()

        # alternative version using a popup and confirmation
        # p = DeletePopup()
        # p.open()

    def deleteMail(self):
        DatabaseController.DatabaseController.deleteEmail(self.oMail)


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
    pass