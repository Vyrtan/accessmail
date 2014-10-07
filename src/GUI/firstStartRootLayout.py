from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from GUI.firstStartLayout import FirstStartLayout
from GUI.providerDataLayout import ProviderDataLayout


class RootWidget(BoxLayout):
    '''
    This class is the controller level to choose the currently used e-mail provider.
    So far only two providers are being supported, however, future patches intent to add
    further support for more providers.

    '''

    def selected_provider(self, provider):
        '''
        This method takes the selected provider, hands it to the next class, which processes the
        login information.

        :param provider:
        :return:
        '''
        self.clear_widgets()
        self.add_widget(ProviderDataLayout(provider))


class FirstStartRootApp(App):
    '''
    This class is the App which is started, if the program has not been started before and the
    database is empty.
    '''

    def build(self):
        '''
        This method builds the Application. It is an essential part of the kivy framwork and is
        responsible for displaying the created widgets/Layouts.

        :return:
        '''
        root = RootWidget()

        Window.clearcolor = (1, 1, 1, 1)

        root.add_widget(FirstStartLayout())

        root.killMe = self.kill_me

        return root

    def kill_me(self):
        self.stop()

if __name__ == '__main__':
    FirstStartRootApp().run()

