__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import StringProperty


Builder.load_file("CustomListViewItem.kv")


class CustomListViewItem(BoxLayout):
    sender = StringProperty()
    subject = StringProperty()

    def __init__(self, **kwargs):
        super(CustomListViewItem, self).__init__(**kwargs)
        self.sender = kwargs["sender"]
        self.subject = kwargs["subject"]

    def trigger_delete(self):
        print "Delete pressed"

    def trigger_read(self):
        print "Read pressed"

    def trigger_reply(self):
        print "Reply pressed"