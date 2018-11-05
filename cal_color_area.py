# -*- coding:utf-8 -*-
import cv2


def cal_color_area(BinColors, contours, hierarchy):  # 计算轮廓的面积。两个变量的长度是相同的，同一个图形的参数
    print("def cal_color_area(BinColors, contours, hierarchy): >>>")

    # print(type(hierarchy))  # <class 'numpy.ndarray'>  多维矩阵………还没有细看
    # print("hierarchy[0] = ", hierarchy[0])  # hierarchy[0] =  [[ 1 -1 -1 -1] [ 2  0 -1 -1]]
    # print("hierarchy[0][0][0] = ", hierarchy[0][0][0])  # hierarchy[0][0][0] =  1
    if len(contours) == 0:
        print("len(contours) == 0:")
        return -1
    if len(contours) == 1:
        print("len(contours) == 1:")
        return cv2.contourArea(contours[0])
    area_p = 0
    area_n = 0
    i = 0
    j = 0
    flag = 1
    BinColors_show = BinColors.copy()
    print("hierarchy =", hierarchy)
    while i != -1:  # 遍历第一层所有的轮廓的编号  cv2.RETR_CCOMP 保证包住白色的轮廓是第一层，包住黑色的是第二层
        print("i =", i)
        cv2.drawContours(BinColors_show, contours, i, (0, 0, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充
        cv2.imshow("cal_color_area//BinColors_show", BinColors_show)
        area_p += cv2.contourArea(contours[i])
        if hierarchy[0][i][0] != i + 1 and flag == 1:
            j = i + 1
            flag = 0
        i = hierarchy[0][i][0]  # 同一层的编号是串联的，一个接一个
    print("area_p =", area_p)
    while j != -1 and j < len(contours):  # 遍历第二层所有的轮廓的编号
        print("j =", j)
        cv2.drawContours(BinColors_show, contours, j, (255, 255, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充
        cv2.imshow("cal_color_area//BinColors_show", BinColors_show)
        area_n += cv2.contourArea(contours[j])

        j = hierarchy[0][j][0]
    print("area_n =", area_n)
    print("area_p - area_n =", area_p - area_n)
    return area_p - area_n

