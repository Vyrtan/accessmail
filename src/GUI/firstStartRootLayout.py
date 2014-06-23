from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from GUI.firstStartLayout import FirstStartLayout
from GUI.providerDataLayout import ProviderDataLayout


class RootWidget(BoxLayout):

    def selectedProvider(self, provider):
        print(provider)
        self.clear_widgets()
        self.add_widget(ProviderDataLayout(provider))


class FirstStartRootApp(App):

    def build(self):
        root = RootWidget()

        Window.clearcolor = (1, 1, 1, 1)

        root.add_widget(FirstStartLayout())

        root.killMe = self.killMe

        return root

    def killMe(self):
        self.stop()

if __name__ == '__main__':
    FirstStartRootApp().run()

