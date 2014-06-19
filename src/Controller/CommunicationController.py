__author__ = 'grafgustav'
import MainController
import smtplib
import email #TODO: Python mail class im Modell?
import imaplib
import poplib


class CommunicationController(object):

    def __init__(self, main_controller):
        self.__credentials = self._load_credentials()
        self.__inbox = self._load_inbox()
        self.__main_controller = main_controller

    def _imap_login(self):
        connection = imaplib.IMAP4_SSL() #TODO: Daten aus Model laden, SSL ?
        connection.login()
        return connection

    def _pop_login(self):
        connection = poplib.POP3_SSL()
        connection.login()
        return connection

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



    def _getmailboxes_imap(self):
        c = self._imap_login()
        typ, data = c.list()    #TODO: Richtige Mailbox auswaehlen(erstmal nur "Bekannte?")
        c.close()
        c.logout()
        return data

    def _getmails_imap(self):
        c = self._imap_login()
        c.select()
        rv, data = c.search(None, "ALL")           #TODO: Mailbox auswaehlen, holt sich erstmal ALLE mails
        for num in data[0].split():
            typ, msg_data = c.fetch(num, '(RFC822)')
        msg = email.message_from_string(msg_data[0][1]) #typ und rv können für Fehlermeldungen genutzt werden.
        c.close()                                       # beinhalten server antwort.
        c.logout()
        return msg         #TODO: Daten weiter verarbeiten

    def _getmails_pop(self):
        c = self._pop_login()
        msg = c.list()      #TODO: alle Messages in String format (liste)
        c.quit()
        return msg

    def _pop_delete(self, msgnum):
        c = self._pop_login()
        msgs = self._getmails_pop()
                                    #TODO: msg filtern nach der zu löschenden msgnum!
        c.dele(msgnum)
        c.quit()

    # TODO: delete imap/pop
