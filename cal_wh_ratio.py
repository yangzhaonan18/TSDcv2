# -*- coding:utf-8 -*-
import cv2
import numpy as np


def cal_wh_ratio(cnt):
    """
    :param cnt: 一个轮廓
    :return: [1, wh_rat, [width, heigh]] 第一个值0表示轮廓是横向的，1表示纵向的；
    第二个变量表示宽窄边的比例， 第三个变量表示轮廓的宽度和高度；
    """
    print("run def cal_wh_ratio(cnt) >>>")

    # cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 5)
    # cv2.minEnclosingCircle(cnt)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径
    # SomeThings_line = SomeThings.copy()
    # SomeThings_line =
    # cv2.imshow("SomeThings_line", SomeThings_line )
    try:
        rect = cv2.minAreaRect(cnt)  # 最小外接矩形
        box = cv2.boxPoints(rect)
        box = np.int0(box)  # 左下角的点开始计数，顺时针转
        print(box)
        # print("box:", box)  # [[310 525] [307 254] [399 253] [402 524]]
        # heigh = box[0][1] - box[1][1]
        # width = box[2][0] - box[1][0]
        # heigh = box[0][1] - box[3][1]
        # width = box[0][0] - box[3][0]

        x = 100000
        y = 100000
        width = 0
        heigh = 0
        for i in range(len(box)):
            if box[i][0] < x:
                x = box[i][0]
            if box[i][1] < y:
                y = box[i][0]
            for j in range(1, len(box)):
                if box[i][0] - box[j][0] > width:
                    width = box[i][0] - box[j][0]
                if box[i][1] - box[j][1] > heigh:
                    heigh = box[i][1] - box[j][1]

        # if heigh < 10 or width < 10:  # 忽略低于10像素的 #################33？？？？？？？？？？？？？？？？？？？？？？？？
        #     return [-1, -1, [-1, -1]]
        print("min(heigh, width)", min(heigh, width))
        print("max(heigh, width)", max(heigh, width))
        if min(heigh, width) < 5:
            return None
        rat = max(heigh, width) / min(heigh, width)  # int(rat + 0.5) =  3
        # wh_rat = int(rat + 0.5)  # 四舍五入取整
        wh_rat = int(rat)
        if width > heigh:
            return [0, wh_rat, [x, y, width, heigh]]  # 0 表示图标是横向的
        else:
            return [1, wh_rat, [x, y, width, heigh]]  # 1 表示图标是纵向的
    except:
        return None

