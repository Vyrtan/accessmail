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
        if self.grid:
            self.test_data()

    #the kivy properties don't always load properly
    #this method observes the property and trigger on_change
    def on_grid(self, instance, value):
        print("Callback called")
        self.displayEmails()

    def get_emails_from_db(self):
        return DatabaseController.load_emails()

    def displayEmails(self):
        currentMails = self.mails[self.counter*10:(self.counter+1)*10]
        self.add_emails(currentMails)

    # TODO: limit added emails to 8/10 and store rest somewhere else for later use
    # even better: we always only fetch 8/10 emails from the controller and hand over a counter which indicates
    # all_emails[counter*10:(counter+1)*10]
    # Parameter emails is a list of email objects as defined below, maybe adjust getter if different class is used
    def add_emails(self, emails):
        for v in emails:
            print("email added")
            item = EmailItem(name="asdf", email="asdf", subject=v.subject)
            self.grid.add_widget(item)

        # testing routines
        # item1 = EmailItem(name="Max Mustermann", email="max.mustermann@web.de", subject="Your photo")
        # item2 = EmailItem(email="dascha.grib@mail.ru", subject="50 Euro")
        # item3 = EmailItem()
        # self.grid.add_widget(item1)
        # self.grid.add_widget(item2)
        # self.grid.add_widget(item3)

    # def test_data(self):
    #     items = [Email(name="Max Mustermann", email="max.mustermann@web.de", subject="Your photo"),
    #              Email(email="dascha.grib@mail.ru", subject="50 Euro"),
    #              Email()]
    #     self.add_emails(items)

    def previous_page(self):
        if self.counter > 0:
            self.counter -= 1
        else:
            self.counter = 0
        self.displayEmails()

    def next_page(self):
        self.counter += 1
        self.displayEmails()

    # responsible to switch between folders
    def switch_to(self, str):
        print("%s pressed" %str)
