# color
import math

import cv2
import numpy as np


def color(image, point, radius):
    c = cv2.circle(image, point, radius, (0, 0, 0))
    i = cv2.bitwise_and(image, image, mask=c)
    roi = i[point[0] - radius / 2, point[1] - radius / 2:point[0] + radius / 2, point[1] + radius / 2]
    r = reduce_color(roi)
    h, w, c = r.shape
    return r[h // 2][w // 2]


def reduce_color(frame):
    data = np.float32(frame).reshape((-1, 3))
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    ret, label, center = cv2.kmeans(data, 1, None, crit, 10, cv2.KMEANS_PP_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(frame.shape)
    return result

    # initialization based on the cheeks


def math_triangle(point, line):
    m, c = line
    mp = -1 / m
    point

    return decimal


def angle(li_st, points):
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]
