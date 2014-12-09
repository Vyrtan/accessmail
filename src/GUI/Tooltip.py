from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics import Color
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.uix.label import Label

__author__ = 'grafgustav'


class ToolTip(Label):
    #default properties
    #text property, default property value "Click to edit"
    text = StringProperty("Default Tooltip")
    #text color as list, rgba value default black with 100% opacity
    color = ListProperty([0, 0, 0, 1])
    bold = BooleanProperty(True)
    font_size = NumericProperty(20)
    #background colour as an rgb list,value default yellow
    background = ListProperty([1, 1, 0.1])

    #initialise tooltip label
    def __init__(self, **kwargs):
        super(ToolTip, self).__init__(**kwargs)
        # set position at current mouse cursor position
        self.pos = (Window.mouse_pos[0], Window.mouse_pos[1])
        # update the texture value of the widget
        self.texture_update()
        # set the size of the label to that of the text
        self.size = self.texture_size
        # draw the label background
        with self.canvas.before:
            #set the label background color to the background property as rgb list color
            #sure there must be a better method than this but it works
            Color(self.background[0], self.background[1], self.background[2])
            #draw in the background rectangle
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)