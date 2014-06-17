__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import CustomListViewItem


Builder.load_file('overviewLayout.kv')


class OverviewLayout(Screen):
    list_view = ObjectProperty()
    label = ObjectProperty()

    def __init__(self):
        super(OverviewLayout, self).__init__()
        self.list_view.adapter.data = [1, 2, 3, 4]
