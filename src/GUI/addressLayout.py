__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
#from kivy.properties import ListProperty

Builder.load_file('addressLayout.kv')


class AddressLayout(Screen):

    def __init__(self, **kwargs):
        super(AddressLayout, self).__init__(**kwargs)
        print("Address constructor called")
        #buttons = ListProperty()

    def get_buttons(self):
        for child in self.children:
            print(child)