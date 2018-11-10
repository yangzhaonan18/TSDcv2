# -*- coding:utf-8 -*-
import cv2
import os
import numpy as np

from cal_wh_ratio import cal_wh_ratio
from Crop_cnt import Crop_cnt
from cal_color_ratio import cal_ratio
from find_crop_center import find_crop_center

from find_ColorThings import find_ColorThings
from judge_index import judge_index


def find_light_direct(SquareThings, min_s=0.8, max_s=0.93):
    try:
        print("def find_class_name(SquareThings, color, min_s, max_s):  >>>")
        for color in ["red", "yellow", "green"]:
            SquareThings_resize = cv2.resize(SquareThings, (200, 200), interpolation=cv2.INTER_CUBIC)  # 放大之后方便腐蚀判断方向
            BinColors, BinThings, contours, hierarchy = find_ColorThings(SquareThings_resize, color, num=1)
            contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
            if len(contours) > 0:
                direct = judge_index(BinColors, contours, color, min_s=min_s, max_s=max_s, max_item=6)
                return direct
    except:
        return -1



def cal_color2_ratio(BinColors, contours, hierarchy):  # 计算轮廓的面积。两个变量的长度是相同的，同一个图形的参数
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
    area2_rect = 0.1
    while j != -1 and j < len(contours):  # 遍历第二层所有的轮廓的编号
        print("j =", j)
        cv2.drawContours(BinColors_show, contours, j, (255, 255, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充
        cv2.imshow("cal_color_area//BinColors_show", BinColors_show)
        area_n += cv2.contourArea(contours[j])
        rect = cv2.minAreaRect(contours[j])
        area2_now = rect[1][0] * rect[1][1]

        if area2_now > area2_rect:
            print("w * h > area2_rect:")
            area2_rect = area2_now
        j = hierarchy[0][j][0]
    print("area_n =", area_n)
    print("area_p - area_n =", area_p - area_n)
    # return area_p - area_n
    # The degree of rectangularity of the internal graph
    color2_ratio = area_n/area2_rect
    return color2_ratio


def find_mask(frame, color):
    print(" def find_light_mask(frame, color): >>>")
    blackLower01 = np.array([0, 0, 0])  # 黑的阈值 标准H：0:180 S:0:255 V:0:46:220
    blackUpper01 = np.array([180, 255, 90])
    blackLower02 = np.array([0, 0, 46])  # 灰的阈值 标准H：0:180 S:0:43 V:0:46:220
    blackUpper02 = np.array([180, 43, 45])  # 灰色基本没用

    redLower01 = np.array([0, 80, 80])  # 红色的阈值 标准H：0-10 and 160-179 S:43:255 V:46:255
    redUpper01 = np.array([10, 255, 255])
    redLower02 = np.array([156, 80, 80])  # 125 to 156
    redUpper02 = np.array([180, 255, 255])

    greenLower = np.array([50, 80, 80])  # 绿色的阈值 标准H：35:77 S:43:255 V:46:255
    greenUpper = np.array([95, 255, 255])  # V 60 调整到了150

    blueLower = np.array([105, 120, 46])  # 蓝H:100:124 紫色H:125:155
    blueUpper = np.array([130, 255, 255])

    yellowLower = np.array([26, 80, 100])  # 黄色的阈值 标准H：26:34 S:43:255 V:46:255
    yellowUpper = np.array([34, 255, 255])  # 有的图 黄色变成红色的了
    try:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        red1_mask = cv2.inRange(hsv, redLower01, redUpper01)  # 根据阈值构建掩膜, 红色的两个区域
        red2_mask = cv2.inRange(hsv, redLower02, redUpper02)
        red_mask = red1_mask + red2_mask

        black01_mask = cv2.inRange(hsv, blackLower01, blackUpper01)  # 根据阈值构建掩膜,黑色的区域
        black02_mask = cv2.inRange(hsv, blackLower02, blackUpper02)  # 根据阈值构建掩膜,黑色的区域
        black_mask = black01_mask + black02_mask

        yellow_mask = cv2.inRange(hsv, yellowLower, yellowUpper)  # 根据阈值构建掩膜, 黄色的区域
        green_mask = cv2.inRange(hsv, greenLower, greenUpper)  # 根据阈值构建掩膜, 绿色的区域

        blue_mask = cv2.inRange(hsv, blueLower, blueUpper)
        if color == "black":
            mask = black_mask
        elif color == "yellow":
            mask = yellow_mask
        elif color == "red":
            mask = red_mask
        elif color == "green":
            mask = green_mask
        elif color == "blue":
            mask = blue_mask
        elif color == "red+blue":
            mask = red_mask + blue_mask
        elif color == "green+yellow":
            mask = green_mask + yellow_mask

        else:
            mask = None
        return mask

    except:
        return None


def find_ColorThings(frame, color, num=0, RETR=cv2.RETR_EXTERNAL, dilate_num=2):  # 默认返回最外层的轮廓
    print(" def find_ColorThings(frame, color, num=0, RETR=cv2.RETR_EXTERNAL): >>>")
    mask = find_mask(frame, color)
    mask = cv2.dilate(mask, None, iterations=dilate_num)  # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    # mask = cv2.erode(mask, None, iterations=num)  # 腐蚀操作
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





def find_box(crop_frame, mask):
    BinColors = cv2.bitwise_and(crop_frame, crop_frame, mask=mask)
    cv2.imshow("BinColors", BinColors)
    gray = cv2.cvtColor(BinColors, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
    cv2.imshow("gray image", gray)
    ret, BinThings = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
    BinThings, contours, hierarchy = cv2.findContours(BinThings, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    cnt_max = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt_max)
    return x, y, w, h


def correct_10(frame, results):  # to "11"=W38 work man
    for i in range(len(results)):
        results[i][2] = list(results[i][2])
    # light_num = ["10", ]  # 交通灯的类型编号
    print("results", results)
    for i in range(0, len(results)):
        if results[i][0] == "10":  # P 误判成P 路牌时
            print("i =", i)
            print("str(results[i][0]) == 10:")
            x1 = int(results[i][2][0] - results[i][2][2] / 2)  # 将中心点的坐标转换成 左上角的坐标
            x2 = int(results[i][2][0] + results[i][2][2] / 2)
            y1 = int(results[i][2][1] - results[i][2][3] / 2)
            y2 = int(results[i][2][1] + results[i][2][3] / 2)
            print("x1,y1,x2,y2 = ", x1, y1, x2, y2)
            crop_frame = frame[y1: y2, x1: x2]
            try:
                mask = find_yellow_mask(crop_frame)  # 区域中有黄色存在的情况
                print("mask")
                x, y, w, h = find_box(crop_frame, mask)
                if w * h > 20 and (x + w/2) > (x2 - x1)/4 and (w / h < 3 and h / w < 3):  # 黄色区域已经要在图像的上方中间
                    print("10 to red work man")
                    results[i][2][0] = x1 + x + w / 2  # center point
                    results[i][2][1] = y1 + y + h / 2
                    results[i][2][2] = w * 3
                    results[i][2][3] = h * 2
                    results[i][0] = "11"
                # if find_in_size(crop_frame)

                # rect_ratio(crop_frame)
                BinColors, BinThings, contours, hierarchy = find_ColorThings(crop_frame, "blue", num=1, RETR=cv2.RETR_CCOMP)
                if len(contours) == 0:
                    continue
                print("is blue")
                color2_ratio = cal_color2_ratio(BinColors, contours, hierarchy)
                print("color2_ratio", color2_ratio)
                if color2_ratio > 0.9 and BinColors.shape[0] > 10:  # 绿色标志中 中间白色部分占了整个矩形 则将类别标记为 “-1”。只考图标尺寸较大一点的
                    results[i][0] = "-1"
            except:
                ""
    for result in results:  # 遍历数据 删除之前标记类别为-1 的测试目标
        if result[0] == "-1":
            results.remove(result)

    return results


def draw_line(frame, newResults):
    for i in range(len(newResults)):
        x1 = int(newResults[i][2][0] - newResults[i][2][2] / 2)
        x2 = int(newResults[i][2][0] + newResults[i][2][2] / 2)
        y1 = int(newResults[i][2][1] - newResults[i][2][3] / 2)
        y2 = int(newResults[i][2][1] + newResults[i][2][3] / 2)
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.imshow("add line", frame)
    cv2.waitKey(0)

def find_light_mask(frame):
    print(" def find_light_mask(frame, color): >>>")
    redLower01 = np.array([0, 80, 80])  # 红色的阈值 标准H：0-10 and 160-179 S:43:255 V:46:255
    redUpper01 = np.array([10, 255, 255])
    redLower02 = np.array([156, 80, 80])  # 125 to 156
    redUpper02 = np.array([180, 255, 255])
    greenLower = np.array([50, 80, 80])  # 绿色的阈值 标准H：35:77 S:43:255 V:46:255
    greenUpper = np.array([95, 255, 255])  # V 60 调整到了150
    yellowLower = np.array([26, 80, 80])  # 黄色的阈值 标准H：26:34 S:43:255 V:46:255
    yellowUpper = np.array([34, 255, 255])  # 有的图 黄色变成红色的了
    try:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        red1_mask = cv2.inRange(hsv, redLower01, redUpper01)  # 根据阈值构建掩膜, 红色的两个区域
        red2_mask = cv2.inRange(hsv, redLower02, redUpper02)
        red_mask = red1_mask + red2_mask

        yellow_mask = cv2.inRange(hsv, yellowLower, yellowUpper)  # 根据阈值构建掩膜, 黄色的区域
        green_mask = cv2.inRange(hsv, greenLower, greenUpper)  # 根据阈值构建掩膜, 绿色的区域

        mask = red_mask + green_mask + yellow_mask
        return mask
    except:
        return None


def find_yellow_mask(frame):
    yellowLower = np.array([20, 43, 46])  # 黄色的阈值 标准H：26:34 S:43:255 V:46:255
    yellowUpper = np.array([36, 255, 255])  # 有的图 黄色变成红色的了
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, yellowLower, yellowUpper)  # 根据阈值构建掩膜, 黄色的区域
    return yellow_mask





def correct_light_box(frame, results):
    # [["19", 0.913, (830.6, 72.8, 22.2, 49.7)], ["19", 0.8, (990.3, 64.4, 24.0, 37.8)],["19", 0.85, (685.5, 82.4, 24.5, 52.2)]]
    light_num = ["15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]  # 交通灯的类型编号
    newResults = []
    if len(results) > 0:
        for i in range(0, len(results)):
            # results[i][:] = [list(result) for result in results[i]]
            newResult = ["-1", 0.5, [0.0, 0.0, 0.0, 0.0]]
            try:
                if str(results[i][0]) in light_num:
                    print("results[i] =", results[i])
                    x1 = int(results[i][2][0] - results[i][2][2] / 2)  # 将中心点的坐标转换成 左上角的坐标
                    x2 = int(results[i][2][0] + results[i][2][2] / 2)
                    y1 = int(results[i][2][1] - results[i][2][3] / 2)
                    y2 = int(results[i][2][1] + results[i][2][3] / 2)
                    print("x1,y1,x2,y2 = ", x1, y1, x2, y2)
                    XL = 10
                    YU = 10
                    crop_frame = frame[y1 - XL: y2 + 10,  x1 - YU: x2 + 10]  # 上下左右都扩展10
                    mask = find_light_mask(crop_frame)
                    light_direct = find_light_direct(crop_frame, color)
                    x, y, w, h = find_box(crop_frame, mask)  # 坐标是相对于截图的坐标
                    if w * h > 3:
                        # frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))
                        # cv2.imshow("frame", frame)
                        cv2.waitKey(0)
                        newResult[2][0] = x1 + x + w/2 - XL  # center point
                        newResult[2][1] = y1 + y + h/2 - YU
                        newResult[2][2] = w
                        newResult[2][3] = h
                        newResult[0] = results[i][0]
                        newResult[1] = results[i][1]
                        newResults.append(newResult)
            except:
                continue
    return newResults


if __name__ == "__main__":
    img_path = "C:\\Users\\young\\Desktop\\just\\2000\\TSD-Signal-00205-00027.png"  # 纠正红绿灯的例子
    # img_path = "C:\\Users\\young\\Desktop\\just\\2000\\TSD-Signal-00238-00014.png"  # 纠正13号绿牌的例子
    # img_path = "C:\\Users\\young\\Desktop\\just\\2000\\1204.jpg"  # 纠正 蓝色中白 摄像头的 里面那一层的比例大于0.9就删除
    # img_path = "C:\\Users\\young\\Desktop\\just\\2000\\TSD-Signal-00207-00000.png"
    # img_path = "C:\\Users\\young\\Desktop\\just\\2000\\messi5.png"
    save_dir = "C:\\Users\\young\\Desktop\\just\\2000-after"
    frame = cv2.imread(img_path)
    results = [["19", 0.913, (800, 270, 30, 30)], ["19", 0.8, (850, 270, 30, 30)], ["19", 0.85, (910, 270, 10, 30)]]  # 纠正红绿灯的例子
    # # results = [["19", 0.913, (800, 270, 30, 30)], ["19", 0.8, (850, 270, 30, 30)], ["10", 0.85, (1200, 345, 50, 90)]]  # 纠正13号绿牌的例子
    # # results = [["10", 0.8, (900, 320, 90, 80)], ["19", 0.8, (850, 270, 30, 30)], ["10", 0.85, (1200, 345, 50, 90)]]  #  # 纠正 蓝色中白 摄像头的 里面那一层的比例大于0.9就删除
    # results = [["10", 0.8, (539, 325, 30, 35)], ["19", 0.8, (850, 270, 30, 30)], ["10", 0.85, (1200, 345, 50, 90)]]  # # 纠正 蓝色中白 摄像头的 里面那一层的比例大于0.9就删除
    # # print(results)
    frame_copy = frame.copy()
    draw_line(frame_copy, results)
    # results = correct_all_size(frame, results)
    newResults = correct_light_box(frame, results)
    # newResults = correct_10(frame, results)  # ot "11"  yellow work man sign
    draw_line(frame, newResults)
    print("after  newResults", newResults)

