__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from time import strptime
from src.Controller.DatabaseController import DatabaseController
from src.models import Mails


Builder.load_file('GUI/readlayout.kv')


class ReadLayout(Screen):

    email = ObjectProperty()
    textOutput = ObjectProperty()
    subject = ObjectProperty()

    def __init__(self, **kwargs):
        super(ReadLayout, self).__init__(**kwargs)
        self.email = None

    def on_email(self, instance, value):
        if not self.email:
            return
        self.displayEmail()


    def displayEmail(self):
        self.textOutput.text = self.email.message
        self.subject.text = self.email.subject

    # maybe we should have a separate datamodel where all the emails are loaded? Which criteria defines
    # which email is next in the list? -> We already have all emails loaded in the overview layout
    def nextEmail(self):
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
        address = self.email
        subject = self.subject
        message = self.formatReplyMessage()
        self.parent.parent.parent.show_layout("Write", subject=self.email.subject, address=self.email._from, message=message)

    def formatReplyMessage(self):
        replyString = self.email.message.split("\n")
        replyHeader = "\n>" + self.email._from + " wrote on " + self.email.date + ":\n>"
        return replyHeader +'\n>'.join(replyString)