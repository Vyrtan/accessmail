__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


Builder.load_file('GUI/readlayout.kv')


class ReadLayout(Screen):

    email = ObjectProperty()
    textOutput = ObjectProperty()

    def __init__(self, **kwargs):
        super(ReadLayout, self).__init__(**kwargs)

    def on_email(self, instance, value):
        self.displayEmail()
        print "email object changed"

    def displayEmail(self):
        print self.textOutput.text
        print self.email.message
        self.textOutput.text = self.email.message[:5000]
        print "email gets displayed"

    def nextEmail(self):
        print "next email"

    def previousEmail(self):
        print "previous Email"


