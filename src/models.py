__author__ = 'ubuntu'

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Email(Base):
    __tablename__ = 'mail'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)