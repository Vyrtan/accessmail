from pip import __main__
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker, contains_eager
from models import *


class Database:
    
    def __init__(self):

        # change back to relative path!
        uri = 'sqlite:///../data.db'
        # print uri

        if __debug__:
            self.engine = create_engine(uri, echo=True)
        else:
            self.engine = create_engine(uri, echo=True)

        session = sessionmaker(bind=self.engine)
        self.session = session()

    def get_mail_by(self, identifier, value):
        """
        This method searches the database for a certain criteria with a corresponding value and returns
        the found object. It is necessarily an e-mail object. The


        :param identifier: The criteria used to search for
        :type identifier: string
        :param value: The value used to search for
        :type value: object
        :return: returns an email by id
        :rtype: Mails
        """
        mail = self.session.query(Mails)\
            .filter(and_(getattr(Mails, identifier) == value)).first()

        return mail

    def get_all_mails(self):
        """
        This method is used to get all available mails from the Mails-table.

        :return: returns a list of emails
        :rtype: Mails
        """
        mails = self.session.query(Mails).all()[::-1]
        return mails

    def insert_mail(self, pmail):
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
        mail.message = unicode(pmail.message, "utf-8", errors="replace")
        mail.inboxId = pmail.inboxId
        mail.remoteID = pmail.remoteID

        self.session.add(mail)
        self.execute()

    # this is intended to mark an email (in the database) as read
    # i think it's too complicated to synchronize this with the server
    def mark_mail_as_read(self, email):
        """
        This mail uses the attribute "read" of an e-mail object and modifies it in the database.
        Like this read e-mails and not yet read e-mails can be seperated.

        :param email: The E-Mail that is supposed to get marked
        :type Mails: Mails
        :return:
        """
        # TODO: change this to actually using the power of sqlalchemy
        self.session.execute("UPDATE Mails SET read=1 WHERE id=%d;"%(email.id))
        self.execute()

    def get_not_read_mails(self):
        """
        This method is used to search for all mails which have not been read yet.

        :return: Returns all Mails which have not been marked as read
        :rtype: [Mails]: List of Mails

        """
        mails = self.session.query(Mails).filter(and_(getattr(Mails, "read") == 0)).all()
        return mails

    def get_sent_mails(self):
        """
        This method is used to get all mails from the database, which have been sent by the currently
        logged in user account. The active inbox is used to compare to.

        :return: Returns all Mails which have been sent by the currently logged in inbox
        :rtype: [Mails]: List of Mails
        """
        inbox = self.get_inbox()
        mail = inbox.userMail
        mails = self.session.query(Mails).filter(and_(getattr(Mails, "_from") == mail)).all()
        return mails

    def delete_mail(self, email):
        """
        This method removes an e-mail from the database.

        :param: email: The email that ought to be deleted
        :type: Mails: Mails
        :return
        """
        self.session.delete(email)
        self.execute()

    # Contacts
    def get_contacts(self):
        '''
        This method is used to get all contacts stored in the database.

        :return: [Contacts]: A list of contacts
        '''
        contacts = self.session.query(Contacts).all()
        return contacts

    def insert_contact(self, pContact):
        """
        This method is used to insert a new contact into the database.

        :param: pContact: The contact that ought to be added to the database
        :type: Contacts: Contacts
        :return
        """
        contact = Contacts()
        contact.name = unicode(pContact.name, "utf-8")
        contact.emailAddress = unicode(pContact.emailAddress, "utf-8")
        contact.picture = unicode(pContact.picture, "utf-8") if pContact.picture else None
        self.session.add(contact)
        self.execute()

    def delete_contact(self, contact):
        """
        This method is used to delete a specified contact from the database.

        :param: contact: The contact that ought to be deleted to the database
        :type: Contacts: Contacts
        :return
        """
        self.session.delete(contact)
        self.execute()

    def create_inbox(self, firstName,
                     lastName,
                     userMail,
                     account,
                     password,
                     imapServer,
                     smtpServer,
                     imapPort,
                     smtpPort,
                     imapSSL,
                     smtpSSL,
                     smtpAuth,
                     nbr_mails=5,
                     nbr_addresses=5,
                     colourblind_mode=0,
                     font_size=10):
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
        inbox.nbr_mails = nbr_mails
        inbox.nbr_addresses = nbr_addresses
        inbox.colourblind_mode = colourblind_mode
        inbox.font_size = font_size

        self.session.add(inbox)
        self.execute()

        return inbox

    def has_inbox(self):
        '''
        This method is used to check whether an inbox is already existing.

        :return: Boolean: True if there is an inbox, False if there is not.
        '''
        try:
            self.session.query(Inbox).one()
        except NoResultFound:
            return False

        return True

    def get_inbox(self):
        """
        This method is used to return the currently logged in inbox.

        :return The currently logged in inbox (account info, server info, etc.)
        :rtype: Inbox
        """
        inbox = self.session.query(Inbox).first()
        return inbox

    def get_settings(self, identifier):
        """
        This method returns the settings saved in the inbox
        the passed argument defines which part of the settings shall be returned
        the default value for the parameter is "All"

        possible values are:
            number of mails
            number of adresses
            colourblind mode
            font size

        :param: settings: String identifying the settings value to be fetched
        :return: the setting values requested
        :rtype: Tuple, Integer or Boolean
        """
        inbox = self.session.query(Inbox).first()
        return getattr(inbox, identifier)

    def edit_settings(self, identifier, value):
        """

        :param identifier: String identifying the settings value to be set
        :param value: the value to be set
        """
        inbox = self.session.query(Inbox).first()
        # TODO: change this to actually using the power of sqlalchemy
        self.session.execute("UPDATE inboxes SET %s=%d WHERE id=%d;"%(identifier, value, inbox.id))
        self.execute()
        return inbox

    #function not used yet
    # def resetAll(self):
    #     print("Deleting everything")
    #     self.session.expunge_all()
    #     self.execute()

    def execute(self):
        """
        Commits all changes to the databases

        :return:
        """
        self.session.commit()

    def close(self):
        if self.session is not None:
            self.session.close()

    def __del__(self):
        if self.session is not None:
            self.session.close()

if __name__ == "__main__":
    test = Database()
    _inbox = test.create_inbox("abc", "abc", "abc", "abc", 22, "asds")
    test.insert_mail("blabal", _inbox)
    print(test.get_mail_by("id", 1).subject)