__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


Builder.load_file("GUI/EmailItem.kv")


class EmailItem(BoxLayout):
    name = StringProperty()
    email = StringProperty()
    subject = StringProperty()

    def __init__(self, name="Unknown", email="Unknown", subject="Unknown", **kwargs):
        super(EmailItem, self).__init__(**kwargs)
        self.name = name
        self.email = email
        self.subject = subject

    def trigger_delete(self):
        print("Delete pressed")

    def trigger_read(self):
        print("Read pressed")

    def trigger_reply(self):
        print("Reply pressed")