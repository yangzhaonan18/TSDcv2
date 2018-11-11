# -*- coding:utf-8 -*-
import cv2
import numpy as np
from cal_rect_xy import cal_rect_xy


def Crop_cnt(frame, cnt, color, wh_ratio):  # 裁剪轮廓凸包

    """
    :param frame:
    :param cnt:
    :return: CropThing 返回经过 旋转裁剪 后的图片
    """
    print(" def Crop_cnt(frame, cnt, color, wh_ratio): >>>")
    hull = cv2.convexHull(cnt)  # 找到凸包
    rect_min = cv2.minAreaRect(hull)  # 最小外接矩形
    x1, y1, w, h = cv2.boundingRect(hull)  # 外接矩形
    box01 = cv2.boxPoints(rect_min)  # 将中心点宽度高度旋转角度的表示方法转为点坐标
    box = np.int0(box01)  # 最小外接矩形

    ColorThings_line = frame.copy()  # 显示图片

    # cv2.rectangle(ColorThings_line, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)  # 画外接矩形
    # cv2.imshow("Crop_cnt: ", ColorThings_line)
    # print("box", type(box))  # box  <class 'numpy.ndarray'> [[178 488] [156 444] [322 363] [343 407]]
    # print("box:", box)

    print("wh_ratio", wh_ratio)
    if not wh_ratio:
        if wh_ratio[1] > 1 and color == "red":  # 只有长条红色的图形需要纠正倾斜
            cx1, cx2, cy1, cy2 = cal_rect_xy(box)
            CropThing = frame[cy1:cy2, cx1:cx2]  # 裁剪图片
            x0 = box[0][0] - cx1  # 最下面的那个点（首选左边的）
            y0 = box[0][1] - cy1
            x1 = box[1][0] - cx1
            y1 = box[1][1] - cy1
            x2 = box[2][0] - cx1
            y2 = box[2][1] - cy1
            x3 = box[3][0] - cx1
            y3 = box[3][1] - cy1
            w = box[2][0] - box[1][0]
            h = box[0][1] - box[1][1]
            print(x0, x1, x2, x3, y0, y1, y2, y3)
            rat = 1.1  # 缩放比例  利用三个坐标点透视变换 （特点：前后平行线保持平行）
            pts1 = np.float32([[x1, y1], [x0, y0], [x2, y2]])
            pts2 = np.float32([[0, 0], [0, int(h * rat)], [int(w * rat), 0]])
            # print("pts1, pts2", pts1, pts2)
            # print("(int(w * rat), int(h * rat)):", (int(w * rat), int(h * rat)))
            M = cv2.getAffineTransform(pts1, pts2)
            CropThing = cv2.warpAffine(CropThing, M, (int(w * rat), int(h * rat)))  # 纠正倾斜后的裁剪后图形
            cv2.drawContours(ColorThings_line, [box], 0, (0, 0, 255), 2)  # 画最小外接矩形
            cv2.imshow("ColorThings_line", ColorThings_line)
            # cv2.waitKey(0)
            # 这里需要将外接倾斜矩形 纠正成水平的（透视变换）
            # 先切分开图像成功多块
            # 原图上裁剪出含cnt凸包的部分
            return CropThing  # 返回裁剪下来的图片
        else:  # 正方的图形，不需要纠正角度（很难判断是否是倾斜的）
            cv2.rectangle(ColorThings_line, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)  # 画最小外接矩形
            cv2.imshow("ColorThings_line", ColorThings_line)
            # cv2.waitKey(0)
            return frame[y1: y1 + h, x1:x1 + w]
    return None
