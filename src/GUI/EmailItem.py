__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup
from src.database import Database
from src.Controller.CommunicationController import CommunicationController
from kivy.graphics import Color
import string


Builder.load_file("GUI/EmailItem.kv")
Builder.load_file("GUI/deletePopup.kv")


class EmailItem(BoxLayout):
    """
    This class manages the corresponding controller level for e-mails. Single e-mails can be displayed in
    the inbox and in the outbox. The necessary data is transferred through the email parameter.

    :param email: The email to be displayed.
    :param kwargs:
    """
    name = StringProperty()
    email = StringProperty()
    subject = StringProperty()
    root = ObjectProperty()
    oMail = ObjectProperty()
    grey = BooleanProperty()
    read = BooleanProperty()

    def __init__(self, email, rootwidget, **kwargs):
        super(EmailItem, self).__init__(**kwargs)
        self.oMail = email
        self.name = string.split(email._from, "@")[0]
        self.email = email._from
        self.grey = False
        self.read = email.read
        self.rootwidget = rootwidget
        if email.subject:
            self.subject = email.subject if len(email.subject) <= 20 else email.subject[:20] + "..."
        else:
            self.subject = "None"
        if kwargs.get("colour", None):
            self.grey = True

    # delete email with corresponding id from model
    def trigger_delete(self):
        '''
        This method deletes the email which is being displayed by the instance of this class.

        :return:
        '''
        p = DeletePopup(self.oMail, self.rootwidget)
        p.open()

    # call this function with some email id to switch to the corresponding email from the model
    def trigger_read(self):
        '''
        This method switches to the ReadLayout where the e-mail message can be looked at in full text.
        It calls the screenmanager and hands over the e-mail object.

        :return:
        '''
        # best. expression. ever.
        self.root.parent.parent.parent.parent.parent.parent.show_layout("Read", email=self.oMail)

    # get address and subject, create new email
    def trigger_reply(self):
        '''
        This method switches to the WriteLayout handing over the correct e-mail address, the subject
        with a "Re:" string addition and the original message with usual Reply-Mail formatting.

        :return:
        '''
        self.root.parent.parent.parent.parent.parent.parent.show_layout("Write", email=self.oMail)


class DeletePopup(Popup):

    """
    This class is used to delete E-mails within the inbox or outbox Layout.

    :param mail:
    """

    def __init__(self, mail, inbox):
        super(DeletePopup, self).__init__()
        self.em = mail
        self.inbox = inbox

    def delete_mail(self):
        '''
        This method deletes the e-mail from the database and calls the method to delete the e-mail from
        the server as well.

        :return:
        '''
        db = Database()
        db.deleteMail(self.em)
        CommunicationController.delete_mail(self.em)
        self.inbox.scheduled_mail_check("lolno")