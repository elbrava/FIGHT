import threading

import cv2
import pygame
import pymunk
from math import sin, cos
from pymunk import pygame_util

width = 800
height = 800
pygame.init()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("YES")

space = pymunk.Space()


class BODY:
    def __init__(self, spac, *args, **kwargs):
        self._b = pymunk.Body()
        self.size = 3
        self._core_rot = 0
        self.distance = 90
        self.point = [width // 4, height // 4]
        self._b.position = self.point
        x = self.point[1] + self.distance * cos(self._core_rot)
        y = self.point[0] + self.distance * sin(self._core_rot)
        b = [x, y]
        self._b1 = pymunk.Body()
        self.shape = pymunk.Segment(self._b, self.point, b, self.size)
        self.shape.color = pygame.Color("red")
        self.shape.friction = 0.5
        self.shape.elasticity = 0.7
        self.shape.mass = 90

        self._core_rot = 180
        self.distance = 90
        self.point = [width // 4, height // 4]
        self._b1.position = self.point
        x = self.point[1] + self.distance * cos(self._core_rot)
        y = self.point[0] + self.distance * sin(self._core_rot)
        b = [x, y]
        self.shape1 = pymunk.Segment(self._b1, self.point, b, self.size)
        self.shape1.color = pygame.Color("red")
        p = pymunk.PivotJoint(self._b, self._b1, (width // 4, height // 4))
        # pygame.draw.line(win, pygame.Color("red"), self.point, b, self.size)
        spac.add(p)

    def update(self):
        self.point = self._b.position
        self._core_rot = 180
        y = self.point[1] + self.distance * sin(self._core_rot)
        x = self.point[0] + self.distance * cos(self._core_rot)
        b = [x, y]
        self.shape = pymunk.Segment(self._b, self.point, b, self.size)
        space.add(self.shape)
        self.shape.color = pygame.Color("red")
        # pygame.draw.line(win, pygame.Color("red"), self.point, b, self.size)

    class LIMBS:
        pass


def draw(spac, window, draw_options):
    window.fill((255, 255, 255))
    spac.debug_draw(draw_options)


def run_main(window, w, h):
    run = True

    fps = 60
    clock = pygame.time.Clock()
    space.add(pymunk.Segment(space.static_body, (0, 700), (800, 700), 1))
    space.gravity = [60, 0]
    core = BODY(space)
    draw_op = pygame_util.DrawOptions(win)

    while run:
        window.fill((255, 255, 255))

        draw(space, win, draw_op)
        space.step(1 / fps)
        clock.tick(fps)
        # core.update()
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                break


run_main(win, width, height)
