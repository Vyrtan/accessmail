__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from src.GUI.ContactItem import ContactItem
from kivy.properties import ObjectProperty, StringProperty
from src.Controller import DatabaseController
from kivy.uix.popup import Popup

Builder.load_file('GUI/addressLayout.kv')
Builder.load_file('GUI/addContactPopup.kv')


class AddressLayout(Screen):
    grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(AddressLayout, self).__init__(**kwargs)
        self.contacts = []

    def on_grid(self, instance, value):
        self.getContactsFromDB()
        self.addContacts(self.contacts)

    def get_buttons(self):
        for child in self.children:
            print(child)

    # see comments above add_emails in overviewLayout.py
    def addContacts(self, contacts):
        # counter = 0
        for v in contacts:
            print("Contact added")
            item = ContactItem(name=v.name, email=v.emailAddress)
            self.grid.add_widget(item)

    def getContactsFromDB(self):
        contacts = DatabaseController.DatabaseController.loadContacts()
        self.contacts = contacts

    def addNewContact(self):
        p = AddContactPopup()
        p.open()


    def addContactToDB(self, name, address):
        DatabaseController.DatabaseController.addContact(name, address)

    def previous_page(self):
        print("previous page pressed")

    def next_page(self):
        print("next page pressed")

    def printStuff(self):
        print "Stuff"


class AddContactPopup(Popup):
    name = StringProperty()
    address = StringProperty()

    def handOverInfo(self, pname, paddress):
        self.name = pname
        self.address = paddress
        print("Name: %s, Address: %s" %(self.name, self.address))
        DatabaseController.DatabaseController.addContact(self.name, self.address)
        self.dismiss()


