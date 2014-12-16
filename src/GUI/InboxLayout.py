__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from .EmailItem import EmailItem
from src.database import Database
from src.Controller.CommunicationController import CommunicationController
from kivy.clock import Clock
from widgetHelpers.WidgetManager import WidgetManager

Builder.load_file('GUI/inboxLayout.kv')


# The kivy developers themselves are not happy with the list_view. Since we only need about 10 emails at once
# we can just create an own widget adding it x-10 times to the overview
class InboxLayout(Screen):

    """
    This class is the corresponding controller for the Inbox View.
    It manages the synchronisation with the server and the database.

    :param kwargs:
    """
    grid = ObjectProperty()
    pageCount = StringProperty()
    all_emails = StringProperty()

    def __init__(self, **kwargs):
        super(InboxLayout, self).__init__(**kwargs)
        self.counter = 0
        self.mails = []
        self.nRead = 0
        self.db = Database()
        self.emailsPerPage = self.db.get_settings("nbr_mails")
        self.all_emails = "Show only not read e-mails"
        Clock.schedule_once(self.scheduled_mail_check, 0)
        Clock.schedule_interval(self.scheduled_mail_check, 60)

    def scheduled_mail_check(self, _):
        '''
        This method is called every 60 seconds to get new emails from the server and synchronize the view
        with the database.

        :param _: I have no idea what is going on here. Somehow I needed it, somehow I didn't.
        :return:
        '''
        CommunicationController.getEmailsFromServer()
        db = Database()
        if self.nRead:
            self.mails = db.get_not_read_mails()
        else:
            self.mails = db.get_all_mails()
        self.display_emails()

    #the kivy properties don't always load properly
    #this method observes the property and triggers when it changes
    def on_grid(self, instance, value):
        '''
        This method is used to compensate the slowness of the framework. It is called when the grid attribute
        changes.

        :param instance: not used, but gets passed
        :param value: not used, but gets passed
        :return:
        '''
        self.display_emails()

    def get_emails_from_db(self):
        '''
        This method loads the emails from the database and returns them.
        A correct way of sorting the emails will come in the future.

        :return: emails: All e-mails found in the database.
        :rtype: [Emails]: List of Emails
        '''
        emails = self.db.get_all_mails()
        return emails

    def display_emails(self):
        '''
        This method calculates the number of e-mails to be displayed, calls the add_emails method using
        that calculation and passes the right e-mails which ought to be displayed.
        Also the labeling for the page number is called.

        :return:
        '''
        self.grid.clear_widgets()
        currentMails = self.mails[self.counter*self.emailsPerPage:(self.counter+1)*self.emailsPerPage]
        self.add_emails(currentMails)
        self.set_page_count()
        WidgetManager.Instance().build_tree("a")

    # Parameter emails is a list of email objects as defined below
    def add_emails(self, emails):
        '''
        This method takes a list of emails and displays them in the Inbox View.

        :param emails: The emails to be displayed.
        :type [Emails]: A list of Emails
        :return:
        '''
        for v in emails:
            if (emails.index(v) % 2) != 0:
                item = EmailItem(v, self)
            else:
                item = EmailItem(v, self, colour=1)
            self.grid.add_widget(item)

    def previous_page(self):
        '''
        This method is used to switch through the available pages.
        It turns the counter one step backwards and refreshes the View.

        :return:
        '''
        if self.counter > 0:
            self.counter -= 1
        else:
            self.counter = 0
        self.display_emails()

    def next_page(self):
        '''
        This method is used to switch through the available pages.
        It turns the counter one step forward and refreshes the View.

        :return:
        '''
        if ((self.counter+1) * self.emailsPerPage) < (len(self.mails)):
            self.counter += 1
        self.display_emails()

    def set_page_count(self):
        '''
        This method is used to calculate how many e-mails are being display and how many are available.

        :return:
        '''
        a = self.emailsPerPage * self.counter + 1
        a1 = a if self.counter >= 1 else self.emailsPerPage * self.counter
        b = self.emailsPerPage * (self.counter + 1)
        c = len(self.mails)
        b1 = b if b < c else c
        self.pageCount = "%d - %d / %d" %(a1,b1,c)

    def toggle_selection(self):
        '''
        This methos is used to toggle between All and only Not-Read e-mails.

        :return:
        '''
        if self.nRead == 1:
            self.all_emails = "Show only not read e-mails"
            self.nRead = 0
        else:
            self.nRead = 1
            self.all_emails = "Show all e-mails"
        print self.all_emails
        self.scheduled_mail_check("lolno")
