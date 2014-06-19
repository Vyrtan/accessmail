__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import StringProperty


Builder.load_file("GUI/CustomListViewItem.kv")


class CustomListViewItem(BoxLayout):
    text = StringProperty()
    #subject = StringProperty()

    def __init__(self, text, **kwargs):
        super(CustomListViewItem, self).__init__(**kwargs)
        self.text = text
        #self.subject = subject

    def trigger_delete(self):
        print("Delete pressed")

    def trigger_read(self):
        print("Read pressed")

    def trigger_reply(self):
        print("Reply pressed")