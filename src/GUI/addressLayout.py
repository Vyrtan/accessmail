__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from src.GUI.ContactItem import ContactItem
from kivy.properties import ObjectProperty, StringProperty
from src.Controller.DatabaseController import DatabaseController
from kivy.uix.popup import Popup
from src.models import Contacts

Builder.load_file('GUI/addressLayout.kv')
Builder.load_file('GUI/addContactPopup.kv')


class AddressLayout(Screen):
    grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(AddressLayout, self).__init__(**kwargs)
        self.contacts = []
        self.counter = 0

    def on_grid(self, instance, value):
        # this only indicates the object is loaded properly
        # better set observer to datamodel as well
        self.onChange()

    def onChange(self):
        self.getContactsFromDB()
        self.displayContacts()

    def get_buttons(self):
        for child in self.children:
            print(child)

    def displayContacts(self):
        print self.counter
        self.grid.clear_widgets()
        self.addContacts(self.contacts[self.counter*10:(self.counter+1)*10])

    # see comments above add_emails in overviewLayout.py
    def addContacts(self, contacts):
        # counter = 0
        for v in contacts:
            print("Contact added")
            item = ContactItem(v)
            self.grid.add_widget(item)

    def getContactsFromDB(self):
        contacts = DatabaseController.loadContacts()
        self.contacts = contacts

    def addNewContact(self):
        p = AddContactPopup()
        p.open()
        p.bind(on_dismiss=self.processNewContact)
        # this thread continues even with the popup open

    def processNewContact(self, p):
        contact = Contacts()
        contact.emailAddress = p.address
        contact.name = p.name
        DatabaseController.addContact(contact)
        self.contacts.append(contact)

        self.displayContacts()

    def deleteContact(self, contact):
        DatabaseController.deleteContact(contact)
        self.contacts.remove(contact)
        self.grid.clear_widgets()
        self.displayContacts()

    def previousPage(self):
        if self.counter > 0:
            self.counter -= 1
        else:
            self.counter = 0
        self.displayContacts()

    def nextPage(self):
        self.counter += 1
        self.displayContacts()

    def printStuff(self):
        print "Stuff"


class AddContactPopup(Popup):
    name = StringProperty()
    address = StringProperty()

    def handOverInfo(self, pname, paddress):
        self.name = pname
        self.address = paddress
        self.dismiss()


