import kivy
kivy.require('1.11.1')  # update with your current version

# import the kivy elements used by our classes
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager

from levelObjects import snake, level

class Matrix(Widget)
    def __init__(self):
        super().__init__()

    def generateLevel(self):
        self.lvl1 = level.Level(10, 10)
        self.lvl1.setGridFromFile('levels/level1.txt')
        positionsInit = [[1, 8], [1, 7], [1, 6], [1, 5]]
        snakeObj = snake.Snake(positionsInit)
        self.lvl1.getSnakePos(snakeObj)
        self.lvl1.showGrid()
        while True:
            snakeObj.direction = input('Direction : ')
            print(snakeObj.direction)
            snakeObj.moving = True
            while snakeObj.moving:
                snakeObj.move(self.lvl1)
                self.lvl1.getSnakePos(snakeObj)
                self.lvl1.showGrid()



class SnakeApp(App):

    def build(self):
        return(Matrix)

if __name__ == '__main__':
    SnakeApp().run()