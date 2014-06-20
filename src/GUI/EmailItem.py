__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty


Builder.load_file("GUI/EmailItem.kv")


class EmailItem(BoxLayout):
    name = StringProperty()
    email = StringProperty()
    subject = StringProperty()
    root = ObjectProperty()

    def __init__(self, name="Unknown", email="Unknown", subject="Unknown", **kwargs):
        super(EmailItem, self).__init__(**kwargs)
        self.name = name
        self.email = email
        self.subject = subject

    # delete email with corresponding id from model
    def trigger_delete(self):
        print("Delete pressed")

    # call this function with some email id to switch to the corresponding email from the model
    def trigger_read(self, email_id="None"):
        # best. expression. ever.
        self.root.parent.parent.parent.parent.parent.parent.show_layout("Read", email_id=email_id)
        print("Read pressed")

    # get address and subject, create new email
    def trigger_reply(self):
        address = self.email
        subject = self.subject
        self.root.parent.parent.parent.parent.parent.parent.show_layout("Write", address=address, subject=subject)