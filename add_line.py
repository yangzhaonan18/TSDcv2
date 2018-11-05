# -*- coding:utf-8 -*-
import cv2
from cal_circle_xy import cal_circle_xy


def add_line(ColorThings, x, y, radius):
    print("def add_line(ColorThings, x, y, radius):  >>>")
    x = int(x)
    y = int(y)
    x1, x2, y1, y2 = cal_circle_xy(ColorThings, x, y, radius)
    # 画矩形框
    cv2.circle(ColorThings, (x, y), int(radius), (0, 255, 255), 2)  # 画圆
    cv2.rectangle(ColorThings, (x1, y1), (x, y), (0, 0, 255), 2)  # 左上
    cv2.rectangle(ColorThings, (x, y1), (x2, y), (0, 0, 255), 2)  # 右上
    cv2.rectangle(ColorThings, (x1, y), (x, y2), (0, 0, 255), 2)  # 左下
    cv2.rectangle(ColorThings, (x, y), (x2, y2), (0, 0, 255), 2)  # 右下
