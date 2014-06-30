__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from src.GUI.ContactItem import ContactItem
from kivy.properties import ObjectProperty, StringProperty
from src.database import Database
from kivy.uix.popup import Popup
from src.models import Contacts

Builder.load_file('GUI/addressLayout.kv')
Builder.load_file('GUI/addContactPopup.kv')


class AddressLayout(Screen):
    grid = ObjectProperty()
    pageCount = StringProperty()

    def __init__(self, **kwargs):
        super(AddressLayout, self).__init__(**kwargs)
        self.contsPerPage = 5
        self.contacts = []
        self.counter = 0
        self.db = Database()

    def on_grid(self, instance, value):
        # this only indicates the object is loaded properly
        # better set observer to datamodel as well
        self.onChange()

    def onChange(self):
        self.getContactsFromDB()

    def displayContacts(self):
        self.grid.clear_widgets()
        self.addContacts(self.contacts[self.counter*self.contsPerPage:(self.counter+1)*self.contsPerPage])
        a = self.counter * self.contsPerPage
        a1 = a if self.counter == 0 else self.counter * self.contsPerPage + 1
        b = (self.counter + 1) * self.contsPerPage
        b1 = b if b < len(self.contacts) else len(self.contacts)
        c = len(self.contacts)
        self.pageCount = "%d - %d/%d" %(a1, b1, c)

    # see comments above add_emails in InboxLayout.py
    def addContacts(self, contacts):
        # counter = 0
        for v in contacts:
            if (contacts.index(v) % 2) != 0:
                item = ContactItem(v)
            else:
                item = ContactItem(v, colour=1)
            self.grid.add_widget(item)

    def getContactsFromDB(self):
        contacts = self.db.getContacts()
        self.contacts = contacts
        self.displayContacts()

    def addNewContact(self):
        p = AddContactPopup(self.db, self)
        p.open()

    def deleteContact(self, contact):
        self.db.deleteContact(contact)
        self.contacts.remove(contact)
        self.grid.clear_widgets()
        self.getContactsFromDB()

    def previousPage(self):
        if self.counter > 0:
            self.counter -= 1
        else:
            self.counter = 0
        self.getContactsFromDB()

    def nextPage(self):
        if ((self.counter+1) * self.contsPerPage) < len(self.contacts):
            self.counter += 1
        self.getContactsFromDB()


class AddContactPopup(Popup):
    name = ObjectProperty()
    address = ObjectProperty()

    def __init__(self, db, par, **kwargs):
        super(AddContactPopup, self).__init__(**kwargs)
        self.par = par
        self.db = db

    def addContact(self):
        newContact = Contacts
        newContact.emailAddress = self.address.text
        newContact.name = self.name.text
        self.db.insertContact(newContact)
        self.par.getContactsFromDB()
        self.dismiss()
