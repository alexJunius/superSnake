from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ObjectProperty


class SnakePart(Widget):
    nCols = NumericProperty(1)
    nLines = NumericProperty(1)
    x_grid = NumericProperty(1)
    y_grid = NumericProperty(1)
    imagePath = ObjectProperty(None)

    def __init__(self, xGrid, yGrid, num_lines, num_cols):
        super().__init__()
        self.nCols = num_cols
        self.nLines = num_lines
        self.x_grid = xGrid
        self.y_grid = yGrid


class Snake:
    def __init__(self, positionsInit, nLines, nCols):
        self.head = SnakePart(positionsInit[0][0], positionsInit[0][1], nLines, nCols)
        self.body = [SnakePart(elt[0], elt[1], nLines, nCols) for elt in positionsInit[1:]]
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

    def move(self, level):
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

    def draw_snake(self):
        self.update_head_widget()
        self.update_body_widgets()
        # for elt in [self.head] + self.body:
        #     app.root.add_widget(elt)
        # print(app.level.grid)

    def update_head_widget(self):
        bx, by = self.body[0].x_grid, self.body[0].y_grid
        hx, hy = self.head.x_grid, self.head.y_grid
        self.head.imagePath = "img/head_" + "left"*int(hx==bx-1) + "right"*int(hx==bx+1) + "down"*int(hy==by-1) + \
                           "up"*int(hy==by+1) +".png"
        return self.head

    def update_body_widgets(self):
        head_body = [self.head] + self.body
        for i in range(1, len(head_body) - 1):
            b0x, b0y = head_body[i-1].x_grid, head_body[i-1].y_grid
            b1x, b1y = head_body[i].x_grid, head_body[i].y_grid
            b2x, b2y = head_body[i+1].x_grid, head_body[i+1].y_grid
            head_body[i].imagePath = "img/body_" + \
                                  "left_down"*int((b1x==b0x+1 and b1y==b2y+1) or (b1x==b2x+1 and b1y==b0y+1)) + \
                                  "left_right"*int((b1x==b0x+1 and b1x==b2x-1) or (b1x==b2x+1 and b1x==b0x-1)) + \
                                  "left_up"*int((b1x==b0x+1 and b1y==b2y-1) or (b1x==b2x+1 and b1y==b0y-1)) + \
                                  "right_down"*int((b1x==b0x-1 and b1y==b2y+1) or (b1x==b2x-1 and b1y==b0y+1)) + \
                                  "right_up"*int((b1x==b0x-1 and b1y==b2y-1) or (b1x==b2x-1 and b1y==b0y-1)) + \
                                  "up_down"*int((b1y==b0y-1 and b1y==b2y+1) or (b1y==b2y-1 and b1y==b0y+1)) + ".png"
        bx, by = head_body[-2].x_grid, head_body[-2].y_grid
        tx, ty = head_body[-1].x_grid, head_body[-1].y_grid
        self.body[-1].imagePath = "img/tail_" + "left"*int(tx==bx+1) + "right"*int(tx==bx-1) + "down"*int(ty==by+1) + \
                               "up"*int(ty==by-1) +".png"
        return self.body
