from pygamii.scene import BaseScene
from pygamii.objects import Object
from pygamii.action import BaseKeyboard, MoveAction

import os
import random

class Scene(BaseScene):
    particles = 50
    def __init__(self, *args, **kwargs):
        super(Scene, self).__init__(*args, **kwargs)
        self.cols, self.rows = self.get_terminal_size()
        self.rows -= 1

        self.add_action(Keyboard())

        for i in range(self.particles):
            ball = Ball()
            ball.x = random.randrange(self.cols-10)
            ball.y = random.randrange(self.rows-5)
            ball.color = random.choice(["red","green","blue","yellow","cyan","white","magenta"])
            ball.dx = random.randint(0,3)
            ball.dy = random.randint(1,2)
            ball.x_rbound = self.cols
            ball.y_lbound = self.rows
            self.add_action(MoveAction(ball))
            self.add_object(ball)


        help_tip = Tip()
        help_tip.y = self.rows
        self.add_object(Tip())

class Ball(Object):
    width = 1
    height = 1
    x = 0
    y = 0
    dx = 2
    dy = 2
    x_lbound = 1
    y_ubound = 1
    x_rbound = 0
    y_lbound = 0
    gravity = 1
    speed = 12
    started = True
    color = "white"
    char = "#"

    def in_move(self):
        return self.started

    def move(self):
        self.dy += self.gravity
        self.y += self.dy
        self.x += self.dx

        if self.y >= self.y_lbound-3:
            self.dy *= -1
        if self.x >= self.x_rbound-3:
            self.dx *= -1
        if self.x <= self.x_lbound:
            self.dx *= -1
        if self.y <= self.y_lbound//2+(self.y_lbound//2)//2:
            self.gravity = 1
        else:
            self.gravity = 0

    def on_collision(self, obj):
        if isinstance(obj, Ball):
            self.dx, obj.dx = obj.dx, self.dx
            self.dy, obj.dy = obj.dy, self.dy

class Tip(Object):
    char = "Press q to quit"
    color = "white"

class Keyboard(BaseKeyboard):
    def handler(self, key):
        if key == ord('q'):
            self.scene.stop()
            os._exit(0)

if __name__ == '__main__':
    scene = Scene()
    scene.start()