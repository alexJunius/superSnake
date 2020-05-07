import kivy

kivy.require('1.11.1')  # update with your current version

from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

# import the kivy elements used by our classes
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

from levelObjects import snake, level


class Background(Widget):
    floor_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #Create textures
        self.floor_texture = Image(source="img/floor.png").texture
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)


class MainApp(App):
    def on_start(self):
        # Init level object and draw everything
        self.level = level.Level('levels/level1.txt')  # Create matrix on init
        self.walls = self.level.create_walls()
        self.apples = [] #self.level.draw_apples()
        self.snake = self.level.create_snake()  # draw and return snake object
        self.draw_everything()

    def draw_everything(self):
        for elt in self.walls:
            self.root.add_widget(elt)
        for elt in self.apples:
            self.root.add_widget(elt)
        self.snake.draw_snake()
        self.root.add_widget(self.snake.head)
        for elt in self.snake.body:
            self.root.add_widget(elt)
        print('done')


if __name__ == '__main__':
    MainApp().run()
