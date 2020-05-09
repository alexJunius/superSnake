from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty

from levelObjects.snake import Snake, SnakePart
from random import randint

def set_grid_from_file(path):
    with open(path) as f:
        lines = f.readlines()
        lines.reverse()
        n_lines = len(lines)
        n_cols = len(lines[0].replace('\n', ''))
        grid = [['0'] * n_lines for _ in range(n_cols)]

        for i in range(n_lines):
            line = lines[i].replace('\n', '')
            for j in range(n_cols):
                grid[j][i] = str(line[j])
    return grid, n_lines, n_cols

class Wall(Widget):
    nCols = NumericProperty(1)
    nLines = NumericProperty(1)
    x_grid = NumericProperty(1)
    y_grid = NumericProperty(1)
    imagePath = ObjectProperty(None)

    def __init__(self, num_lines, num_cols, xGrid, yGrid):
        super().__init__()
        self.nCols = num_cols
        self.nLines = num_lines
        self.x_grid = xGrid
        self.y_grid = yGrid
        self.imagePath = "img/wall_{}.png".format(randint(1,5))

class Apple(Widget):
    nCols = NumericProperty(1)
    nLines = NumericProperty(1)
    x_grid = NumericProperty(1)
    y_grid = NumericProperty(1)

    def __init__(self, num_lines, num_cols, xGrid, yGrid):
        super().__init__()
        self.nCols = num_cols
        self.nLines = num_lines
        self.x_grid = xGrid
        self.y_grid = yGrid


class Level:
    def __init__(self, path):
        self.grid, self.n_lines, self.n_cols = set_grid_from_file(path)
        self.walls = []
        self.apples = []
        self.snake = None

    def has_apple_on(self, pos):
        return self.grid[pos[0]][pos[1]] == 'a'

    def destroy_apple_on(self, pos, app):
        self.grid[pos[0]][pos[1]] = '0'
        for elt in self.apples:
            if elt.x_grid == pos[0] and elt.y_grid == pos[1]:
                print('Apple destroyed !')
                app.root.remove_widget(elt)

    def show_grid(self):
        print("-----GRID-----")
        for line in self.grid:
            print(line)

    def get_snake_pos(self, snake):
        for i in range(self.n_cols):
            for j in range(self.n_lines):
                if self.grid[i][j].startswith('s'):
                    self.grid[i][j] = '0'
        self.grid[snake.head.x_grid][snake.head.y_grid] = 's'
        for part in snake.body:
            self.grid[part.x_grid][part.y_grid] = 's'

    def create_walls(self):
        nLines = self.n_lines
        nCols = self.n_cols

        for i in range(self.n_cols):
            for j in range(self.n_lines):
                if self.grid[i][j] == 'm':
                    self.walls.append(Wall(nLines, nCols, i, j))
        return self.walls


    def create_apples(self):
        nLines = self.n_lines
        nCols = self.n_cols

        for i in range(self.n_cols):
            for j in range(self.n_lines):
                if self.grid[i][j] == 'a':
                    self.apples.append(Apple(nLines, nCols, i, j))
        return self.apples

    def create_snake(self):
        nLines = self.n_lines
        nCols = self.n_cols
        positions_init = []

        for i in range(self.n_cols):
            for j in range(self.n_lines):
                if self.grid[i][j] == 's':
                    positions_init.append([i, j])

        self.snake = Snake(positions_init, nLines, nCols)

        return self.snake