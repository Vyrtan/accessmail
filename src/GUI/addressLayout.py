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
        '''
        This method is an observer for the attribute self.grid.
        Since kivy is a young framework it can occur that the object grid is not properly set during the
        __init__ cycle. This method observes the object and triggers, if something changes. Usually the change
        is the correct instance of the spoken to GridLayout.

        :param instance:
        :param value:
        :return:
        '''

        # this only indicates the object is loaded properly
        # better set observer to datamodel as well
        self.getContactsFromDB()

    def displayContacts(self):
        '''
        This method calculates how many contacts shall be added to the GridLayout, calculates the
        page indicator and calls the actual adding of the contact objects.

        :return:
        '''
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
        '''
        This method adds the contacts given by the parameter "contacts" to the GridLayout.

        :param contacts: The contacts to be added to the Overview.
        :type [Contacts]: List of contacts
        :return:
        '''
        # counter = 0
        for v in contacts:
            if (contacts.index(v) % 2) != 0:
                item = ContactItem(v)
            else:
                item = ContactItem(v, colour=1)
            self.grid.add_widget(item)

    def getContactsFromDB(self):
        '''
        This method gets all contacts from the database, stores them in the object-attribute "contacts"
        and calls the method to display all contacts stored in the attribute.

        :return:
        '''
        contacts = self.db.getContacts()
        self.contacts = contacts
        self.displayContacts()

    def addNewContact(self):
        '''
        This method is called when the user clicks the "Add contact" button in the bottom center.
        It opens up the necessary popup to fill in name and e-mail address of the new contact.

        :return:
        '''
        p = AddContactPopup(self.db, self)
        p.open()

    def deleteContact(self, contact):
        '''
        This method can be called from the contact item object of a certain contact object. The respective
        contact gets deleted from the database and the view is updated to the new data.

        :param contact:
        :return:
        '''
        self.db.deleteContact(contact)
        self.contacts.remove(contact)
        self.grid.clear_widgets()
        self.getContactsFromDB()

    def previousPage(self):
        '''
        This method is used to switch through the pages of contacts.
        It turns one step backwards.

        :return:
        '''
        if self.counter > 0:
            self.counter -= 1
        else:
            self.counter = 0
        self.getContactsFromDB()

    def nextPage(self):
        '''
        This method is used to switch through the pages of contacts.
        It turns one step forward.

        :return:
        '''
        if ((self.counter+1) * self.contsPerPage) < len(self.contacts):
            self.counter += 1
        self.getContactsFromDB()


class AddContactPopup(Popup):
    """
    This class is the controller for the AddContactPopup-view. It adds the filled in contact data
    to the database and refreshes the view of the contacts overview.

    :param db: The database object which holds the session used in the addressbook as well
    :param par: The addressbook itself. Like this the refresh can easily be triggered.
    :param kwargs: Not really used, but it is good style I think.
    """
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
