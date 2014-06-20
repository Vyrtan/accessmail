from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from GUI.firstStartLayout import FirstStartLayout
from GUI.providerDataLayout import ProviderDataLayout


class RootWidget(BoxLayout):


    def selectedProvider(self, provider):
        print(provider)
        self.clear_widgets()
        self.add_widget(ProviderDataLayout())


class FirstStartRootApp(App):

    def build(self):
        root = RootWidget()

        root.add_widget(FirstStartLayout())

        return root

if __name__ == '__main__':
    FirstStartRootApp().run()

