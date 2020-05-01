from levelObjects.level import Level
from levelObjects.snake import Snake

if __name__ == '__main__':
    lvl1 = Level(10, 10)
    lvl1.setGridFromFile('levels/level1.txt')
    positionsInit = [[1, 8],
                     [1, 7],
                     [1, 6],
                     [1, 5]]
    snake = Snake(positionsInit)
    lvl1.getSnakePos(snake)
    lvl1.showGrid()
    while True:
        snake.direction = input('Direction : ')
        print(snake.direction)
        snake.moving = True
        while snake.moving:
            snake.move(lvl1)
            lvl1.getSnakePos(snake)
            lvl1.showGrid()
