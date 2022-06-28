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
webcam = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions
count = 0
time_begin = time.perf_counter()
right_pointer_x = 0
right_pointer_y = 0
left_pointer_x = 0
left_pointer_y = 0
left_angle = 0
right_angle = 0
im = ""
right_closed = False
left_closed = False
left_edit = True
right_edit = True
speed = 0



def angle(li_st, points):
    x1, y1 = li_st[points[0]].x, li_st[points[0]].y
    x2, y2 = li_st[points[1]].x, li_st[points[1]].y
    x3, y3 = li_st[points[2]].x, li_st[points[2]].y

    return math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))


def pre_wok():
    while webcam.isOpened():
        success, frame = webcam.read()

        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            t1 = threading.Thread(target=work, args=[holistic, frame])
            t1.start()
            t1.join()
            cv2.imshow("dh", im)
            cv2.waitKey(1)


def work(holistic, frame):
    global height, width, right_closed, left_closed, left_edit, right_edit, speed, time_begin

    global count, left_angle, right_angle, right_pointer_x, right_pointer_y, left_pointer_x, left_pointer_y, im
    # Recolor Feed
    cx = 0
    cy = 0

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)
    # Make Detections
    results = holistic.process(image)
    # print(results.face_landmarks)
    # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
    # Recolor image back to BGR for rendering

    # Draw face landmarks
    # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS)

    h, w, c = height, width, image.shape[-1]
    r = results.right_hand_landmarks
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    if results.right_hand_landmarks:
        # 5,9,13,17

        if r.landmark[9].y >= r.landmark[12].y:
            right_closed = False



        else:

            right_closed = True
        if right_closed and right_edit:
            x, y = [], []
            for i in [0, 5, 9, 13, 17]:
                x.append(r.landmark[i].x * w)
                y.append(r.landmark[i].y * h)
            cx = sum(x) / len(x)
            cy = sum(y) / len(y)
            right_pointer_x = cx
            right_pointer_y = cy
        print("right:", right_closed)

        cv2.circle(image, [int(cx), int(cy)], 3, (204, 34, 55), -1)

    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    l = results.left_hand_landmarks
    if results.left_hand_landmarks:
        # 5,9,13,17

        if l.landmark[9].y >= l.landmark[12].y:
            left_closed = False
        else:

            left_closed = True
        if left_closed and left_edit:
            x, y = [], []
            for i in [0, 5, 9, 13, 17]:
                x.append(l.landmark[i].x * w)
                y.append(l.landmark[i].y * h)
            cx = sum(x) / len(x)
            cy = sum(y) / len(y)
            cv2.circle(image, [int(cx), int(cy)], 3, (204, 34, 55), -1)
            left_pointer_x = cx
            left_pointer_y = cy
        print("left", left_closed)

    # Pose Detections
    p = results.pose_landmarks
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    if p:
        left = abs(angle(p.landmark, [14, 12, 24]))
        right = angle(p.landmark, [13, 11, 23])
        print("left:", int(left))
        print("RIGHT:", int(right))
        speed1 = (left - left_angle) / (time.perf_counter() - time_begin)
        if speed1 < 0: speed1 = 0
        speed2 = (right - right_angle) / (time.perf_counter() - time_begin)
        if speed2 < 0: speed2 = 0
        speed = speed1 + speed2
        left_angle = left
        right_angle = right
        time_begin = time.perf_counter()
    im = image
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)


def onrelease():
    global left_pointer_y, left_pointer_x, right_pointer_y, right_pointer_x, left_closed, right_closed, left_edit
    global right_edit, dart

    if not (int(left_pointer_x) == 0 and int(left_pointer_y) == 0):
        window.blit(dart, dart.get_rect(center=(int(left_pointer_x), int(left_pointer_y) + 35)))

        if not left_closed:
            left_edit = False

    if not (int(right_pointer_x) == 0 and int(right_pointer_y) == 0):
        window.blit(dart, dart.get_rect(center=(int(right_pointer_x), int(right_pointer_y) + 35)))
        if not right_closed:
            right_edit = False


t = threading.Thread(target=pre_wok)
t.start()
score = 0
while webcam.isOpened():

    window.fill((29, 39, 39))

    pygame.draw.circle(window, (0, 70, 0), (width / 2, height / 2), 350, 0)
    for x in [40, 60, 90, 130, 180, 240]:
        pygame.draw.circle(window, (0, 0, 70), (width / 2, height / 2), x, 1)
    pygame.draw.circle(window, (0, 0, 70), (width / 2, height / 2), 10, 0)
  
    onrelease()
    right_score = 350 - int(int((width / 2 - right_pointer_x) ** 2 + (height / 2 - right_pointer_y) ** 2) ** 0.5)
    if right_score < 0: right_score = 0
    left_score = 350 - int(int((width / 2 - left_pointer_x) ** 2 + (height / 2 - left_pointer_y) ** 2) ** 0.5)
    if left_score < 0: left_score = 0
    score = right_score + left_score
    print(speed)
    print(score)


    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("quit")
            webcam.release()
            print("quit")
            cv2.destroyAllWindows()
            print("quit")
            t.join()
            print("quit")
            pygame.quit()
            print("quit")
            sys.exit()
