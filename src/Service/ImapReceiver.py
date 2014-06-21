__author__ = 'phillip'

from .MailReceiver import MailReceiver
import poplib


class IMAPReceiver(MailReceiver):

    def __init__(self, config):
        self._conn = None

    def connect(self, config):
        self._server = poplib.POP3_SSL()
        self._server.apop()

    def delete_mail(self, n):
        self._server.dele(n)

    def list_folders(self):
        pass

    def create_folder(self, name):
        pass

    def get_number_of_mails(self):
        count, size = self._server.stat()
        return count

    def change_folder(self, path):
        pass

    def get_header(self, n):
        return self._server.top(n,0)

    def can_create_folder(self):
        return False

    def delete_folder(self, name):
        pass

    def get_total_mails(self):
        return self.get_number_of_mails()

    def get_mail(self, n):
        return self._server.retr(n)

    def get_mailbox_size(self):
        count, size = self._server.stat()
        return size

    def quit(self):
        self._server.quit()