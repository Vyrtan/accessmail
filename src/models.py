__author__ = 'ubuntu'

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Mails(Base):
    __tablename__ = 'mails'

    id = Column(Integer, primary_key=True)
    date = Column(String(255))  #TODO: We should use the internal sqlite date type
    subject = Column(String(255), index=True)
    _from = Column(String(255))
    to = Column(String(255))
    cc = Column(Text)
    bcc = Column(Text)
    inReplyTo = Column(String(255), index=True)
    message = Column(String(255), index=True)
    read = Column(Integer())
    inboxId = Column(Integer, ForeignKey('inboxes.id'))


class Inbox(Base):
    __tablename__ = 'inboxes'

    id = Column(Integer, primary_key=True)
    userMail = Column(String(255))
    account = Column(String(255))
    password = Column(String(255), index=True)

    firstName = Column(String(255))
    lastName = Column(String(255))

    imapServer = Column(String(255))
    smtpServer = Column(String(255))

    imapPort = Column(String(255))
    smtpPort = Column(String(255))

    imapSSL = Column(Integer())
    smtpSSL = Column(Integer())

    smtpAuth = Column(Integer())
    caches = relationship("Mails")

#simply add a class like this?
class Contacts(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    emailAddress = Column(String(255))