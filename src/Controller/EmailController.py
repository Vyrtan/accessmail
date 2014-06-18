__author__ = 'grafgustav'
import MainController


class EmailController(object):

    def __init__(self, main_controller):
        self.__emails = self.__load_emails()
        self.__main_controller = main_controller

    def get_emails(self):
        return self.__emails

    def __load_emails(self):
        emails = self.__main_controller.get_database_controller().load_emails()
        return emails

    def _save_email(self, mail):
        self.__main_controller.get_database_controller().save_email(mail)

    def _remove_email(self, mail):
        self.__main_controller.get_database_controller().remove_email(mail) #TODO: Mail auch aus Webadresse löschen?

