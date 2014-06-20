__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from ContactItem import ContactItem
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

Builder.load_file('GUI/addressLayout.kv')


class AddressLayout(Screen):
    grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(AddressLayout, self).__init__(**kwargs)

    def on_grid(self, instance, value):
        self.test_data()

    def get_buttons(self):
        for child in self.children:
            print(child)

    # see comments above add_emails in overviewLayout.py
    def add_contacts(self, contacts):
        # counter = 0
        for v in contacts:
            print("Contact added")
            item = ContactItem(name=v.get_name(), email=v.get_email())
            self.grid.add_widget(item)

    # TODO: delete this method
    def test_data(self):
        items = [Contact(name="Max Mustermann", email="max.mustermann@web.de"),
                 Contact(email="dascha.grib@mail.ru"),
                 Contact()]
        self.add_contacts(items)

    def previous_page(self):
        print("previous page pressed")

    def next_page(self):
        print("next page pressed")


class Contact(object):

    def __init__(self, name="Unknown", email="Unknown"):
        self.name = name
        self.email = email

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email
