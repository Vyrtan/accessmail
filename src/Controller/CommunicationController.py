__author__ = 'grafgustav'
import smtplib
import email
import imaplib
from src.database import Database
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.models import Mails
from clunky_config import clunkyConfig


class CommunicationController(object):
    ''' This class handles the communication with the remote server.

    This class only contains static methods. There are no attributes of the class used.
    Because of the static character of the methods we can access them equally from
    everywhere.

    It automatically looks for the necessary connection data in the database.

    Example:
        To get the emails from the server import the module, call the class and the method:
        from src.Controller.CommuncationController import CommunicationController
        CommunicationController.getEmailsFromServer()


    '''


    @staticmethod
    def getEmailsFromServer():
        '''
        This method fetches all emails in the remote folder "inbox" and stores them in the database.

        :return
        '''

        try:
            # open database connection and get credentials
            db = Database()
            inbox = db.get_inbox()

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
                # content_type = e["Content-Type"]
                # print content_type
                m.read = 0
                m.remoteID = e.get("message-ID", None)
                print m.remoteID

                message = ""
                if e.is_multipart():
                    for payload in e.get_payload():
                        message = message + " " + str(payload)
                else:
                    message = e.get_payload()
                m.message = message
                m.inboxId = inboxID
                db.insert_mail(m)
                index += 1

            # close database connection
            db.close()
            imapCon.logout()
        except imaplib.IMAP4.error as e:
            print(e)

    @staticmethod
    def delete_mail(mail):
        '''
        This method takes an email-object, adds the flag "\\Deleted" and sends it to the server.
        The IMAP server then deletes the mail.

        :param mail: The mail to be deleted.
        :type: Mails
        :return:
        '''

        # open database connection and get credentials
        db = Database()
        inbox = db.get_inbox()
        try:
            # establish IMAP Connection
            imap_con = imaplib.IMAP4_SSL(inbox.imapServer, int(inbox.imapPort))

            if inbox.imapServer=="imap.web.de":
                emailAddress = inbox.account
            else:
                emailAddress = inbox.userMail

            password = inbox.password

            imap_con.login(emailAddress, password)
            imap_con.select('Inbox')

            search_query = '(HEADER message-id %s)' % mail.remoteID

            typ, data = imap_con.search(None, search_query)

            imap_con.store(data[0], '+FLAGS', '\\Deleted')
            imap_con.expunge()
            imap_con.close()
            db.close()
            imap_con.logout()
        except imaplib.IMAP4.error as e:
            print(e)

    # gets all sent mails from the server
    @staticmethod
    def getSentFromServer():
        ''' This method fetches all stored mails from the server from the "Sent" folder.
        The received emails are then stored in the database.

        :return:
        '''
        try:
            # open database connection and get credentials
            db = Database()
            inbox = db.get_inbox()

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
            if(inbox.imapServer=="imap.web.de"):
                imapCon.select("Sent")
            else:
                imapCon.select("Sent Mail")
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
                m.read = 1
                m.remoteID = e.get("message-ID", None)

                message = ""
                if e.is_multipart():
                    for payload in e.get_payload():
                        message = message + " " + str(payload)
                else:
                    message = e.get_payload()
                m.message = message
                m.inboxId = inboxID
                db.insert_mail(m)
                index += 1

            # close database connection
            db.close()
            imapCon.logout()
        except imaplib.IMAP4.error as e:
            print(e)