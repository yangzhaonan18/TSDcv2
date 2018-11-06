# -*- coding:utf-8 -*-
import cv2
from cal_wh_ratio import cal_wh_ratio
from Crop_cnt import Crop_cnt
from cal_color_ratio import cal_color_ratio
from find_crop_center import find_crop_center


def detection(frame, BinColors, color, contours, i):  # 判断是否是需要识别的对象 是返回1 否为0
    """
    :param frame:  一张没有处理过的原始图片
    :param BinColors:  经过颜色选择 二值化处理之后对应彩色部分的图片
    :param color:  当前处理的颜色
    :param contours:  当前颜色提取出的所有轮廓
    :param i: 正在处理的轮廓下表号
    :return: -1 表示当前编号对应的轮廓是不需要的后续对象（直接放弃的对象），1 表示是需要后续分类的对象
    """
    print("def detection(frame, BinColors, color, contours, i):   >>>")
    # 输入只有一个轮廓

    BinColors_show = BinColors.copy()
    cv2.drawContours(BinColors_show, contours, i, (0, 255, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充
    cv2.imshow("detection/BinColors_show", BinColors_show)  # 二值彩图上显示当前处理的轮廓

    wh_ratio = cal_wh_ratio(contours[i])  # 返回轮廓的比例 [1,判断外接矩形的长宽比例   不应该很大
    CropThing = Crop_cnt(frame, contours[i], color, wh_ratio)  # 裁剪图片， 将图片变成水平的
    color_ratio, cnt_ratio = cal_color_ratio(CropThing, color)  # 计算轮廓面积 与 凸包面积的比例  不应该很大
    if color_ratio == -1:  # 排除计算异常的情况
        print(">>>  case: color_ratio == -1")
        return None, -1
    if wh_ratio[0] == -1:  # 排除计算异常的情况
        print(">>> case: wh_ratio[0] == -1 :", wh_ratio)
        return None, -1
    if wh_ratio[1] > 9:  # 排除长宽比例和合理的情况
        print(">>> case: wh_ratio[1] > 9 :", wh_ratio)
        return None, -1

    # 下面讨论只符合条件的情况 可能是红绿灯的情况：
    # 红灯 = 红色 + 长窄比为1 + 尺寸（10:50）
    if color == "red" and wh_ratio[1] == 1:
        if wh_ratio[2][0] > 10 and wh_ratio[2][0] < 50 and color_ratio > 0.5 and color_ratio / cnt_ratio >= 1:
            print(">>> a red  light" * 10)
            return CropThing, 1
        if wh_ratio[2][0] > 15 and wh_ratio[2][0] < 150 and color_ratio / cnt_ratio != 1:
            if color_ratio / cnt_ratio < 0.99:  # 图标中间有非红色
                print(">>> a red sign " * 10)
            return CropThing, 1

    elif color == "red" and wh_ratio[1] > 1 and wh_ratio[1] < 10:  # 长宽比限制
        if wh_ratio[2][0] > 15 and wh_ratio[2][
            1] > 15 and color_ratio / cnt_ratio < 1 and color_ratio < 0.85 and color_ratio > 0.3:

            print(">>> many red sign " * 10)
            CropThing_show, center, radius = find_crop_center(CropThing, color)
            return CropThing_show, 1

    if color == "green" and wh_ratio[1] == 1 and color_ratio > 0.4 and wh_ratio[2][0] > 10 and wh_ratio[2][
        0] < 50 and color_ratio / cnt_ratio >= 1:
        print(">>> a green light" * 10)
        return CropThing, 1

    if color == "blue" and wh_ratio[1] == 1:
        print(">>> a blue sign" * 10)
        return CropThing, 1

    elif color == "blue" and wh_ratio[0] == 1 and wh_ratio[2][0] > 20 and wh_ratio[2][0] < 150 and (
            wh_ratio[1] == 2 or wh_ratio[1] == 3):
        print(">>> many  longitudinal blue sign" * 10)
        CropThing_show, center, radius = find_crop_center(CropThing, color)
        return CropThing_show, 1

    if color == "yellow" and wh_ratio[1] == 1 and color_ratio > 0.4 and wh_ratio[2][0] > 10 and wh_ratio[2][
        0] < 50 and color_ratio / cnt_ratio >= 1:
        print(">>> a yellow light" * 10)
        return CropThing, 1
    cv2.waitKey(0)
    if color == "yellow" and wh_ratio[0] == 0 and wh_ratio[1] == 2 and wh_ratio[2][0] > 50 and wh_ratio[2][
        0] < 400 and color_ratio / cnt_ratio < 0.9 and color_ratio > 0.5 and cnt_ratio > 0.9:
        print(">>> a yellow ETC sign " * 10)
        return CropThing, 1

    elif color == "yellow" and wh_ratio[1] == 1 and color_ratio > 0.5:
        print(">>> mabey a yellow work sign")
        return CropThing, 1

    # center, radius = find_crop_center(CropThing, color)
    # cv2.drawContours(frame, [box[0:2]], 0, (0, 0, 255), 2)   # 画外接矩形
    # cv2.imshow("frame", frame)
    # print("wh_ratio:", wh_ratio)
    # print("color_ratio:", color, "=", color_ratio)
    # print("good " * 10)

    else:
        return None, -1
