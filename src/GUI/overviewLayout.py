__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListItemButton
import CustomListViewItem


Builder.load_file('overviewLayout.kv')


class OverviewLayout(Screen):
    list_view = ObjectProperty()
    label = ObjectProperty()
    text = StringProperty()

    def __init__(self, **kwargs):
        super(OverviewLayout, self).__init__(kwargs)
        list_item_args_converter = \
                    lambda row_index, rec: {"name": rec["name"],
                                            "address": rec["address"],
                                            "subject": rec["subject"]}

        sample = {"ob1":{"name": "Franz Bauer",
                         "address": "franz.bauer@mail.ru",
                         "subject": "empty"}}

        my_adapter = DictAdapter(sorted_keys=sorted(sample.keys()),
                                 data=sample,
                                 args_converter=list_item_args_converter,
                                 selection_mode="single",
                                 allow_empty_selection=True,
                                 cls=ListItemButton)

        self.list_view.adapter = my_adapter
        print "Listview initialized"
