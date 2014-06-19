__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

import CustomListViewItem
import time

Builder.load_file('GUI/overviewLayout.kv')

# The kivy developers themselves are not happy with the list_view. Since we only need about 10 emails at once
# we can just create an own widget adding it x-10 times to the overview
class OverviewLayout(Screen):

    grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(OverviewLayout, self).__init__(**kwargs)
        if self.grid:
            self.test_data()

    def on_grid(self, instance, value):
        print("Callback called")
        self.test_data()

    def add_email(self, sender):
        print("add_email called")
        print(self.grid)
        item1 = CustomListViewItem.CustomListViewItem(sender)
        self.grid.add_widget(item1)

    def test_data(self):
        print("test_data called")
        self.add_email("testsender")
