import math

import pymunk  # Import pymunk..

import pygame
from pymunk import pygame_util

pygame.init()
W, H = 800, 800
win = pygame.display.set_mode((W, H))

increment = 1
lshape = ""

rotatation = 300


def add_line(space):
    global lshape
    global increment
    for i in range(-increment, W + -increment):
        x1 = i
        y1 = 500 + int(math.sin(i / 300) * 70)

        x = i + 1
        y = 500 + int(math.sin(x / 300) * 70)
        lshape = pymunk.Segment(space.static_body, (x1 + increment, y1), (x + increment, y), radius=1)
        lshape.friction = 0.5
        lshape.elasticity = 0.7
        lshape.density = 100000000
        lshape.mass = 90

        lshape.color = pygame.Color("red")

        space.add(lshape)
        win.fill((255, 255, 255))
        print(i)
        print(int(math.sin(i / 300)))
    # print(H - math.sin(i / 300))


def add_object(space, radius, mass):
    body = pymunk.Body()
    shape = pymunk.Circle(body, radius)
    body.position = (W / 2, H / 2)
    shape.mass = mass
    shape.density = 1
    shape.elasticity = 0.4

    shape.color = (245, 34, 45, 100)
    space.add(body, shape)
    return shape


def draw(space, window, draw_options):
    window.fill((255, 255, 255))
    space.debug_draw(draw_options)


def run_main(window, w, h):
    global increment
    run = True
    fps = 60
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0, 981)
    ball = add_object(space, 30, 100)

    draw_op = pygame_util.DrawOptions(win)

    while run:
        window.fill((255, 255, 255))
        add_line(space)
        draw(space, win, draw_op)
        space.step(1 / 60)
        clock.tick(fps)
        increment -= 3
        for i in space.shapes:
            if type(i) == pymunk.shapes.Segment:
                space.remove(i)
        ball.body.angle += 1
        pygame.display.update()
        print(increment)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                break


if __name__ == '__main__':
    run_main(win, W, H)
