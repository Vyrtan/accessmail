__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


Builder.load_file('GUI/readlayout.kv')


class ReadLayout(Screen):

    email = ObjectProperty()
    textOutput = ObjectProperty()
    subject = ObjectProperty()

    def __init__(self, **kwargs):
        super(ReadLayout, self).__init__(**kwargs)

    def on_email(self, instance, value):
        self.displayEmail()

    def displayEmail(self):
        self.textOutput.text = self.email.message
        self.subject.text = self.email.subject

    def nextEmail(self):
        print "next email"

    def previousEmail(self):
        print "previous Email"

    def reply(self):
        print self.parent.parent.parent.show_layout("Write", subject=self.email.subject, address=self.email._from)