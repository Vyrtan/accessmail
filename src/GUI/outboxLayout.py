__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from .EmailItem import EmailItem
from src.database import Database
from src.Controller.DatabaseController import DatabaseController
from src.Controller.CommunicationController import CommunicationController
from kivy.clock import Clock

Builder.load_file('GUI/outboxLayout.kv')


class OutboxLayout(Screen):
    '''
    You can compare this documentation to the documentation for the inboxLayout class.
    They are almost completely similar, but this one only gets Sent emails from the database
    and displays them.
    '''

    grid = ObjectProperty()
    pageCount = StringProperty()
    emailsPerPage = 5

    def __init__(self, **kwargs):
        super(OutboxLayout, self).__init__(**kwargs)
        self.counter = 0
        self.mails = []
        self.nRead = 0
        Clock.schedule_once(self.scheduledMailCheck, 0)
        Clock.schedule_interval(self.scheduledMailCheck, 60)

    def scheduledMailCheck(self, _):
        CommunicationController.getSentFromServer()
        db = Database()
        self.mails = db.getSentMails()
        self.displayEmails()

    #the kivy properties don't always load properly
    #this method observes the property and triggers when it changes
    def on_grid(self, instance, value):
        self.displayEmails()

    def get_emails_from_db(self):
        emails = DatabaseController.load_emails()
        return emails

    def displayEmails(self):
        self.grid.clear_widgets()
        currentMails = self.mails[self.counter*self.emailsPerPage:(self.counter+1)*self.emailsPerPage]
        self.add_emails(currentMails)
        self.setPageCount()

    # Parameter emails is a list of email objects as defined below
    def add_emails(self, emails):
        for v in emails:
            if (emails.index(v) % 2) != 0:
                item = EmailItem(v)
            else:
                item = EmailItem(v, colour=1)
            self.grid.add_widget(item)

    def previous_page(self):
        if self.counter > 0:
            self.counter -= 1
        else:
            self.counter = 0
        self.displayEmails()

    def nextPage(self):
        if ((self.counter+1) * self.emailsPerPage) < (len(self.mails)):
            self.counter += 1
        self.displayEmails()

    def setPageCount(self):
        a = self.emailsPerPage * self.counter + 1
        a1 = a if self.counter >= 1 else self.emailsPerPage * self.counter
        b = self.emailsPerPage * (self.counter + 1)
        c = len(self.mails)
        b1 = b if b < c else c
        self.pageCount = "%d - %d / %d" %(a1,b1,c)

