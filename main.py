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
from kivy.clock import Clock

from levelObjects.level import Level
from levelObjects.snake import Snake, SnakePart
from functools import partial


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
        self.level = Level('levels/level1.txt')  # Create matrix on init
        self.walls = self.level.create_walls()
        self.apples = self.level.create_apples()
        self.snake = self.level.create_snake()  # draw and return snake object
        self.draw_everything()

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def draw_everything(self):
        for elt in self.walls:
            self.root.add_widget(elt)
        for elt in self.apples:
            self.root.add_widget(elt)
        self.snake.draw_snake()
        self.root.add_widget(self.snake.head)
        for elt in self.snake.body:
            self.root.add_widget(elt)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if not self.snake.moving:
            self.snake.moving = True
            self.key = keycode[1]
            self.clock = Clock.schedule_interval(partial(self.move_snake, keycode[1]), 1/60.)

    def move_snake(self, direction, dt):
        if self.snake.moving:
            self.snake.move(direction, self.level, self)
        else:
            self.clock.cancel()


if __name__ == '__main__':
    MainApp().run()
