__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from time import strptime
from src.database import Database
from src.Controller.DatabaseController import DatabaseController
from src.models import Mails


Builder.load_file('GUI/readlayout.kv')


class ReadLayout(Screen):

    """
    This class is the corresponding controller level for the ReadLayout View. It manages the displayed email
    and offers functions to switch to other emails or reply to the currently disyplayed one.

    :param kwargs:
    """
    email = ObjectProperty()
    textOutput = ObjectProperty()
    subject = ObjectProperty()

    def __init__(self, **kwargs):
        super(ReadLayout, self).__init__(**kwargs)
        self.email = None

    def on_email(self, instance, value):
        '''
        This method observers the attribute email and is fired on changes. The then assigned
        e-mail object gets marked as Read in the database and displayed.
        :param instance:
        :param value:
        :return:
        '''
        if not self.email:
            return
        db = Database()
        db.markMailAsRead(self.email)
        self.displayEmail()

    def displayEmail(self):
        '''
        This method is used to display the currently active e-mail (which is held by the email attribute).
        The sender, subject and text are displayed.
        Unfortunately the encoding of the e-mail is somewhat defective. This will be soon patched.
        :return:
        '''
        self.textOutput.text = self.email.message
        self.subject.text = self.email.subject
        self.sender.text = self.email._from

    # maybe we should have a separate datamodel where all the emails are loaded? Which criteria defines
    # which email is next in the list? -> We already have all emails loaded in the overview layout
    def nextEmail(self):
        '''
        This method is used to access the next e-mail in the model. There is no proper order yet,
        but a chronological order is being pursued in future patches.s

        :return:
        '''
        # example for time
        # Sun, 22 Jun 2014 23:13:07 +0000
        # oldD = strptime(self.email.date, "%a, %d %b %Y %H:%M:%S +0000")
        if not self.email:
            return
        allMails = DatabaseController.load_emails()
        currMail = self.email
        for m in allMails:
            if m.id == currMail.id:
                index = allMails.index(m)
        print currMail
        nextMail = allMails[index+1] if index < (len(allMails)-1) else allMails[0]
        print nextMail
        self.email = nextMail

    def previousEmail(self):
        '''
        This method is used to access the previous e-mail in the model. There is no proper order yet,
        but a chronological order is being pursued in future patches.s

        :return:
        '''
        if not self.email:
            return
        allMails = DatabaseController.load_emails()
        currMail = self.email
        for m in allMails:
            if m.id == currMail.id:
                index = allMails.index(m)
        print currMail
        nextMail = allMails[index-1] if index > 0 else allMails[(len(allMails) -1)]
        print nextMail
        self.email = nextMail

    def trigger_reply(self):
        '''
        This method is called when the reply button is pressed. It calls the screenmanager
        and provides the e-mail object and it's parameters to the WriteLayout.

        :return:
        '''
        message = self.formatReplyMessage()
        self.parent.parent.parent.show_layout("Write", subject=self.email.subject, address=self.email._from, message=message)

    def formatReplyMessage(self):
        '''
        This method formats the message string of the currently displayed e-mail to a Reply-format string.

        :return: string: The formatted message.
        '''
        replyString = self.email.message.split("\n")
        replyHeader = "\n>" + self.email._from + " wrote on " + self.email.date + ":\n>"
        return replyHeader +'\n>'.join(replyString)