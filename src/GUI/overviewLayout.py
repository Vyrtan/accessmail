__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListView
from kivy.clock import Clock
import CustomListViewItem
import time

Builder.load_file("overviewLayout.kv")


# The kivy developers themselves are not happy with the list_view. Since we only need about 10 emails at once
# we can just create an own widget adding it x-10 times to the overview
class OverviewLayout(Screen):
    grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(OverviewLayout, self).__init__(**kwargs)
        if self.grid:
            self.test_data()
        #self.bind(grid=self.callback)

    def on_grid(self, instance, value):
        print "Callback called"
        self.test_data()

    def add_email(self, sender, subject):
        print "add_email called"
        print self.grid
        self.grid.add_widget(CustomListViewItem(sender=sender, subject=subject))

    def test_data(self):
        print "test_data called"
        self.add_email("testsender", "testsubject")
