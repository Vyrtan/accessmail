import kivy
kivy.require('1.7.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

Builder.load_file('writelayout.kv')
Builder.load_file('readlayout.kv')
Builder.load_file('menuLayout.kv')
Builder.load_file('overviewLayout.kv')
Builder.load_file('addressLayout.kv')


class ReadLayout(Screen):
    pass


class MenuLayout(Screen):
    pass


class WriteLayout(Screen):
    pass


class OverviewLayout(Screen):
    pass


class AddressLayout(Screen):
    pass


sm = ScreenManager()
sm.add_widget(WriteLayout(name='write'))
sm.add_widget(ReadLayout(name='read'))
sm.add_widget(OverviewLayout(name='overview'))
sm.add_widget(AddressLayout(name='address'))


class MainApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MainApp().run()