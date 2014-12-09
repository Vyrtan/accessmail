__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from Tooltip import ToolTip


Builder.load_file('GUI/menuLayout.kv')


class MenuLayout(Screen):

    def __init__(self, **kwargs):
        super(MenuLayout, self).__init__(**kwargs)