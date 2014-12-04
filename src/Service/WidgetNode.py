__author__ = 'grafgustav'


class WidgetNode:

    def __init__(self, parent=None, content=None):
        self.parent = parent
        self.content = content
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def remove_child(self, node):
        self.children.remove(node)

    def get_children(self):
        return self.children

    def set_content(self, con):
        self.content = con

    def get_content(self):
        return self.content
