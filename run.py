from pygamii.scene import BaseScene
from pygamii.objects import Object
from pygamii.action import BaseKeyboard, MoveAction

import os
import random

class Scene(BaseScene):
    particles = 50 # number of balls/particles
    def __init__(self, *args, **kwargs):
        super(Scene, self).__init__(*args, **kwargs)
        self.cols, self.rows = self.get_terminal_size() # screen space
        self.rows -= 1

        self.add_action(Keyboard())

        for i in range(self.particles):
            ball = Ball()
            ball.x = random.randrange(self.cols-10) # randomly distribute spawn location
            ball.y = random.randrange(self.rows-5)
            ball.color = random.choice(["red","green","blue","yellow","cyan","white","magenta"]) # colors
            ball.dx = random.randint(-3,3) # random x_axis acceleration
            ball.dy = random.randint(1,3) # random y_axis acceleration
            ball.x_rbound = self.cols # right bound, aka walls
            ball.y_lbound = self.rows # lower bound, aka walls
            self.add_action(MoveAction(ball)) # add it into action group
            self.add_object(ball) # append ball objects to game engine

        help_tip = Tip()
        help_tip.y = self.rows
        self.add_object(Tip()) # Press q to quit

class Ball(Object):
    width = 1 # ball size
    height = 1 # ball size
    x = 0 # see above scene()
    y = 0 # see above scene()
    dx = 2 # see above scene()
    dy = 2 # see above scene()
    x_lbound = 5 # x_axis left bound, aka wall
    y_ubound = 5# y_axis upper bound, aka wall, uncomment follwing commented line to use
    x_rbound = 0 # see above scene()
    y_lbound = 0 # see above scene()
    gravity = 1 # gravity
    speed = 13 # render speed, aka fps
    started = True
    color = "white" # see above scene()
    char = "#" # see above scene()

    def in_move(self):
        return self.started

    def move(self): # physics calculation
        self.dy += self.gravity
        self.y += self.dy
        self.x += self.dx

        if self.y >= self.y_lbound-5:
            self.dy *= -1
        # if self.y <= self.y_ubound: # uncomment this if you want upper bound
        #     self.dy *= -1
        if self.x >= self.x_rbound-5:
            self.dx *= -1
        if self.x <= self.x_lbound:
            self.dx *= -1
        if self.y <= self.y_lbound//2+(self.y_lbound//2)//2:
            self.gravity = 1
        else:
            self.gravity = 0

    def on_collision(self, obj): # check ball collision
        if isinstance(obj, Ball):
            if obj.dx == 0 :
                self.dx = obj.dx = self.dx//2 # collision speed transfer for stationary balls
            else:
                self.dx, obj.dx = obj.dx, self.dx # collision speed transfer
            self.dy, obj.dy = obj.dy, self.dy

class Tip(Object):
    char = "Press q to quit"
    color = "white"

class Keyboard(BaseKeyboard): # keyboard action
    def handler(self, key):
        if key == ord('q'):
            self.scene.stop()
            os._exit(0)

if __name__ == '__main__':
    scene = Scene()
    scene.start()