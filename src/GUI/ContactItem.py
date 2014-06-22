__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from src.Controller.DatabaseController import DatabaseController


Builder.load_file("GUI/ContactItem.kv")


class ContactItem(BoxLayout):
    name = StringProperty()
    email = StringProperty()
    subject = StringProperty()
    root = ObjectProperty()

    def __init__(self, contact=None, **kwargs):
        super(ContactItem, self).__init__(**kwargs)
        self.contact = contact
        self.name = contact.name
        self.email = contact.emailAddress

    def trigger_delete(self):
       print self.root.parent.parent.parent.deleteContact(self.contact)

    # switches to WriteLayout and already fills in the address (supposedly)
    def trigger_write_mail(self):
        self.root.parent.parent.parent.parent.parent.parent.show_layout("Write", address=self.email)