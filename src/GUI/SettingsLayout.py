__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from src.database import Database
from kivy.clock import Clock
import sys
import os

Builder.load_file('GUI/SettingsLayout.kv')


class SettingsLayout(Screen):

    txt_colourblind = ObjectProperty()
    txt_nbr_mails = ObjectProperty()
    txt_nbr_addresses = ObjectProperty()
    txt_font_size = ObjectProperty()

    def __init__(self, **kwargs):
        super(SettingsLayout, self).__init__(**kwargs)
        self.db = Database()
        Clock.schedule_once(self.initial_start, 0.5)

    def initial_start(self, _):
        self.txt_colourblind.text = str(self.db.get_settings("colourblind_mode"))
        self.txt_font_size.text = str(self.db.get_settings("font_size"))
        self.txt_nbr_addresses.text = str(self.db.get_settings("nbr_addresses"))
        self.txt_nbr_mails.text = str(self.db.get_settings("nbr_mails"))

    def save_settings(self):
        # save the changes made
        print "Saving changes"
        self.db.edit_settings("colourblind_mode", int(self.txt_colourblind.text))
        self.db.edit_settings("nbr_mails", int(self.txt_nbr_mails.text))
        self.db.edit_settings("nbr_addresses", int(self.txt_nbr_addresses.text))
        self.db.edit_settings("font_size", int(self.txt_font_size.text))
        self.restart_program()

    def discard_changes(self):
        # set everything to the database state
        print "Reset settings"
        self.txt_colourblind.text = str(self.db.get_settings("colourblind_mode"))
        self.txt_font_size.text = str(self.db.get_settings("font_size"))
        self.txt_nbr_addresses.text = str(self.db.get_settings("nbr_addresses"))
        self.txt_nbr_mails.text = str(self.db.get_settings("nbr_mails"))

    def reset_program(self):
        # reset the entire database
        print "Reset database"
        self.db.edit_settings("font_size", 10)
        self.restart_program()

    @staticmethod
    def restart_program():
        # any cleanup has to be done before calling this method
        # it does not return
        python = sys.executable
        os.execl(python, python, * sys.argv)


# What kind of Settings should be adjustable?
# 1. Reset Account
# 2. Adjust colours
# 3. Adjust text size
# 4. Adjust numbers of contacts and emails displayed per page
