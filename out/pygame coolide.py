import math
import sys
import threading
import time

import pygame
import cv2
import mediapipe as mp
from numpy import ceil

pygame.init()
width, height = 800, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("YES")
i = 0
while True:

    window.fill((29, 39, 39))

    s = pygame.draw.rect(window, (0, 70, 0), ((width / 4), (height / 4), (width / 2), (height / 2)))
    pygame.transform.rotate(s, i)
    print(i)
    i += 1
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("quit")

            print("quit")
            cv2.destroyAllWindows()
            print("quit")

            print("quit")
            pygame.quit()
            print("quit")
            sys.exit()
