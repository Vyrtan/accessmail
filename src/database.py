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
        This method searches the database for a certain criteria with a corresponding value and returns
        the found object. It is necessarily an e-mail object. The


        :param what: The criteria used to search for
        :type what: string
        :param value: The value used to search for
        :type value: object
        :return: returns an email by id
        :rtype: Mails
        """
        mail = self.session.query(Mails)\
            .filter(and_(getattr(Mails, what) == value)).first()

        return mail

    def getAllMails(self):
        """
        This method is used to get all available mails from the Mails-table.

        :return: returns a list of emails
        :rtype: Mails
        """
        mails = self.session.query(Mails).all()[::-1]
        return mails

    def insertMail(self, pmail):
        """
        This method inserts a new mail to the database.

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
        mail.bcc = pmail.bcc
        mail.read = pmail.read
        mail.cc = unicode(pmail.cc, "utf-8") if pmail.cc else ""
        mail.inReplyTo = pmail.inReplyTo
        mail.message = unicode(pmail.message, "utf-8")
        mail.inboxId = pmail.inboxId
        mail.remoteID = pmail.remoteID

        self.session.add(mail)
        self.execute()

    # this is intended to mark an email (in the database) as read
    # i think it's too complicated to synchronize this with the server
    def markMailAsRead(self, email):
        """
        This mail uses the attribute "read" of an e-mail object and modifies it in the database.
        Like this read e-mails and not yet read e-mails can be seperated.

        :param email: The E-Mail that is supposed to get marked
        :type Mails: Mails
        :return:
        """
        self.session.execute("UPDATE Mails SET read=1 WHERE id=%d;"%(email.id))
        print "email marked as read"
        self.execute()

    def getNotReadMails(self):
        """
        This method is used to search for all mails which have not been read yet.

        :return: Returns all Mails which have not been marked as read
        :rtype: [Mails]: List of Mails

        """
        mails = self.session.query(Mails).filter(and_(getattr(Mails, "read") == 0)).all()
        return mails

    def getSentMails(self):
        """
        This method is used to get all mails from the database, which have been sent by the currently
        logged in useraccount. The active inbox is used to compare to.

        :return: Returns all Mails which have been sent by the currently logged in inbox
        :rtype: [Mails]: List of Mails
        """
        inbox = self.getInbox()
        mail = inbox.userMail
        mails = self.session.query(Mails).filter(and_(getattr(Mails, "_from") == mail)).all()
        return mails

    def deleteMail(self, email):
        """
        This method removes an e-mail from the database.

        :param: email: The email that ought to be deleted
        :type: Mails: Mails
        :return
        """
        self.session.delete(email)
        self.execute()

    # Contacts
    def getContacts(self):
        '''
        This method is used to get all contacts stored in the database.

        :return: [Contacts]: A list of contacts
        '''
        contacts = self.session.query(Contacts).all()
        return contacts

    def insertContact(self, pContact):
        """
        This method is used to insert a new contact into the database.

        :param: pContact: The contact that ought to be added to the database
        :type: Contacts: Contacts
        :return
        """
        contact = Contacts()
        contact.name = unicode(pContact.name, "utf-8")
        contact.emailAddress = unicode(pContact.emailAddress, "utf-8")
        self.session.add(contact)
        self.execute()

    def deleteContact(self, contact):
        """
        This method is used to delete a specified contact from the database.

        :param: contact: The contact that ought to be deleted to the database
        :type: Contacts: Contacts
        :return
        """
        self.session.delete(contact)
        self.execute()

    def createInbox(self, firstName, lastName, userMail, account, password, imapServer, smtpServer, imapPort, smtpPort, imapSSL, smtpSSL, smtpAuth):
        """
        Creates an Inbox which contains all information about a user.
        The information which are necessary to connect to the e-mail server are stored in this
        object as well.

        So far only one inbox can be used, however, in the future more inboxes can be added.

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
        '''
        This method is used to check whether an inbox is already existing.

        :return: Boolean: True if there is an inbox, False if there is not.
        '''
        try:
            self.session.query(Inbox).one()
        except NoResultFound:
            return False

        return True

    def getInbox(self):
        """
        This method is used to return the currently logged in inbox.

        :return The currently logged in inbox (account info, server info, etc.)
        :rtype: Inbox
        """
        inboxes = self.session.query(Inbox)
        print inboxes
        return inboxes.first()

    #function not used yet
    # def resetAll(self):
    #     print("Deleting everything")
    #     self.session.expunge_all()
    #     self.execute()

    def execute(self):
        '''
        Commits all changes to the databases

        :return:
        '''
        self.session.commit()
        # flush after commit is redundant
        # self.session.flush()

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