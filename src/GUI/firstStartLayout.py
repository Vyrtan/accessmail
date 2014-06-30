__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("GUI/firstStart.kv")


class FirstStartLayout(BoxLayout):

    """
    This class is used to partially manage the first start of the program.
    It leads to the next Layout, where the necessary user data can be inserted.

    :param kwargs:
    """

    def __init__(self, **kwargs):
        super(FirstStartLayout, self).__init__(**kwargs)
        self.size_hint_x = 1

    #switch togglebutton to display password
    # def on_passwC_toggle(self, state):
    #     if state == "down":
    #         self.passwInput.password = False
    #     else:
    #         self.passwInput.password = True
