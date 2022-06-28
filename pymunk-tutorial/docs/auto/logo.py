"""Program used to generate the logo animation on the pymunk main page.

This program will showcase several features of Pymunk, such as collisions, 
debug drawing, automatic generation of shapes from images, motors, joints and
sleeping bodies.
"""

import pymunk.autogeometry
import pymunk.pygame_util
from pymunk import Vec2d
import pymunk
from pygame.locals import *
import pygame
import random
random.seed(5)  # keep the random factor the same each run.

fps = 60.0
pygame.init()
size = 690, 300
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

clock.tick(1/5.)

# Physics stuff
space = pymunk.Space()
space.gravity = 0, 900
space.sleep_time_threshold = 0.3

draw_options = pymunk.pygame_util.DrawOptions(screen)
pymunk.pygame_util.positive_y_is_up = False

# Generate geometry from pymunk logo image
logo_img = pygame.image.load("pymunk_logo.png")
w, h = logo_img.get_size()
logo_bb = pymunk.BB(0, 0, w, h)

def sample_func(point):
    try:
        p = pymunk.pygame_util.to_pygame(point, logo_img)
        color = logo_img.get_at(p)

        return color.a
    except:
        return 0

line_set = pymunk.autogeometry.PolylineSet()

def segment_func(v0, v1):
    line_set.collect_segment(v0, v1)


pymunk.autogeometry.march_soft(
    logo_bb, w, h, 99,
    segment_func,
    sample_func)

r = 10
letter_group = 0
for line in line_set:
    line = pymunk.autogeometry.simplify_curves(line, .7)

    max_x = 0
    min_x = 1000
    max_y = 0
    min_y = 1000
    for l in line:
        max_x = max(max_x, l.x)
        min_x = min(min_x, l.x)
        max_y = max(max_y, l.y)
        min_y = min(min_y, l.y)
    w, h = max_x - min_x, max_y - min_y

    # we skip the line which has less than 35 height, since its the "hole" in
    # the p in pymunk, and we dont need it.
    # if h < 35:
    #     continue

    center = Vec2d(min_x + w/2., min_y + h/2.)
    t = pymunk.Transform(a=1.0, d=1.0, tx=-center.x, ty=-center.y)

    r += 30
    if r > 255:
        r = 0

    if True:
        for i in range(len(line)-1):
            shape = pymunk.Segment(space.static_body, line[i], line[i+1], 1)
            shape.friction = 0.5
            shape.color = (255, 0, 0, 0)
            space.add(shape)


floor = pymunk.Segment(space.static_body, (-100, 300), (1000, 220), 5)
floor.friction = 1.0
space.add(floor)


class Ball:
    def __init__(self, pos=(100, 100), radius=50, color=None):
        self.body = pymunk.Body()
        self.body.position = pos
        shape = pymunk.Circle(self.body, radius)
        shape.density = 0.01
        shape.friction = 1
        if color != None:
            shape.color = color
        space.add(self.body, shape)

class Poly:
    def __init__(self, pos, vertices, color=None):
        self.body = pymunk.Body()
        self.body.position = pos
        shape = pymunk.Poly(self.body, vertices)
        shape.density = 0.01
        shape.friction = 1
        if color != None:
            shape.color = color
        space.add(self.body, shape)

# events


def big_ball():
    ball = Ball(pos=(800, 100), radius=50, color=(255, 0, 0, 0))
    ball.body.apply_impulse_at_local_point((-10000, 0), (0, -1000))


def boxfloor():
    vs = [(-50, 30), (60, 22), (-50, 22)]
    color = 0, 0, 0, 0
    Poly((600, 50), vs, color)


box_y = 150


def box():
    global box_y

    mass = 10
    moment = pymunk.moment_for_box(mass, (40, 20))
    b = pymunk.Body(mass, moment)
    s = pymunk.Poly.create_box(b, (40, 20))
    s.friction = 1
    b.position = 600, box_y
    box_y -= 30
    space.add(b, s)


def car():
    pos = Vec2d(100, 200)

    wheel_color = 52, 219, 119
    shovel_color = 219, 119, 52
    mass = 100
    radius = 25
    moment = pymunk.moment_for_circle(mass, 20, radius)
    wheel1_b = pymunk.Body(mass, moment)
    wheel1_s = pymunk.Circle(wheel1_b, radius)
    wheel1_s.friction = 1.5
    wheel1_s.color = wheel_color
    space.add(wheel1_b, wheel1_s)

    mass = 100
    radius = 25
    moment = pymunk.moment_for_circle(mass, 20, radius)
    wheel2_b = pymunk.Body(mass, moment)
    wheel2_s = pymunk.Circle(wheel2_b, radius)
    wheel2_s.friction = 1.5
    wheel2_s.color = wheel_color
    space.add(wheel2_b, wheel2_s)

    mass = 100
    size = (50, 30)
    moment = pymunk.moment_for_box(mass, size)
    chassi_b = pymunk.Body(mass, moment)
    chassi_s = pymunk.Poly.create_box(chassi_b, size)
    space.add(chassi_b, chassi_s)

    vs = [(0, 0), (25, 45), (0, 45)]
    shovel_s = pymunk.Poly(chassi_b, vs, transform=pymunk.Transform(tx=85))
    shovel_s.friction = 0.5
    shovel_s.color = shovel_color
    space.add(shovel_s)

    wheel1_b.position = pos - (55, 0)
    wheel2_b.position = pos + (55, 0)
    chassi_b.position = pos + (0, -25)

    space.add(
        pymunk.PinJoint(wheel1_b, chassi_b, (0, 0), (-25, -15)),
        pymunk.PinJoint(wheel1_b, chassi_b, (0, 0), (-25, 15)),
        pymunk.PinJoint(wheel2_b, chassi_b, (0, 0), (25, -15)),
        pymunk.PinJoint(wheel2_b, chassi_b, (0, 0), (25, 15))
    )

    speed = 4
    space.add(
        pymunk.SimpleMotor(wheel1_b, chassi_b, speed),
        pymunk.SimpleMotor(wheel2_b, chassi_b, speed)
    )


def cannon():
    col = 219, 52, 152, 0
    impulse = Vec2d(-200000, 0)

    ball = Ball(pos=(700, 200), radius=15, color=col)
    ball.body.apply_impulse_at_local_point(impulse)


events = []
events.append((0.1, big_ball))
events.append((2, big_ball))
events.append((3.5, boxfloor))
for x in range(8):
    events.append((4+x*.2, box))
events.append((6.5, car))
events.append((8.5, cannon))

events.sort(key=lambda x: x[0])

SMALLBALL = pygame.USEREVENT + 1
pygame.time.set_timer(SMALLBALL, 100)

small_balls = 100
total_time = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        elif event.type == KEYDOWN:
            if event.key in (K_ESCAPE, K_q):
                running = False

        elif event.type == SMALLBALL:
            if small_balls <= 0:
                pygame.time.set_timer(SMALLBALL, 0)
            for x in range(10):
                small_balls -= 1
                pos = random.randint(100, 400), 0
                Ball(pos, 8)

    if len(events) > 0 and total_time > events[0][0]:
        time, func = events.pop(0)
        func()

    space.step(1./fps)

    screen.fill(Color('white'))
    space.debug_draw(draw_options)
    #screen.blit(logo_img, (0, 0))
    pygame.display.flip()

    dt = clock.tick(fps)
    total_time += dt/1000.

pygame.quit()