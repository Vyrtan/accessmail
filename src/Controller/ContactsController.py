__author__ = 'grafgustav'
import MainController


class EmailController(object):

    def __init__(self, main_controller):
        self.__contacts = self.__load_contacts()
        self.__main_controller = main_controller

    def get_contacts(self):
        return self.__contacts

    def __load_contacts(self):
        contacts = self.__main_controller.get_database_controller().load_contacts()
        return contacts

    def _edit_contact(self,contact):
        self.__main_controller.get_database_controller().edit_contacts(contact)

    def _save_contact(self,contact):
        self.__main_controller.get_database_controller().save_contact(contact)

    def _remove_contact(self,contact):
        self._main_controller.get_database_controller().remove_contact(contact)

