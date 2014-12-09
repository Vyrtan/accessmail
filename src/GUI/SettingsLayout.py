__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from src.database import Database

Builder.load_file('GUI/SettingsLayout.kv')


class SettingsLayout(Screen):

    def __init__(self, **kwargs):
        super(SettingsLayout, self).__init__(**kwargs)

    def save_settings(self):
        # save the changes made
        print "Save changes"

    def reset_settings(self):
        # set everything to the database state
        print "Reset settings"

    def reset_program(self):
        # reset the entire database
        print "Reset database"

# What kind of Settings should be adjustable?
# 1. Reset Account
# 2. Adjust colours
# 3. Adjust text size
# 4. Adjust numbers of contacts and emails displayed per page
