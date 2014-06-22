__author__ = 'grafgustav'
import sqlite3
from src.database import Database
from src.models import *


class DatabaseController(object):

    def __init__(self, main_controller=None):
        self.__main_controller = main_controller

    #TODO: Emails und Kontakte in der DB speichern

    @staticmethod
    def load_emails():
        db = Database()
        #get all mails sent to active account
        inbox = db.getInbox()
        mails = db.getAllMailsBy("to", "maxi")
        return mails

    @staticmethod
    def loadContacts():
        db = Database()
        contacts = db.getContacts()
        return contacts

    @staticmethod
    def addContact(name, address):
        contact = Contacts()
        contact.name = name
        contact.emailAddress = address
        db = Database()
        db.insertContact(contact)

    def load_credentials(self):
        conn = sqlite3.connect("../../data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM credential;")
        credentials = c.fetchall()
        conn.commit()
        conn.close()
        return credentials

    def load_inbox(self):
        conn = sqlite3.connect("../../data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM inboxes;")
        inb = c.fetchall()
        conn.commit()
        conn.close()
        return inb