__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from .EmailItem import EmailItem
from src.Controller.DatabaseController import DatabaseController
from src.Controller.CommunicationController import CommunicationController
from kivy.clock import Clock

Builder.load_file('GUI/overviewLayout.kv')


# The kivy developers themselves are not happy with the list_view. Since we only need about 10 emails at once
# we can just create an own widget adding it x-10 times to the overview
class OverviewLayout(Screen):

    grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(OverviewLayout, self).__init__(**kwargs)
        self.counter = 0
        self.mails = []
        Clock.schedule_once(self.scheduledMailCheck, 0)
        Clock.schedule_interval(self.scheduledMailCheck, 60)

    def scheduledMailCheck(self,_):
        CommunicationController.getEmailsFromServer()
        self.mails = DatabaseController.load_emails()
        self.displayEmails()

    #the kivy properties don't always load properly
    #this method observes the property and trigger on_change
    def on_grid(self, instance, value):
        self.displayEmails()

    def get_emails_from_db(self):
        emails = DatabaseController.load_emails()
        return emails

    def displayEmails(self):
        self.grid.clear_widgets()
        currentMails = self.mails[self.counter*7:(self.counter+1)*7]
        self.add_emails(currentMails)

    # Parameter emails is a list of email objects as defined below
    def add_emails(self, emails):
        for v in emails:
            item = EmailItem(v)
            print v.read
            self.grid.add_widget(item)

    def previous_page(self):
        if self.counter > 0:
            self.counter -= 1
        else:
            self.counter = 0
        self.displayEmails()

    def next_page(self):
        if (self.counter+1 * 10) < len(self.mails):
            self.counter += 1
        self.displayEmails()

    # responsible to switch between folders, will probably never be used
    def switch_to(self, str):
        print("%s pressed" %str)
