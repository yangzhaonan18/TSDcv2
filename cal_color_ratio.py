# -*- coding:utf-8 -*-
import cv2
import math
from find_ColorThings import find_ColorThings
from cal_color_area import cal_color_area


def cal_ratio(CropThing, color):  # 计算颜色的比例 考虑 单个目标和多个目标的计算过程 方法相同
    print("def cal_ratio(CropThing, color):   >>>")
    # cv2.imshow("cal_ratio/CropThing ", CropThing)  # 直接裁剪后，没有处理过的图片
    BinColors, BinThings, contours, hierarchy = find_ColorThings(CropThing, color, num=0, RETR=cv2.RETR_CCOMP)
    if not contours or len(contours) == 0:
        print("cal_ratio // len(contours) == 0")
        return -1, -1, -1, -1
    color_area = cal_color_area(BinColors, contours, hierarchy)
    cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
    cnt_area = cv2.contourArea(cnt_max)  # 轮廓的面积 ？ 不能使用这个参数 判断不直观
    hull = cv2.convexHull(cnt_max)  # 计算出凸包形状(计算边界点)

    hull_area = cv2.contourArea(hull)  # 计算凸包面积

    (x, y), radius = cv2.minEnclosingCircle(cnt_max)
    circle_area = math.pi * radius * radius
    # center = (int(x), int(y))
    # radius = int(radius)
    # cv2.circle(img, center, radius, (0, 255, 0), 2)

    x, y, w, h = cv2.boundingRect(cnt_max)  # 外接矩形
    if hull_area == 0:
        print("cal_ratio // hull_area == 0")
        return -1, -1, -1, -1
    color_ratio = float(color_area) / hull_area  # 轮廓中某种颜色的面积与 凸包面积的比值
    cnt_ratio = float(cnt_area) / hull_area  # 轮廓面积与 凸包面积的比值
    rect_ratio = float(cnt_area)/(w * h)  # 矩形度   轮廓面积与最小外接矩形的比值  用于区分是否是规则图形
    circle_ratio = float(cnt_area)/circle_area
    print("cal_ratio // color_ratio", color_ratio)
    print("cal_ratio // cnt_ratio", cnt_ratio)
    print("cal_ratio // hull_area", hull_area)
    print("cal_ratio // rect_ratio", rect_ratio)
    print("cal_ratio // circle_ratio", circle_ratio)

    CropThing_show = CropThing.copy()
    # for i in range(len(contours)):  [contours[3]]
    # cnts = contours[max_index]
    # cv2.drawContours(CropThing_show, [contours[3]], -1, (0, 255, 255), 1)  # 最后一个数字表示线条的粗细 -1时表示填充
    # cv2.imshow(" cal_ratio", CropThing_show)
    # cv2.waitKey(0)

    # CropThing_show = SomeBinary.copy()  # 这个图片只要红色
    # # cv2.drawContours(CropThing_show, contours, i, (0, 255, 255), 1)  # 最后一个数字表示线条的粗细 -1时表示填充
    #
    # cv2.namedWindow("cal_ratio:", 0)
    # cv2.resizeWindow("cal_ratio:", 640, 480)
    # cv2.imshow("cal_ratio:", CropThing_show)
    # cv2.waitKey(0)
    #

    return color_ratio, cnt_ratio, rect_ratio, circle_ratio

