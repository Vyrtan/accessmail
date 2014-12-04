from src.models import Mails

__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup


Builder.load_file("GUI/ContactItem.kv")
Builder.load_file("GUI/deletePopupContact.kv")


class ContactItem(BoxLayout):
    """
    This class is the controller class to the corresponding ContactItem View. It is used to
    delete the held contact or transfers the e-mail address to the WriteLayout in case the user
    wants to write an e-mail to this contact.

    :param contact: The contact to be displayed
    :param kwargs:
    """
    name = StringProperty()
    email = StringProperty()
    subject = StringProperty()
    picture = StringProperty()
    root = ObjectProperty()
    grey = BooleanProperty()

    def __init__(self, contact=None, **kwargs):
        super(ContactItem, self).__init__(**kwargs)
        self.contact = contact
        self.name = contact.name
        self.email = contact.emailAddress
        self.picture = "GUI/Icons/iStandard_user.png" if not contact.picture else contact.picture
        self.grey = False
        if kwargs.get("colour", None):
            self.grey = True

    def trigger_delete(self):
        '''
        This method is used to delete the contained contact-object.
        It opens up the Popup which finally deletes it from the database.

        :return:
        '''
        d = self.root
        p = DeletePopupContacts(self.contact, d)
        p.open()

    # switches to WriteLayout and already fills in the address (supposedly)
    def trigger_write_mail(self):
        '''
        This method transfers the e-mail address to the WriteLayout, where the first Input field is then
        already filled in. It also triggers the change to the respective layout.

        :return:
        '''
        mail = Mails()
        mail._from = self.email
        mail.subject = ""
        mail.message = ""
        self.root.parent.parent.parent.parent.parent.parent.show_layout("Write", email=mail)


class DeletePopupContacts(Popup):

    """
    This class handles the Popup which asks for confirmation in case a contact shall be deleted.

    :param contact: The contact to be deleted.
    :param d: The addressbook which manages the final deletion.
    """

    def __init__(self, contact, d):
        super(DeletePopupContacts, self).__init__()
        self.cont = contact
        self.chef = d

    def delete_contact(self):
        '''
        This method deletes the contact by calling the method from the addressbook itself.

        :return:
        '''
        self.chef.parent.parent.parent.delete_contact(self.cont)
