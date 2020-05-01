from levelObjects.level import Level


class SnakePart:
    def __init__(self, x, y, sprite=None):
        self.pos = [x, y]
        self.sprite = sprite


class Snake:
    def __init__(self, positionsInit):
        self.head = SnakePart(positionsInit[0][0], positionsInit[0][1])
        self.body = [SnakePart(elt[0], elt[1]) for elt in positionsInit[1:]]
        self.moving = False
        self.direction = None

    def move_up(self):
        self.update_body()
        self.head.pos[0] -= 1

    def move_down(self):
        self.update_body()
        self.head.pos[0] += 1

    def move_left(self):
        self.update_body()
        self.head.pos[1] -= 1

    def move_right(self):
        self.update_body()
        self.head.pos[1] += 1

    def update_body(self):
        new_body_pos = [self.head.pos.copy()]
        for elt in self.body[:-1]:
            new_body_pos.append(elt.pos.copy())
        for new_pos, old_part in zip(new_body_pos, self.body):
            old_part.pos = new_pos

    def move(self, level: Level):
        headpos = self.head.pos
        print('Moving')
        if self.direction == "up":
            if not headpos[0] == 0 and not level.grid[headpos[0] - 1][headpos[1]] in ['s', 'm']:
                self.move_up()
                if level.hasAppleOn(self.head.pos):
                    level.destroyAppleOn(self.head.pos)
            else:
                self.moving = False

        elif self.direction == "down":
            if not headpos[0] == level.n_lines-1 and not level.grid[headpos[0] + 1][headpos[1]] in ['s', 'm']:
                self.move_down()
                if level.hasAppleOn(self.head.pos):
                    level.destroyAppleOn(self.head.pos)
            else:
                self.moving = False

        elif self.direction == "left":
            if not headpos[1] == 0 and not level.grid[headpos[0]][headpos[1] - 1] in ['s', 'm']:
                self.move_left()
                if level.hasAppleOn(self.head.pos):
                    level.destroyAppleOn(self.head.pos)
            else:
                self.moving = False

        elif self.direction == "right":
            if not headpos[1] == level.n_cols-1 and not level.grid[headpos[0]][headpos[1] + 1] in ['s', 'm']:
                self.move_right()
                if level.hasAppleOn(self.head.pos):
                    level.destroyAppleOn(self.head.pos)
            else:
                self.moving = False

        else:
            print("Wrong direction")
            self.moving = False
