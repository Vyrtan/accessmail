__author__ = 'grafgustav'

from Singleton import Singleton
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
from src.GUI.Tooltip import ToolTip


@Singleton
class WidgetManager:

    def __init__(self):
        self.root_widget = None
        self.popup_root = None
        self.iterable_list = []
        self.current_butt = 0
        self.previous_mouse_position = None
        self.tooltip_active = False
        print "Widget Manager created"

    def set_root_widget(self, r):
        self.root_widget = r

    def get_root_widget(self):
        return self.root_widget

    def get_widget_list(self):
        return self.iterable_list

    def set_popup_root(self, pop):
        self.popup_root = pop

    def get_popup_root(self):
        return self.popup_root

    # kivy sometimes takes time to load all widgets properly
    # delaying the actual construction of the tree does not guarantee a proper tree construction,
    # but it works
    def build_tree(self, _):
        Clock.schedule_once(self.build_tree_execute, 0.5)

    def build_tree_execute(self, _):
        print "Building Tree"
        buttons = []
        text_input = []
        stack = [self.root_widget] if not self.popup_root else [self.popup_root]
        while len(stack) > 0:
            current_object = stack[0]
            stack.pop(0)
            if type(current_object) == Button:
                buttons.append(current_object)
            elif type(current_object) == TextInput:
                text_input.append(current_object)
            else:
                stack += current_object.children[:]
        self.iterable_list = buttons + text_input
        self.current_butt = 0
        self.initial_focus()

    def initial_focus(self):
        # initial focus, current_butt should be 0 here
        self.focus_button(self.iterable_list[self.current_butt])

    def rotate_buttons(self, keyboard, key,  *args):
        merged_list = self.iterable_list
        current_element = merged_list[self.current_butt]
        if key == 9:
            if type(current_element) == TextInput:
                if current_element.focus:
                    return
            previous_element = current_element
            if len(args[-1]) > 0:
                print args[-1][0]
                if args[-1][0] == "shift":
                    print "Going back"
                    if self.current_butt > 0:
                        self.current_butt -= 1
                    else:
                        self.current_butt = len(merged_list) - 1
            else:
                if self.current_butt < len(merged_list) - 1:
                        self.current_butt += 1
                else:
                    self.current_butt = 0
            current_element = merged_list[self.current_butt]
            if type(current_element) == TextInput:
                current_element.focus = True
                if type(previous_element) == Button:
                    self.unfocus_button(previous_element)
            elif type(current_element) == Button:
                self.unfocus_button(previous_element)
                self.focus_button(current_element)
            else:
                print "Error: Object neither Button nor TextInput"
        if key == 13:
            if type(current_element) != TextInput:
                self.unfocus_button(current_element)
                current_element.trigger_action(duration=0)

    @staticmethod
    def focus_button(butt):
        old_bg = butt.background_normal
        new_bg = old_bg[0:-4] + "_focus.png"
        if old_bg != "atlas://data/images/defaulttheme/button":
            butt.background_normal = new_bg

    @staticmethod
    def unfocus_button(butt):
        orig_bg = butt.background_normal.replace("_focus", "")
        butt.background_normal = orig_bg

    def detect_collision(self, _):
        pos = Window.mouse_pos
        widget_found = False
        # print pos
        for widget in self.iterable_list:
            changed = False
            rel_pos = widget.to_widget(pos[0], pos[1], False)
            # print rel_pos
            if widget.collide_point(rel_pos[0], rel_pos[1]):
                widget_found = True
                # print "Colliding"
                if (self.previous_mouse_position == widget) and not self.tooltip_active:
                    tp = ToolTip(text=widget.tooltip)
                    widget.add_widget(tp)
                    self.tooltip_active = True
                    changed = True
                elif (self.previous_mouse_position == widget) and self.tooltip_active:
                    self.tooltip_active = True
                    changed = True
                elif (self.previous_mouse_position != widget) and self.tooltip_active:
                    self.tooltip_active = False
                    self.previous_mouse_position = widget
                else:
                    self.previous_mouse_position = widget
            if not changed:
                widget.clear_widgets()
        if not widget_found:
            self.previous_mouse_position = None

# Cases of collisions:
# 1. The collided widget is the same as the previous one and has no tooltip displayed -> display tooltip
# 2. The collided widget is the same as the previous one and has a tooltip displayed -> change nothing
# 3. The collided widget is not the same as the previous one and a tooltip is still being displayed
# -> remove tooltip, edit previous one
# 4. The collided widget is not the same as the previous one, no tooltip displayed -> edit previous one