# -*- coding:utf-8 -*-
import cv2
import numpy as np
from add_line import add_line
from cal_circle_xy import cal_circle_xy
from find_class_name import find_class_name

def identify_light(SomeThings, cnt, color, min_s, max_s):
    print("def identify_light(SomeThings, cnt, color, min_s, max_s):  >>>")
    ((x, y), radius) = cv2.minEnclosingCircle(cnt)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径
    SomeThings_line = SomeThings.copy()
    add_line(SomeThings_line, x, y, radius)
    cv2.imshow("firt SomeThings_line", SomeThings_line)
    # cv2.waitKey(0)  # ********************************

    x1, x2, y1, y2 = cal_circle_xy(SomeThings, int(x), int(y), radius)
    SquareThings = SomeThings[y1:y2, x1:x2]  # 裁剪需要的部分
    SquareThings_resize = cv2.resize(SquareThings, (200, 200), interpolation=cv2.INTER_CUBIC)

    name = find_class_name(SquareThings_resize, color, min_s, max_s)

    font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体
    cv2.putText(SquareThings_resize, name, (1, 15), font, 0.5, (0, 0, 255), 1)  # 添加文字，1.2表示字体大小，（0,40）是
    cv2.imwrite(save_path, SquareThings_resize)  # 保存修改像素点后的图片

