__author__ = 'grafgustav'
import sqlite3


class DatabaseController(object):

    def __init__(self, main_controller):
        self.__main_controller = main_controller

    #TODO: Emails und Kontakte in der DB speichern

    def load_emails(self):
        conn = sqlite3.connect("../../data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM mail;")
        emails = c.fetchall()
        conn.commit()
        conn.close()
        return emails

    def load_contacts(self):
        conn = sqlite3.connect("../../data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM contact;")
        contacts = c.fetchall()
        conn.commit()
        conn.close()
        return contacts

    def edit_contacts(self, cont):
        conn = sqlite3.connect("../../data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM contact;")
        context = c.fetchone(cont) #Todo: richtigen Context fetchen. Edit fenster oder direkte übergabe der zu edit. Daten?

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