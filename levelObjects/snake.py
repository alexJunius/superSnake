from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ObjectProperty
from kivy.core.window import Window

class SnakePart(Widget):
    imagePath = ObjectProperty(None)

    def __init__(self, xGrid, yGrid, num_lines, num_cols):
        super().__init__()
        self.nCols = num_cols
        self.nLines = num_lines
        self.x_grid = xGrid
        self.y_grid = yGrid
        self.x = Window.width / num_cols * xGrid
        self.y = Window.height / num_lines * yGrid
        self.size = Window.width / num_cols, Window.height / num_lines

    def update_coord(self):
        self.x = Window.width / self.nCols * self.x_grid
        self.y = Window.height / self.nLines * self.y_grid


class Snake:
    def __init__(self, positionsInit, nLines, nCols):
        self.nLines = nLines
        self.nCols = nCols
        self.head = SnakePart(positionsInit[0][0], positionsInit[0][1], nLines, nCols)
        self.body = [SnakePart(elt[0], elt[1], nLines, nCols) for elt in positionsInit[1:]]
        self.moving = False
        self.direction = None

    def move_dir(self, direction, level, app):
        self.direction = direction
        oldPosHeadGrid = [self.head.x_grid, self.head.y_grid]
        self.head.x_grid += (-1)*(direction=='left') + 1*(direction=='right')
        self.head.y_grid += (-1)*(direction=='down') + 1*(direction=='up')
        self.head.update_coord()
        posHeadGrid = [self.head.x_grid, self.head.y_grid]
        if level.has_apple_on(posHeadGrid):
            print("Apple found !")
            level.destroy_apple_on(posHeadGrid, app)
            self.grow(app)
        self.update_body(oldPosHeadGrid)
        self.draw_snake()

    def grow(self, app):
        new_elt = SnakePart(self.body[-1].x_grid, self.body[-1].y_grid, self.nLines, self.nCols)
        app.root.add_widget(new_elt)
        self.body.append(new_elt)

    def update_body(self, oldPosHeadGrid):
        new_body_pos = [oldPosHeadGrid]
        for elt in self.body[:-1]:
            new_body_pos.append([elt.x_grid, elt.y_grid])
        for new_pos, old_part in zip(new_body_pos, self.body):
            old_part.x_grid, old_part.y_grid = new_pos
            old_part.update_coord()

    def move(self, direction, level, app):
        headpos = int(self.head.x_grid), int(self.head.y_grid)
        if direction == "up" and not self.direction=="down":
            if not headpos[0] == 0 and not level.grid[headpos[0]][headpos[1] + 1] in ['s', 'm']:
                self.move_dir(direction, level, app)
            else: self.moving = False

        elif direction=="down" and not self.direction == "up":
            if not headpos[0] == level.n_cols-1 and not level.grid[headpos[0]][headpos[1] - 1] in ['s', 'm']:
                self.move_dir(direction, level, app)
            else: self.moving = False

        elif direction=="left" and not self.direction == "right":
            if not headpos[1] == 0 and not level.grid[headpos[0] - 1][headpos[1]] in ['s', 'm']:
                self.move_dir(direction, level, app)
            else: self.moving = False

        elif direction =="right" and not self.direction == "left":
            if not headpos[1] == level.n_lines-1 and not level.grid[headpos[0] + 1][headpos[1]] in ['s', 'm']:
                self.move_dir(direction, level, app)
            else: self.moving = False

        else:
            print("Wrong direction")
            self.moving = False
        level.get_snake_pos(self)


    def draw_snake(self):
        self.update_head_widget()
        self.update_body_widgets()
        # for elt in [self.head] + self.body:
        #     app.root.add_widget(elt)

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
