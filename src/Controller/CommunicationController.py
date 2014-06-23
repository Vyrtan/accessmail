__author__ = 'grafgustav'
import smtplib
import email
import imaplib
import poplib
from src.database import Database
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.models import Mails

clunkyConfig = {
    0: {
        "IMAP": {
            "host": "imap.gmail.com",
            "port": 993,
            "ssl": True
        },
        "SMTP": {
            "host": "smtp.gmail.com",
            "port": 465,
            "ssl": True,
            "auth": True
        }
    }
}


class CommunicationController(object):

    def __init__(self):
        self.__credentials = self._load_credentials()
        self.__inbox = self._load_inbox()

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
        c.dele(msgnum)
        c.quit()

    @staticmethod
    def getEmailsFromServer():


        try:
            # open database connection and get credentials
            db = Database()
            inbox = db.getInbox()

            # establish IMAP Connection
            imapCon = imaplib.IMAP4_SSL(inbox.imapServer, int(inbox.imapPort))

            # get inbox id for later use
            inboxID = inbox.id

            if(inbox.imapServer=="imap.web.de"):
                emailAddress = inbox.account
            else:
                emailAddress = inbox.userMail

            password = inbox.password

            imapCon.login(emailAddress, password)
            # fetch emails from server
            imapCon.select("inbox")
            result, data = imapCon.search(None, "ALL")
            ids = data[0].split()
            raw_mails = []
            index = 0
            for i in ids:
                result, data = imapCon.fetch(i, "(RFC822)")
                raw_mails.append(data[0][1])
                m = Mails()

                e = email.message_from_string(raw_mails[index])
                m_name, m.to = email.utils.parseaddr(e["To"])
                m_name, m._from = email.utils.parseaddr(e["From"])
                m.date = e["Date"]
                m.cc = e["CC"]
                m.subject = e["Subject"]
                m.inReplyTo = e["In-Reply-To"]
                m.read = 0
                message = ""
                if e.is_multipart():
                    for payload in e.get_payload():
                        message = message + " " + str(payload)
                else:
                    message = e.get_payload()
                m.message = message
                m.inboxId = inboxID
                db.insertMail(m)
                index += 1

            # close database connection
            db.close()
            imapCon.logout()
        except imaplib.IMAP4.error as e:
            print(e)
