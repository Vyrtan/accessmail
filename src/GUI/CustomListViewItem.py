__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton


Builder.load_file("CustomListViewItem.kv")


class CustomListViewItem(BoxLayout, ListItemButton):
    pass