from pip import __main__
from sqlalchemy.orm.exc import NoResultFound
import time
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker, contains_eager
from models import *


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
        mail = self.session.query(Inbox)\
            .filter(and_(getattr(Mails, what) == value)).one()

        return mail

    def getMails(self):
        pass

    def insertMail(self, subject):
        mail = Mails()
        mail.subject = subject

    def createInbox(self, userMail, account, password, server, port, protocol):
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
        inbox.userMail = userMail
        inbox.account = account
        inbox.password = password
        inbox.server = server
        inbox.port = port
        inbox.protocol = protocol

        self.session.add(inbox)
        self.execute()

    def execute(self):
        self.session.commit()
        self.session.flush()

    def __del__(self):
        if self.session is not None:
            self.session.close()

if __name__ == "__main__":
    test = Database()
    print(test.getMailBy("id", 1))