import kivy
kivy.require('1.11.1')  # update with your current version

# import the kivy elements used by our classes
from kivy.app import App
from kivy.uix.screenmanager import Screen

class WelcomeScreen(Screen):
    pass

class SnakeApp(App):
    pass

if __name__ == '__main__':
    SnakeApp().run()