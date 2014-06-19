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

Builder.load_file('overviewLayout.kv')


class OverviewLayout(Screen):
    list_view = ObjectProperty()
    label = ObjectProperty()
    text = StringProperty()
    grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(OverviewLayout, self).__init__(**kwargs)
        if self.list_view:
            self.list_view.adapter.data = ["test1", "test2"]
        #self.add_listview()
        print("Listview initialized")

    #called when the list_view property changes
    #unfortunately the updated view does not get rendered
    def on_list_view(self, instance, value):
        print("value changed")
        self.list_view.adapter.data = ["asdf"]

    # def add_listview(self):
    #     print "add_listview called"
    #
    #     sample = {"sample1": {"name": "Rudolph", "address": "rudolph@rentier.np", "subject": "empty"}}
    #
    #     list_item_args_converter = \
    #             lambda row_index, rec: {'text': rec['name'],
    #                                     'size_hint_y': None,
    #                                     'height': 25}
    #
    #     my_dict_adapter = \
    #             DictAdapter(
    #                 sorted_keys=sorted(sample.keys()),
    #                 data=sample,
    #                 args_converter=list_item_args_converter,
    #                 selection_mode='single',
    #                 allow_empty_selection=True,
    #                 cls=CustomListViewItem)
    #
    #     fruits_list_view = ListView(adapter=my_dict_adapter,
    #                                 size_hint=(.2, 1.0))
    #
    #     self.add_widget(fruits_list_view)

