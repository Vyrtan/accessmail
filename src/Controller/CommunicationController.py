__author__ = 'grafgustav'
import MainController
import smtplib
import email #TODO: Python mail class im Modell?
import imaplib

def _imap_login(self):
    connection = imaplib.IMAP4_SSL() #TODO: Daten aus Model laden, SSL ?
    connection.login()
    return connection

class CommunicationController(object):

    def __init__(self, main_controller):
        self.__credentials = self._load_credentials()
        self.__inbox = self._load_inbox()
        self.__main_controller = main_controller

    def _load_credentials(self):
        cred = self.__main_controller.get_database_controller().load_credentials()
        return cred

    def _load_inbox(self):
        inb = self.__main_controller.get_database_controller().load_inbox()
        return inb

    def _send(self):                              #TODO: Mail aus Model laden? (Wo/wann ins Model kopieren)
       connection = smtplib.SMTP()      #TODO: Inbox in Feld umwandeln, SSL verschluesselung?
       connection.starttls()
       connection.login()              #TODO: Python mail class benutzen?
       connection.sendmail()
       connection.quit()

    #TODO: IMAP verbindung dauerhaft aufrechterhalten? Oder Intervall abfrage? Oder Buttons?



    def _getmailboxes(self):
        c = _imap_login()
        typ, data = c.list()    #TODO: Richtige Mailbox auswaehlen(erstmal nur "Bekannte?")
        c.close()
        c.logout()
        return data

    def _getmails(self):
        c = _imap_login()
        c.select()              #TODO: Mailbox auswaehlen
        typ, msg_data = c.fetch('1', '(BODY.PEEK[HEADER] FLAGS)')   #TODO: Nur Recent abfragen?
        c.close()
        c.logout()
        return msg_data         #TODO: Daten weiter verarbeiten


