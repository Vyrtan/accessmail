__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty


Builder.load_file("GUI/ContactItem.kv")


class ContactItem(BoxLayout):
    name = StringProperty()
    email = StringProperty()
    subject = StringProperty()
    root = ObjectProperty()

    def __init__(self, name="Unknown", email="Unknown", **kwargs):
        super(ContactItem, self).__init__(**kwargs)
        self.name = name
        self.email = email

    def trigger_delete(self):
        print("Delete pressed")

    def trigger_write_mail(self):
        print("Write mail pressed")