# -*- coding:utf-8 -*-
import cv2
import numpy as np
from find_ColorThings import find_ColorThings
from judge_index import judge_index

def find_class_name(SquareThings, color, min_s, max_s):
    print("def find_class_name(SquareThings, color, min_s, max_s):  >>>")
    BinColors, BinThings, contours, hierarchy = find_ColorThings(SquareThings, color, num=1)
    contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
    if len(contours) > 0:
        direct_index = judge_index(BinColors, contours, color, min_s=min_s, max_s=max_s, max_item=55)
        index_dict = {0: "circle", 1: "<- ", 2: "/\\", 3: "->", 4: "V"}
        print("direction:", index_dict[direct_index])
        return index_dict[direct_index]
    else:
        print("NONONOONON0 color %d:" % color)
        return "NONONOONON0 color %d:" % color
