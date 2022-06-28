import math
import sys
import threading
import time

import cv2
import mediapipe as mp
import numpy as np
from cvzone import findContours
from numpy import ceil

width, height = 800, 800
webcam = cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mask_convex = np.zeros((webcam.read()[-1]).shape, np.uint8)
mask_z = mask_convex.copy()


def angle(li_st, points):
    x1, y1 = li_st[points[0]].x, li_st[points[0]].y
    x2, y2 = li_st[points[1]].x, li_st[points[1]].y
    x3, y3 = li_st[points[2]].x, li_st[points[2]].y

    return math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))


def draw_line(image, landmarks, connections):
    global mask_convex, mask_z
    mask_convex = np.zeros(image.shape, np.uint8)
    mask_z = mask_convex.copy()
    h, w, c = image.shape

    h = h
    w = w // 4
    for i in connections:
        poi1 = landmarks[i[0]]
        poi2 = landmarks[i[1]]
        if poi1.visibility >= 0.5 and poi2.visibility >= 0.5:
            xxx1 = w / 2 - poi1.z * w

            yyy1 = poi1.y * h
            xxx2 = w / 2 - poi2.z * w
            yyy2 = poi2.y * h

            ma = 3
            val = abs((xxx1 + xxx2) / w / 2)
            cv2.circle(image, [int(xxx1), int(yyy1)], int(ma), (0, 0, 0))
            cv2.circle(image, [int(xxx2), int(yyy2)], int(ma), (0, 0, 0))
            cv2.line(image, [int(xxx1), int(yyy1)], [int(xxx2), int(yyy2)], (0, 0, 203), int(1))


def draw_edges(frame):
    cv2.setUseOptimized(onoff=True)
    blur = 3
    linesize = 7
    k = 30
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayBlur = cv2.medianBlur(gray, blur)
    edges = cv2.Canny(grayBlur, k, k)
    return edges


def pre_wok():
    while webcam.isOpened():
        frame = cv2.imread("1_BpJhcvGwx6ucBjbosW11WA.png")
        _ = draw_edges(frame)
        mask = np.zeros(frame.shape, np.uint8)
        mask_cont = np.zeros(frame.shape, np.uint8)
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
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
            try:
                draw_line(mask, results.face_landmarks.landmark, mp_holistic.FACEMESH_TESSELATION)
            except:
                pass
            h, w, c = height, width, image.shape[-1]
            r = results.right_hand_landmarks
            # mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            if results.right_hand_landmarks:
                # 5,9,13,17
                # print(r.landmark)
                try:
                    pass
                    # draw_line(mask, r.landmark, mp_holistic.HAND_CONNECTIONS)
                except:
                    pass
            # mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            l = results.left_hand_landmarks
            # Pose Detections
            p = results.pose_landmarks
            # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            im = image
            im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
            cv2.imshow("dh", im)
            cv2.imshow("moa", mask)
            f = draw_edges(image)
            min_a = 120
            l, _ = cv2.findContours(f, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            

            for i in l:
                area = cv2.contourArea(i)
                if area >= min_a:
                    h = cv2.convexHull(i)
                    cv2.drawContours(mask_convex, h, -1, (0, 45, 90))
                    cv2.drawContours(mask_cont,i,1,(1,80,90))

            cv2.imshow("h", f)
            cv2.drawContours(mask_cont, l, -1, (0, 45, 90))

            cv2.imshow("cont", mask_cont)
            cv2.imshow("conv", mask_convex)
            cv2.waitKey(1)


t = threading.Thread(target=pre_wok)
t.start()
score = 0
# face
# body
# hands
# reconstruction ai
