# -*- coding:utf-8 -*-

import cv2
import os
import numpy as np

from cal_wh_ratio import cal_wh_ratio
from Crop_cnt import Crop_cnt
from cal_color_ratio import cal_color_ratio
from find_crop_center import find_crop_center




def find_ColorThingsOfLight02(frame, color, num=0, RETR=cv2.RETR_EXTERNAL, dilate_num=1):  # 默认返回最外层的轮廓
    print(" def find_ColorThings(frame, color, num=0, RETR=cv2.RETR_EXTERNAL): >>>")
    mask = find_light_mask(frame, color)

    # BinColors = cv2.bitwise_and(frame, frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
    # gray = cv2.cvtColor(BinColors, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
    # gray = cv2.cvtColor(BinColors, cv2.COLOR_BGR2GRAY)  # 转成灰色图像


    # mask = cv2.dilate(mask, None, iterations=dilate_num)  # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    # mask = cv2.erode(mask, None, iterations=num)  # 腐蚀操作
    BinColors = cv2.bitwise_and(frame, frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
    # an_ColorThings = cv2.bitwise_not(frame, frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
    # cv2.imshow("an_ColorThings:", an_ColorThings)
    # cv2.waitKey(0)  # ********************************

    # cv2.imshow("First BinColors",  BinColors)  # 显示感兴趣的颜色区域

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 直线提取    找到轮廓的时候忽略掉小目标 后续正确的小目标通过膨胀复原
    # BinColors = cv2.morphologyEx(BinColors, cv2.MORPH_OPEN, kernel)

    # cv2.imshow("line-result", ColorThings_er)
    #
    # BinColors = cv2.GaussianBlur(BinColors, (3, 3), 0)  # 彩色图时 高斯消除噪音
    gray = cv2.cvtColor(BinColors, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
    # # cv2.imshow("gray image", gray)

    ret, BinThings = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
    # cloneImage, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 边界不是封闭的
    # cloneImage, contours, hierarchy = cv2.findContours(BinThings, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的
    BinThings, contours, hierarchy = cv2.findContours(BinThings, RETR, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 黑白图时 直线消除 小斑点
    # BinThings = cv2.morphologyEx(BinThings, cv2.MORPH_OPEN, kernel)  # 输出是二值化的图片， 后面用来作为轮廓使用 吧！！！！！
    BinThings, contours, hierarchy = cv2.findContours(BinThings, RETR, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的

    ret, mask = cv2.threshold(BinThings, 1, 255, cv2.THRESH_BINARY)  # 二值图提取mask
    BinColors = cv2.bitwise_and(frame, frame, mask=mask)  # 二值化中白色对应的彩色部分
    cv2.imshow("find_ColorThings/BinColors：", BinColors)
    return BinColors, BinThings, contours, hierarchy




def cal_diamond_ratio(frame, color, cnt):
    print("def cal_diamond_ratio(frame, color, contours, i):   >>>>>>")
    x, y, w, h = cv2.boundingRect(cnt)  # 外接矩形
    crop_frame = frame[y: y + h, x:x + w]

    # crop_frame = cv2.bitwise_and(frame, frame, mask=contours[i])
    cv2.imshow("crop_frame",  crop_frame)
    BinColors, BinThings, contours, hierarchy = find_ColorThingsOfLight02(crop_frame, color, num=0, dilate_num=0)  # num = 腐蚀的次数
    # cv2.imshow("cal_diamond_ratio", BinColors)
    # cv2.waitKey(0)
    if not contours:
        print("contours = None")
        return None

    cnt_max = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt_max)  # 外接矩形
    area01 = w * h

    rect = cv2.minAreaRect(cnt_max)  # 最小外接矩形
    # print("rect" * 10, rect) ((5.0, 4.0), (8.0, 6.0), -0.0)
    box = cv2.boxPoints(rect)
    box = np.int0(box)  # 左下角的点开始计数，顺时针转
    # print("box:", box)  # [[310 525] [307 254] [399 253] [402 524]]
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
    # heigh = box[0][1] - box[1][1]
    # width = box[2][0] - box[1][0]
    area02 = width * heigh

    diamond_ratio = float(area01) / area02  # 正外接矩形的面积 除 最小外接矩形的面积
    print("area01 = ", area01)
    print("area02 = ", area02)
    print("area01/area02 = diamond_ratio", diamond_ratio)

    # 理论上信号灯计数器的diamond_ratio = 1,  箭头的diamond_ratio= 2
    # 箭头被遮挡 只出现一半时 如何判断？
    # diamond_ratio = 2 的一定是剪头， =1不确定是什么？ 不能通知这个来之间判断是否是箭头
    return diamond_ratio

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
    frame_copy = frame.copy()
    print("contours i = ", i)
    cv2.drawContours(BinColors_show, contours, i, (0, 255, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充
    cv2.imshow("detection/BinColors_show", BinColors_show)  # 二值彩图上显示当前处理的轮廓

    # 计算轮廓的相关信息

    diamond_ratio = cal_diamond_ratio(frame, color, contours[i])  # 如果值=2 一定是箭头  =1 正矩形
    print("diamond_ratio = ", diamond_ratio)
    wh_ratio = cal_wh_ratio(contours[i])  # 返回轮廓的比例 [1,判断外接矩形的长宽比例   不应该很大
    if not wh_ratio:
        return None, []
    CropThing = Crop_cnt(frame, contours[i], color, wh_ratio)  # 裁剪图片， 将图片变成水平的
    color_ratio, cnt_ratio = cal_color_ratio(CropThing, color)  # 计算轮廓面积 与 凸包面积的比例  不应该很大



    if color_ratio == -1:  # 排除计算异常的情况
        print(">>>  case: color_ratio == -1")
        return None, []
    if wh_ratio[0] == -1:  # 排除计算异常的情况
        print(">>> case: wh_ratio[0] == -1 :", wh_ratio)
        return None, []
    if wh_ratio[1] > 9:  # 排除长宽比例和合理的情况
        print(">>> case: wh_ratio[1] > 9 :", wh_ratio)
        return None, []

    # 下面讨论只符合条件的情况 可能是红绿灯的情况：
    # 红灯 = 红色 + 长窄比为1 + 尺寸（10:50）
    if color == "red" and wh_ratio[1] == 1:
        if wh_ratio[2][2] > 10 and wh_ratio[2][2] < 100 and color_ratio > 0.5 and color_ratio / cnt_ratio >= 1:
            print(">>> a red  light" * 10)
            cv2.waitKey(0)
            return CropThing, []
        # if wh_ratio[2][2] > 15 and wh_ratio[2][2] < 150 and color_ratio / cnt_ratio != 1:
        #     if color_ratio / cnt_ratio < 0.99:  # 图标中间有非红色
        #         print(">>> a red sign " * 10)
        #         cv2.waitKey(0)
        #     return CropThing, 1

    # elif color == "red" and wh_ratio[1] > 1 and wh_ratio[1] < 10:  # 长宽比限制
    #     if wh_ratio[2][2] > 15 and wh_ratio[2][
    #         3] > 15 and color_ratio / cnt_ratio < 1 and color_ratio < 0.85 and color_ratio > 0.3:
    #
    #         print(">>> many red sign " * 10)
    #         cv2.waitKey(0)
    #         CropThing_show, center, radius = find_crop_center(CropThing, color)
    #         return CropThing_show, 1

    if color == "green" and wh_ratio[1] == 1 and color_ratio > 0.4 and wh_ratio[2][2] > 10 and wh_ratio[2][
        2] < 100 and color_ratio / cnt_ratio >= 1:
        print(">>> a green light" * 10)
        cv2.waitKey(0)
        return CropThing, 1

    # if color == "blue" and wh_ratio[1] == 1:
    #     print(">>> a blue sign" * 10)
    #     cv2.waitKey(0)
    #     return CropThing, 1

    # elif color == "blue" and wh_ratio[0] == 1 and wh_ratio[2][2] > 20 and wh_ratio[2][2] < 150 and (
    #         wh_ratio[1] == 2 or wh_ratio[1] == 3):
    #     print(">>> many  longitudinal blue sign" * 10)
    #     cv2.waitKey(0)
    #     CropThing_show, center, radius = find_crop_center(CropThing, color)
    #     return CropThing_show, 1

    if color == "yellow" and wh_ratio[1] == 1 and color_ratio > 0.4 and wh_ratio[2][2] > 10 and wh_ratio[2][
        2] < 100 and color_ratio / cnt_ratio >= 1:
        print(">>> a yellow light" * 10)
        cv2.waitKey(0)
        return CropThing, 1

    # if color == "yellow" and wh_ratio[0] == 0 and wh_ratio[1] == 2 and wh_ratio[2][2] > 50 and wh_ratio[2][
    #     2] < 400 and color_ratio / cnt_ratio < 0.9 and color_ratio > 0.5 and cnt_ratio > 0.9:
    #     print(">>> a yellow ETC sign " * 10)
    #     cv2.waitKey(0)
    #     return CropThing, 1

    # elif color == "yellow" and wh_ratio[1] == 1 and color_ratio > 0.5:
    #     print(">>> mabey a yellow work sign")
    #     cv2.waitKey(0)
    #     return CropThing, 1

    # center, radius = find_crop_center(CropThing, color)
    # cv2.drawContours(frame, [box[0:2]], 0, (0, 0, 255), 2)   # 画外接矩形
    # cv2.imshow("frame", frame)
    # print("wh_ratio:", wh_ratio)
    # print("color_ratio:", color, "=", color_ratio)
    # print("good " * 10)

    else:
        return None, -1





def find_light_mask(frame, color):
    print(" def find_light_mask(frame, color): >>>")
    blackLower01 = np.array([0, 0, 0])  # 黑的阈值 标准H：0:180 S:0:255 V:0:46:46
    blackUpper01 = np.array([180, 255, 46])
    #     # blackLower02 = np.array([0, 0, 46])  # 灰的阈值 标准H：0:180 S:0:43 V:0:46:220
    #     # blackUpper02 = np.array([180, 43, 45])  # 灰色基本没用

    redLower01 = np.array([0, 80, 80])  # 红色的阈值 标准H：0-10 and 160-179 S:43:255 V:46:255
    redUpper01 = np.array([10, 255, 255])
    redLower02 = np.array([156, 80, 80])  # 125 to 156
    redUpper02 = np.array([180, 255, 255])

    greenLower = np.array([50, 80, 80])  # 绿色的阈值 标准H：35:77 S:43:255 V:46:255
    greenUpper = np.array([95, 255, 255])  # V 60 调整到了150

    # blueLower = np.array([105, 120, 46])  # 蓝H:100:124 紫色H:125:155
    # blueUpper = np.array([130, 255, 255])

    yellowLower = np.array([26, 80, 100])  # 黄色的阈值 标准H：26:34 S:43:255 V:46:255
    yellowUpper = np.array([34, 255, 255])  # 有的图 黄色变成红色的了
    try:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        red1_mask = cv2.inRange(hsv, redLower01, redUpper01)  # 根据阈值构建掩膜, 红色的两个区域
        red2_mask = cv2.inRange(hsv, redLower02, redUpper02)
        red_mask = red1_mask + red2_mask

        # black01_mask = cv2.inRange(hsv, blackLower01, blackUpper01)  # 根据阈值构建掩膜,黑色的区域
        # black02_mask = cv2.inRange(hsv, blackLower02, blackUpper02)  # 根据阈值构建掩膜,黑色的区域
        # black_mask = black01_mask + black02_mask

        yellow_mask = cv2.inRange(hsv, yellowLower, yellowUpper)  # 根据阈值构建掩膜, 黄色的区域
        green_mask = cv2.inRange(hsv, greenLower, greenUpper)  # 根据阈值构建掩膜, 绿色的区域

        # blue_mask = cv2.inRange(hsv, blueLower, blueUpper)
        # if color == "black":
        #     mask = black_mask
        if color == "yellow":
            mask = yellow_mask
        elif color == "red":
            mask = red_mask
        elif color == "green":
            mask = green_mask
        # elif color == "blue":
        #     mask = blue_mask
        # elif color == "red+blue":
        #     mask = red_mask + blue_mask
        # elif color == "green+yellow":
        #     mask = green_mask + yellow_mask

        else:
            mask = None
        return mask

    except:
        return None



def find_ColorThings(frame, color, num=0, RETR=cv2.RETR_EXTERNAL):  # 默认返回最外层的轮廓
    print(" def find_ColorThings(frame, color, num=0, RETR=cv2.RETR_EXTERNAL): >>>")
    mask = find_light_mask(frame, color)

    mask = cv2.dilate(mask, None, iterations=2)  # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    mask = cv2.erode(mask, None, iterations=num)  # 腐蚀操作
    BinColors = cv2.bitwise_and(frame, frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
    # an_ColorThings = cv2.bitwise_not(frame, frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
    # cv2.imshow("an_ColorThings:", an_ColorThings)
    # cv2.waitKey(0)  # ********************************

    # cv2.imshow("First BinColors",  BinColors)  # 显示感兴趣的颜色区域

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 直线提取    找到轮廓的时候忽略掉小目标 后续正确的小目标通过膨胀复原
    BinColors = cv2.morphologyEx(BinColors, cv2.MORPH_OPEN, kernel)

    # cv2.imshow("line-result", ColorThings_er)

    dst = cv2.GaussianBlur(BinColors, (3, 3), 0)  # 彩色图时 高斯消除噪音
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
    # cv2.imshow("gray image", gray)

    ret, BinThings = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
    # cloneImage, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 边界不是封闭的
    # cloneImage, contours, hierarchy = cv2.findContours(BinThings, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的
    BinThings, contours, hierarchy = cv2.findContours(BinThings, RETR, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 黑白图时 直线消除 小斑点
    BinThings = cv2.morphologyEx(BinThings, cv2.MORPH_OPEN, kernel)  # 输出是二值化的图片， 后面用来作为轮廓使用 吧！！！！！
    BinThings, contours, hierarchy = cv2.findContours(BinThings, RETR, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的

    ret, mask = cv2.threshold(BinThings, 127, 255, cv2.THRESH_BINARY)  # 二值图提取mask
    BinColors = cv2.bitwise_and(frame, frame, mask=mask)  # 二值化中白色对应的彩色部分
    # cv2.imshow("find_ColorThings/BinColors：", BinColors)
    return BinColors, BinThings, contours, hierarchy




def dect_light(frame):
    frame = cv2.GaussianBlur(frame, (3, 3), 0)  # 高斯消除噪音
    for color in ["red", "yellow", "green"]:  # 分别单独处理三个颜色的结果
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 直线提取
        # frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        BinColors, BinThings, contours, hierarchy = find_ColorThings(frame, color, num=1)  # num = 腐蚀的次数
        if len(contours) < 1:  # 排除不存在轮廓的情况
            # contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
            print("\n>>> Path, color, len(contours) < 1 =", len(contours))
            continue
        contours.sort(key=lambda cnt: cv2.contourArea(cv2.convexHull(cnt)), reverse=True)  # 根据轮毂的面积降序排列

        for i in range(0, len(contours)):
            print("\n>>> Path, color, i =", img_path, color, i)
            # cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
            # print("len(contours):", len(contours))
            if cv2.contourArea(contours[i]) < 5:  # 排除面积判断 < 50
                print(">>> cv2.contourArea(contours[%d]) < 100 :" % i, cv2.contourArea(contours[i]))
                continue
            image, box = detection(frame, BinColors, color, contours, i)  # 判断是否是 需要识别的对象， 是返回1 否为0
            if box:  # 是需要的对象时
               " "


def find_light_box(frame, color):
    frame = cv2.GaussianBlur(frame, (3, 3), 0)  # 高斯消除噪音
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 直线提取
    # frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    BinColors, BinThings, contours, hierarchy = find_ColorThings(frame, color, num=1)  # num = 腐蚀的次数
    if len(contours) < 1:  # 排除不存在轮廓的情况
        # contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
        print("\n>>> Path, color, len(contours) < 1 =", len(contours))
        return []
    contours.sort(key=lambda cnt: cv2.contourArea(cv2.convexHull(cnt)), reverse=True)  # 根据轮毂的面积降序排列
    box_list = []
    for i in range(0, len(contours)):
        # print("\n>>> Path, color, i =", img_path, color, i)
        # cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
        # print("len(contours):", len(contours))
        if cv2.contourArea(contours[i]) < 20:  # 排除面积判断 < 50
            print(">>> cv2.contourArea(contours[%d]) < 20 :" % i, cv2.contourArea(contours[i]))
            continue
        image, box = detection(frame, BinColors, color, contours, i)  # 返回当前轮廓的坐标和类型
        if box:  # 是需要的对象时
            box_list.append(box)
    return box_list




if __name__ == "__main__":
    img_path = "C:\\Users\\young\\Desktop\\just\\2000\\TSD-Signal-00205-00000.png"
    save_dir = "C:\\Users\\young\\Desktop\\just\\2000-after"
    frame = cv2.imread(img_path)
    frame = cv2.GaussianBlur(frame, (3, 3), 0)  # 高斯消除噪音
    # contours_demo(number, img_path, frame, save_dir)
    #  在图片中找到红色的目标并返回 编号和坐标
    for color in ["red", "yellow", "green"]:  # 分别单独处理三个颜色的结果
        boxList = find_light_box(frame, color)
    # number = 0

    # dect_light(frame)

    # if not os.path.exists(save_dir):
    #     os.makedirs(save_dir)
        #     os.makedirs(os.path.join(os.path.join(save_dir, str(direct_index), color)))

        # save_dir = os.path.join(save_dir, color)
    # save_name = str(color) + "+" + str(number) + ".png"
    # save_path = os.path.join(save_dir, save_name)
    # cv2.imwrite(save_path, image)
