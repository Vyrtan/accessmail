__author__ = 'grafgustav'
import CommunicationController
import ContactsController
import DatabaseController
import EmailController


class MainController(object):

    def __init__(self):
        self.__email_controller = EmailController(self)
        self.__contacts_controller = ContactsController(self)
        self.__database_controller = DatabaseController(self)
        self.__communication_controller = CommunicationController(self)

    def get_mail_controller(self):
        return self.__email_controller

    def get_contacts_controller(self):
        return self.__contacts_controller

    def get_database_controller(self):
        return self.__database_controller

    def get_communication_controller(self):
        return self.__communication_controller
