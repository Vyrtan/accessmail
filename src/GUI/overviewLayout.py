__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from .EmailItem import EmailItem
from src.Controller.DatabaseController import DatabaseController

Builder.load_file('GUI/overviewLayout.kv')


# The kivy developers themselves are not happy with the list_view. Since we only need about 10 emails at once
# we can just create an own widget adding it x-10 times to the overview
class OverviewLayout(Screen):

    grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(OverviewLayout, self).__init__(**kwargs)
        self.counter = 0
        self.mails = self.get_emails_from_db()

    #the kivy properties don't always load properly
    #this method observes the property and trigger on_change
    def on_grid(self, instance, value):
        self.displayEmails()

    def get_emails_from_db(self):
        emails = DatabaseController.load_emails()
        return emails

    def displayEmails(self):
        self.grid.clear_widgets()
        currentMails = self.mails[self.counter*10:(self.counter+1)*10]
        self.add_emails(currentMails)

    # Parameter emails is a list of email objects as defined below
    def add_emails(self, emails):
        for v in emails:
            item = EmailItem(v)
            self.grid.add_widget(item)

    def previous_page(self):
        if self.counter > 0:
            self.counter -= 1
        else:
            self.counter = 0
        self.displayEmails()

    def next_page(self):
        self.counter += 1
        self.displayEmails()

    # responsible to switch between folders, will probably never be used
    def switch_to(self, str):
        print("%s pressed" %str)
