from pip import __main__
from sqlalchemy.orm.exc import NoResultFound
import time
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker, contains_eager
from models import *
from time import strptime


class Database:
    
    def __init__(self):

        uri = 'sqlite:///../data.db'

        if __debug__:
            self.engine = create_engine(uri, echo=True)
        else:
            self.engine = create_engine(uri, echo=True)

        session = sessionmaker(bind=self.engine)
        self.session = session()

    def getMailBy(self, what, value):
        """

        :param what: By What do you want to search?
        :type what: string
        :param value: Which value should I search for?
        :type value: object
        :return: returns an email by id
        :rtype: Mails
        """
        mail = self.session.query(Mails)\
            .filter(and_(getattr(Mails, what) == value)).first()

        return mail

    def getAllMails(self):
        """
        :return: returns a list of emails
        :rtype: Mails
        """
        mails = self.session.query(Mails).all()
        return mails

    def insertMail(self, pmail):
        """

        :param subject: Mail's subject
        :type subject: str
        :type inbox: Inbox
        :return:
        """
        for m in self.session.query(Mails).all():
            if (m.date == pmail.date) & (m.subject == pmail.subject):
                print("Email dismissed")
                return

        mail = Mails()
        mail.date = pmail.date
        mail.subject = unicode(pmail.subject, "utf-8")
        mail._from = unicode(pmail._from, "utf-8")
        mail.bcc = unicode(pmail.bcc, "utf-8")
        mail.cc = unicode(pmail.cc, "utf-8")
        mail.inReplyTo = unicode(pmail.inReplyTo, "utf-8")
        mail.message = unicode(pmail.message, "utf-8")
        mail.inboxId = pmail.inboxId

        self.session.add(mail)
        self.execute()

    def deleteMail(self, email):
        self.session.delete(email)
        self.execute()

    # Contacts
    def getContacts(self):
        contacts = self.session.query(Contacts).all()
        return contacts

    def insertContact(self, pContact):
        contact = Contacts()
        contact.name = unicode(pContact.name, "utf-8")
        contact.emailAddress = unicode(pContact.emailAddress, "utf-8")
        self.session.add(contact)
        self.execute()

    def deleteContact(self, contact):
        self.session.delete(contact)
        self.execute()

    def createInbox(self, firstName, lastName, userMail, account, password, imapServer, smtpServer, imapPort, smtpPort, imapSSL, smtpSSL, smtpAuth):
        """
        Creates an Inbox

        :type userMail: str
        :type account: str
        :type password: str
        :type server: str
        :type port: int
        :type protocol: str
        """
        inbox = Inbox()
        inbox.firstName = firstName
        inbox.lastName = lastName
        inbox.userMail = userMail
        inbox.account = account
        inbox.password = password
        inbox.imapServer = imapServer
        inbox.smtpServer = smtpServer
        inbox.imapPort = imapPort
        inbox.smtpPort = smtpPort
        inbox.imapSSL = imapSSL
        inbox.smtpSSL = smtpSSL
        inbox.smtpAuth = smtpAuth

        self.session.add(inbox)
        self.execute()

        return inbox

    def hasInbox(self):
        try:
            self.session.query(Inbox).one()
        except NoResultFound:
            return False

        return True

    def getInbox(self):
        """
        :rtype: Inbox
        """
        return self.session.query(Inbox).first()

    def execute(self):
        self.session.commit()
        self.session.flush()

    def close(self):
        if self.session is not None:
            self.session.close()

    def __del__(self):
        if self.session is not None:
            self.session.close()

if __name__ == "__main__":
    test = Database()
    _inbox = test.createInbox("abc", "abc", "abc", "abc", 22, "asds")
    test.insertMail("blabal", _inbox)
    print(test.getMailBy("id", 1).subject)