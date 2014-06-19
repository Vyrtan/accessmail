__author__ = 'phillip'

from abc import ABCMeta, abstractmethod

class MailReceiver:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def connect(self, config):
        pass

    @abstractmethod
    def can_create_folder(self):
        """True if this mail access protocol supports the creation of folders on the server
        """
        pass

    @abstractmethod
    def change_folder(self,path):
        """Returns True if the change to the folder path was successfully. If path starts with a / it is a absolut path
        """
        pass

    @abstractmethod
    def create_folder(self, name):
        """Creates a folder in the current directory. can_create_folder must be true. Returns True on success.
        """
        pass

    @abstractmethod
    def delete_folder(self, name):
        """ Deletes the folder name
        """
        pass

    @abstractmethod
    def list_folders(self):
        """Returns the names of all subfolders
        """
        pass

    @abstractmethod
    def get_number_of_mails(self):
        """Returns the number of mails in this folder
        """
        pass

    @abstractmethod
    def get_mail(self, n):
        """Returns the mail number n
        """
        pass

    @abstractmethod
    def get_header(self, n):
        """Returns the header of the mail number n
        """
        pass

    @abstractmethod
    def get_mailbox_size(self):
        """Returns the size of the mailbox
        """
        pass

    @abstractmethod
    def get_total_mails(self):
        """Returns the number of all mails in the mailbox
        """
        pass

    @abstractmethod
    def delete_mail(self, n):
        """Returns True if mail n was successfully marked for deletion
        """
        pass

    @abstractmethod
    def quit(self):
        pass