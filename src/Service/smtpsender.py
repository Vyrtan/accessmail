from email.message import Message
import smtplib
from database import Database

__author__ = 'ubuntu'


class SMTPSender(object):

    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.user = config['user']
        self.pw = config['pw']
        self.ssl = config['ssl']

        self.conn = None

    def connect(self):
        if self.ssl:
            self.conn = smtplib.SMTP_SSL(self.host, self.port)
        else:
            self.conn = smtplib.SMTP(self.host, self.port)

        self.conn.login(self.user, self.pw)

    def send_mail(self, _from, to, subject, msg, attachments):
        if self.conn is None:
            self.connect()

        mail = self._compile_mail(_from, to, subject, msg, attachments)

        self.conn.sendmail(_from, to, mail)

    def _compile_mail(self, _from, to, subject, _msg, attachments):
        msg = Message()
        msg.set_payload(_msg)
        msg["Subject"] = subject
        msg["From"] = _from
        msg["To"] = to

        return msg.as_string()


if __name__ == '__main__':
    db = Database()
    inbox = db.getInbox()
    dicti = {
        'host': inbox.smtpServer,
        'port': inbox.smtpPort,
        'user': inbox.userMail,
        'pw': inbox.password,
        'ssl': inbox.smtpSSL
    }
    test = SMTPSender(dicti)
    test.connect()