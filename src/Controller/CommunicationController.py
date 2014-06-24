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
