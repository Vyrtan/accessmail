__author__ = 'grafgustav'
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from Tooltip import ToolTip


Builder.load_file('GUI/menuLayout.kv')


class MenuLayout(Screen):

    inboxBtn = ObjectProperty()
    outboxBtn = ObjectProperty()
    writeBtn = ObjectProperty()
    contactBtn = ObjectProperty()
    exitBtn = ObjectProperty()

    def __init__(self, **kwargs):
        super(MenuLayout, self).__init__(**kwargs)
        Clock.schedule_interval(self.check_mouse_pos, 1)
        self.tooltip_active = ""

    def check_mouse_pos(self, _):
        pos = Window.mouse_pos

        if self.inboxBtn.collide_point(pos[0], pos[1]):
            if (not self.tooltip_active) | (self.tooltip_active != "inbox"):
                tp = ToolTip(text="Inbox")
                self.inboxBtn.add_widget(tp)
                self.tooltip_active = "inbox"
                # clear all other tooltips
                self.contactBtn.clear_widgets()
                self.outboxBtn.clear_widgets()
                self.exitBtn.clear_widgets()
                self.writeBtn.clear_widgets()

        elif self.outboxBtn.collide_point(pos[0], pos[1]):
            if (not self.tooltip_active) | (self.tooltip_active != "outbox"):
                tp = ToolTip(text="Sent\nMessages")
                self.outboxBtn.add_widget(tp)
                self.tooltip_active = "outbox"
                # clear all other tooltips
                self.inboxBtn.clear_widgets()
                self.contactBtn.clear_widgets()
                self.exitBtn.clear_widgets()
                self.writeBtn.clear_widgets()

        elif self.writeBtn.collide_point(pos[0], pos[1]):
            if (not self.tooltip_active) | (self.tooltip_active != "write"):
                tp = ToolTip(text="Write a\nnew E-mail")
                self.writeBtn.add_widget(tp)
                self.tooltip_active = "write"
                # clear all other tooltips
                self.inboxBtn.clear_widgets()
                self.outboxBtn.clear_widgets()
                self.exitBtn.clear_widgets()
                self.contactBtn.clear_widgets()

        elif self.contactBtn.collide_point(pos[0], pos[1]):
            if (not self.tooltip_active) | (self.tooltip_active != "contact"):
                tp = ToolTip(text="Add and delete\nContacts")
                self.contactBtn.add_widget(tp)
                self.tooltip_active = "contact"
                # clear all other tooltips
                self.inboxBtn.clear_widgets()
                self.outboxBtn.clear_widgets()
                self.exitBtn.clear_widgets()
                self.writeBtn.clear_widgets()
        elif self.exitBtn.collide_point(pos[0], pos[1]):
            if (not self.tooltip_active) | (self.tooltip_active != "exit"):
                tp = ToolTip(text="Exit the\nprogram")
                self.exitBtn.add_widget(tp)
                self.tooltip_active = "exit"
                # clear all other tooltips
                self.inboxBtn.clear_widgets()
                self.outboxBtn.clear_widgets()
                self.contactBtn.clear_widgets()
                self.writeBtn.clear_widgets()
        else:
            self.tooltip_active = ""
            self.inboxBtn.clear_widgets()
            self.outboxBtn.clear_widgets()
            self.contactBtn.clear_widgets()
            self.writeBtn.clear_widgets()
            self.exitBtn.clear_widgets()




