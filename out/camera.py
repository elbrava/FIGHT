import pygame
import pymunk
from pymunk import pygame_util

pygame.init()

W, H = 800, 800
screen = pygame.display.set_mode((W, H))
space = pymunk.Space()
draw_options = pygame_util.DrawOptions(screen)
translation = pymunk.Transform()
scaling = 1
rotation = 0
clockgit  = pygame.time.Clock()
running = True
while True:
    for event in pygame.event.get():
        if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
        ):
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pygame.image.save(screen, "camera.png")

    keys = pygame.key.get_pressed()
    left = int(keys[pygame.K_LEFT])
    up = int(keys[pygame.K_UP])
    down = int(keys[pygame.K_DOWN])
    right = int(keys[pygame.K_RIGHT])

    zoom_in = int(keys[pygame.K_a])
    zoom_out = int(keys[pygame.K_z])
    rotate_left = int(keys[pygame.K_s])
    rotate_right = int(keys[pygame.K_x])

    translate_speed = 10
    translation = translation.translated(
        translate_speed * left - translate_speed * right,
        translate_speed * up - translate_speed * down,
    )

    zoom_speed = 0.1
    scaling *= 1 + (zoom_speed * zoom_in - zoom_speed * zoom_out)

    rotation_speed = 0.1
    rotation += rotation_speed * rotate_left - rotation_speed * rotate_right

    # to zoom with center of screen as origin we need to offset with
    # center of screen, scale, and then offset back
    draw_options.transform = (
            pymunk.Transform.translation(300, 300)
            @ pymunk.Transform.scaling(scaling)
            @ translation
            @ pymunk.Transform.rotation(rotation)
            @ pymunk.Transform.translation(-300, -300)
    )
    screen.fill(pygame.Color("white"))

    # ## Draw stuff
    space.debug_draw(draw_options)

    dt = 1.0 / 60.0
    space.step(dt)
    ### Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
