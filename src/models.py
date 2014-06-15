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
    messageId = Column(String(255), index=True)
    inboxId = Column(Integer, ForeignKey('inboxes.id'))


class Inbox(Base):
    __tablename__ = 'inboxes'

    id = Column(Integer, primary_key=True)
    userMail = Column(String(255))  #TODO: We should use the internal sqlite date type
    password = Column(String(255), index=True)
    server = Column(String(255))
    port = Column(String(255))
    protocol = Column(String(255))
    authProtocol = Column(String(255))
    caches = relationship("ConCacheConcrete")

#simply add a class like this?
class Contacts(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    firstName = Column(String(255))  #TODO: We should use the internal sqlite date type
    lastName = Column(String(255), index=True)
    emailAddress = Column(String(255))