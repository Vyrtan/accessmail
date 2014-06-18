__author__ = 'grafgustav'
import MainController
import smtplib
import email #TODO: Python mail class im Modell?
import imaplib


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

    def _send(self):                   #TODO: Mail aus Model laden? (Wo/wann ins Model kopieren)
       connection = smtplib.SMTP_SSL() #TODO: Inbox in Feld umwandeln, SSL verschlüsselung?
       connection.login()              #TODO: Python mail class benutzen?
       connection.sendmail()
       connection.close()

    #TODO: IMAP verbindung dauerhaft aufrechterhalten? Oder Intervall abfrage? Oder Buttons?

    def _getmails(self):
        connection = imaplib.IMAP4_SSL() #TODO: Daten aus Model laden
        connection.login()
        mail = connection.fetch()       #TODO: Mail an DataBase übergeben
        connection.close()
        connection.logout()

    def _getstats(self):
        connection = imaplib.IMAP4_SSL() #TODO: Daten aus Model laden
        connection.login()
        mail = connection.status()       #TODO: Brauchen wir Size und Count`?
        connection.close()
        connection.logout()

     def _del(self):
        connection = imaplib.IMAP4_SSL() #TODO: Daten aus Model laden
        connection.logiin()
        mail = connection.delete()       #TODO: Richtiger Befehl Phillip? oder lösche ich ne ganze Mailbox? :D
        connection.quit()
        connection.close()
        connection.logout()