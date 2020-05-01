class Level:
    def __init__(self, n_cols, n_lines):
        self.n_cols = n_cols
        self.n_lines = n_lines
        self.grid = [['0'] * n_cols for k in range(n_lines)]

    def setGridFromFile(self, path):
        with open(path) as f:
            lines = f.readlines()
            num_lines_file = len(lines)
            assert(num_lines_file == self.n_lines)

            for i in range(num_lines_file):
                line = lines[i].replace('\n', '')
                num_cols_file = len(line)
                assert(num_cols_file == self.n_cols)
                for j in range(num_cols_file):
                    self.grid[i][j] = str(line[j])

    def hasAppleOn(self, pos):
        return self.grid[pos[0]][pos[1]].startswith('p')

    def destroyAppleOn(self, pos):
        self.grid[pos[0]][pos[1]] = '0'

    def getSnakePos(self, snake):
        for i in range(self.n_lines):
            for j in range(self.n_cols):
                if self.grid[i][j].startswith('s'):
                    self.grid[i][j] = '0'
        self.grid[snake.head.pos[0]][snake.head.pos[1]] = 's1'
        for part in snake.body:
            self.grid[part.pos[0]][part.pos[1]] = 's'

    def showGrid(self):
        print("-----GRID-----")
        for line in self.grid:
            print(line)