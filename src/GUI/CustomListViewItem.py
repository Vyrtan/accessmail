__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import StringProperty


Builder.load_file("CustomListViewItem.kv")


class CustomListViewItem(BoxLayout, ListItemButton):
    name = StringProperty()
    email = StringProperty()
    subject = StringProperty()

    def __init__(self, **kwargs):
        super(CustomListViewItem).__init__(kwargs)
        self.name = "Test1"
        self.email = "Test2"
        self.subject = "Test3"

    def trigger_delete(self):
        #fill with behaviour
        pass

    def trigger_read(self):
        #fill with behaviour
        pass

    def trigger_reply(self):
        #fill with behaviour
        pass