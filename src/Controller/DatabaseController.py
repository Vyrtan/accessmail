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
        mails = db.getAllMails()
        return mails

    @staticmethod
    def deleteEmail(email):
        db = Database()
        db.deleteMail(email)

    @staticmethod
    def loadContacts():
        db = Database()
        contacts = db.getContacts()
        return contacts

    @staticmethod
    def addContact(contact):
        db = Database()
        db.insertContact(contact)

    @staticmethod
    def deleteContact(contact):
        db = Database()
        db.deleteContact(contact)

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