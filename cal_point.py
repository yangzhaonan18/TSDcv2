# -*- coding:utf-8 -*-
import cv2
import numpy as np
from cal_circle_xy import cal_circle_xy


def cal_point(SomeBinary, x, y, radius):  # 返回最大方向的编号int
    print("def cal_point(SomeBinary, x, y, radius):   >>>")
    x = int(x)
    y = int(y)
    x1, x2, y1, y2 = cal_circle_xy(SomeBinary, x, y, radius)
    S00 = SomeBinary[y1:y, x1:x]  # 计算面积时，使用二值图，左上
    S01 = SomeBinary[y1:y, x:x2]  # 右上
    S10 = SomeBinary[y:y2, x1:x]  # 左下
    S11 = SomeBinary[y:y2, x:x2]  # 右下

    SS00 = np.sum(S00)
    SS01 = np.sum(S01)
    SS10 = np.sum(S10)
    SS11 = np.sum(S11)

    value = [SS00, SS01, SS10, SS11]
    value.sort(reverse=True)  # 将面积大的放在前面
    if SS01 in value[0:2] and SS11 in value[0:2]:  # 箭头右侧需要补齐的东西多
        return 1  # left
    elif SS10 in value[0:2] and SS11 in value[0:2]:
        return 2  # up
    elif SS00 in value[0:2] and SS10 in value[0:2]:
        return 3  # right
    elif SS00 in value[0:2] and SS01 in value[0:2]:
        return 4  # down
    else:
        direct_index = np.argmax(value)
        return direct_index + 1

