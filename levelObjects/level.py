from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

from levelObjects.snake import Snake, SnakePart


def set_grid_from_file(path):
    with open(path) as f:
        lines = f.readlines()
        lines.reverse()
        n_lines = len(lines)
        n_cols = len(lines[0].replace('\n', ''))
        grid = [['0'] * n_cols for _ in range(n_lines)]

        for i in range(n_lines):
            line = lines[i].replace('\n', '')
            for j in range(n_cols):
                grid[i][j] = str(line[j])
    return grid, n_lines, n_cols

class Wall(Widget):
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
        self.snake = None

    def has_apple_on(self, pos):
        return self.grid[pos[0]][pos[1]].startswith('p')

    def destroy_apple_on(self, pos):
        self.grid[pos[0]][pos[1]] = '0'

    def show_grid(self):
        print("-----GRID-----")
        for line in self.grid:
            print(line)

    def create_walls(self):
        nLines = self.n_lines
        nCols = self.n_cols

        for i in range(self.n_lines):
            for j in range(self.n_cols):
                if self.grid[i][j] == 'm':
                    self.walls.append(Wall(nLines, nCols, j, i))
        return self.walls

    def create_snake(self):
        nLines = self.n_lines
        nCols = self.n_cols
        positions_init = []

        for i in range(self.n_lines):
            for j in range(self.n_cols):
                if self.grid[i][j] == 's':
                    positions_init.append([j, i])

        self.snake = Snake(positions_init, nLines, nCols)

        return self.snake