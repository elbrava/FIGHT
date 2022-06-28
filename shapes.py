import cv2
import pygame.draw
from numpy import cos, sin

pygame.init()
win = pygame.display.set_mode((800, 800))
im = cv2.VideoCapture(0)
_, mask = im.read()
h, w = 800, 800
r = 80
points = [[(w / 2) + i, (h / 2) + r * sin(i/30)] for i in range(400)]
print(points)
m = cv2.circle(mask, (w // 2, h // 2), 60, (0, 90, 90), -1)
# m = cv2.polylines(mask, [1, 1], isClosed=True, color=(0, 90, 90))
"""m = cv2.polylines(mask, points, True, (0, 79, 90))"""
cv2.imshow("m", m)
points.remove(points[-1])
pygame.draw.polygon(win, (0, 90, 90), points)
while True:
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
