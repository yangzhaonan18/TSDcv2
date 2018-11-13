# -*- coding:utf-8 -*-
import os
import cv2
import math
import numpy as np



def find_mask(frame, color):
    print(" def find_mask(frame, color): >>>")
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
        elif color == "yellow+green":
            mask = yellow_mask + green_mask
        elif color == "red+yellow+green":
            mask = red_mask + yellow_mask + green_mask
        else:
            mask = None
        return mask

    except:
        return None



def find_color_aera(Crop_frame, color):
    try:
        mask = find_mask(Crop_frame, color)
        # mask = cv2.dilate(mask, None, iterations=1)  # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
        # mask = cv2.erode(mask, None, iterations=num)  # 腐蚀操作
        BinColors = cv2.bitwise_and(Crop_frame, Crop_frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
        dst = cv2.GaussianBlur(BinColors, (3, 3), 0)  # 彩色图时 高斯消除噪音
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)  # 转成灰色图像

        ret, BinThings = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
        BinThings, contours, hierarchy = cv2.findContours(BinThings, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的
        cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
        color_aera = cv2.contourArea(cnt_max)
        return color_aera
    except:
        return 0.0


def judge_color(Crop_frame):
    yellow_area = find_color_aera(Crop_frame, "yellow")
    red_area = find_color_aera(Crop_frame, "red")
    green_area = find_color_aera(Crop_frame, "green")
    # print("yellow_area,  red_area, green_area = ", yellow_area,  red_area, green_area)
    if yellow_area > red_area and yellow_area > green_area:
        return "yellow"
    if red_area > yellow_area and red_area > green_area:
        return "red"
    if green_area > yellow_area and green_area > red_area:
        return "green"
    else:
        return None



def judge_light_type(Crop_frame):
    color = judge_color(Crop_frame)
    direction = judge_direction(Crop_frame)
    if color == "red" and direction == "R":
        return "15"
    elif color == "green" and direction == "R":
        return "16"
    elif color == "yellow" and direction == "R":
        return "17"
    elif color == "red" and direction == "D":
        return "18"
    elif color == "green" and direction == "D":
        return "19"
    elif color == "yellow" and direction == "D":
        return "20"
    elif color == "red" and direction == "L":
        return "21"
    elif color == "green" and direction == "L":
        return "22"
    elif color == "yellow" and direction == "L":
        return "23"
    elif color == "red" and direction == "C":
        return "24"
    elif color == "green" and direction == "C":
        return "25"
    elif color == "yellow" and direction == "C":
        return "26"
    else:
        return "27"





def cal_circle_xy(frame, x, y, radius):
    print("def cal_circle_xy(frame, x, y, radius):  >>>")
    x1 = x - radius if x - radius > 0 else 0
    x2 = x + radius if x + radius < frame.shape[1] else frame.shape[1]  # cv里面横坐标是x 是shape[1]
    y1 = y - radius if y - radius > 0 else 0
    y2 = y + radius if y + radius < frame.shape[0] else frame.shape[0]  # cv里面纵坐标是y 是shape[0]
    return int(x1), int(x2), int(y1), int(y2)




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
    if SS10 > SS00 + SS01 + SS11 or SS11 > SS00 + SS01 + SS10:
        return "D"  # direct # 图形有空缺的时候
    elif SS01 in value[0:2] and SS11 in value[0:2]:  # 箭头右侧需要补齐的东西多
        return "L"  # left
    elif SS10 in value[0:2] and SS11 in value[0:2]:
        return "D"  # direct
    elif SS00 in value[0:2] and SS10 in value[0:2]:
        return "R"  # right
    else:
        return "X"  # circle


def find_cnt(Crop_frame, mask):
    try:
        mask = cv2.dilate(mask, None, iterations=1)
        BinColors = cv2.bitwise_and(Crop_frame, Crop_frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
        dst = cv2.GaussianBlur(BinColors, (3, 3), 0)  # 彩色图时 高斯消除噪音
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
        ret, BinThings = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
        BinThings, contours, hierarchy = cv2.findContours(BinThings, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的
        cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
        return cnt_max
    except:
        return None


def judge_direction(Crop_frame):  # 判断方向
    size = 100
    Crop_frame = cv2.resize(Crop_frame, (size, int(size * Crop_frame.shape[0] / Crop_frame.shape[1])), interpolation=cv2.INTER_CUBIC)
    # cv2.imshow("judge_direction//Crop_frame", Crop_frame)
    # cv2.waitKey(0)
    mask = find_mask(Crop_frame, "red+yellow+green")
    mask = cv2.erode(mask, None, iterations=5)  # 腐蚀操作
    cnt_max = find_cnt(Crop_frame, mask)

    solidity = 0.85
    direction = "D"
    ilter_num = 1
    min_s = 0.8
    max_s = 0.95  #
    max_item = 4
    while solidity > min_s and solidity < max_s and ilter_num < max_item:
        try:
            cnts = np.array(cnt_max)
            # cnts = cnt_max
            ((x, y), radius) = cv2.minEnclosingCircle(cnts)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径
        except:
            break
        x = int(x)
        y = int(y)
        area = cv2.contourArea(cnts)  # 轮廓面积
        hull = cv2.convexHull(cnts)  # 计算出凸包形状(计算边界点)
        hull_area = cv2.contourArea(hull)  # 计算凸包面积
        solidity = float(area) / hull_area
        print("solidity = ", solidity)
        if solidity > max_s:
            direction = "C"  # circle
            break
        elif solidity < min_s:
            direction = "D"  # others type not light
            break
        cnts_ColorThings = Crop_frame.copy()
        hull_ColorThings = Crop_frame.copy()
        cnts_ColorThings = cv2.drawContours(cnts_ColorThings, [cnts], -1, (255, 255, 255), -1)
        hull_ColorThings = cv2.drawContours(hull_ColorThings, [hull], -1, (255, 255, 255), -1)
        BinThings = ~cnts_ColorThings & hull_ColorThings & ~Crop_frame
        direction = cal_point(BinThings, x, y, radius)
        ilter_num += 1

        cnt_max = find_cnt(Crop_frame, mask)
        if cv2.contourArea(cnt_max) < size * size / 5:
            break
    return direction


def cal_wh_ratio(cnt):
    x, y, w, h = cv2.boundingRect(cnt)  # 外接矩形
    wh_rat = int(max(w / h, h / w))
    if w > h:
        return [0, wh_rat, [x, y, w, h]]
    else:
        return [1, wh_rat, [x, y, w, h]]


def detection_light(BinColors, color, contours, i):
    print("def detection(frame, BinColors, color, contours, i):   >>>")
    BinColors_show = BinColors.copy()
    cv2.drawContours(BinColors_show, contours, i, (0, 255, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充
    wh_ratio = cal_wh_ratio(contours[i])  # 返回轮廓的比例 [1,判断外接矩形的长宽比例   不应该很大
    if not wh_ratio:
        return None

    cnt_max = contours[i]
    cnt_area = cv2.contourArea(cnt_max)  # 轮廓的面积 ？ 不能使用这个参数 判断不直观
    hull = cv2.convexHull(cnt_max)  # 计算出凸包形状(计算边界点)
    hull_area = cv2.contourArea(hull)  # 计算凸包面积
    (x, y), radius = cv2.minEnclosingCircle(cnt_max)
    circle_area = math.pi * radius * radius
    x, y, w, h = cv2.boundingRect(cnt_max)  # 正外接矩形
    if hull_area == 0:
        print("cal_ratio // hull_area == 0")
        return None
    # color_ratio = float(color_area) / hull_area  # 轮廓中某种颜色的面积与 凸包面积的比值
    cnt_ratio = float(cnt_area) / hull_area  # 凸包度 轮廓面积/凸包面积
    rect_ratio = float(cnt_area) / (w * h)  # 矩形度   轮廓面积与最小外接矩形的比值  用于区分是否是规则图形
    circle_ratio = float(cnt_area) / circle_area  # 圆形度
    # print("cal_ratio // color_ratio", color_ratio)
    print("cnt_area =", cnt_area)
    print("w * h =", w * h)
    print("circle_area =", circle_area)
    print("cal_ratio // cnt_ratio", cnt_ratio)
    print("cal_ratio // rect_ratio", rect_ratio)
    print("cal_ratio // circle_ratio", circle_ratio)
    print("wh_ratio = ", wh_ratio)

    if wh_ratio[1] == 1 and wh_ratio[2][2] > 3 and wh_ratio[2][2] < 100 and w / h < 1.3 and circle_ratio > 0.3:  # 尺寸要求
        if ((circle_ratio >= rect_ratio or (w < h and circle_ratio > 0.7))and w >= 20) or (w > 3 and w < 20):  # 大一点的图标要求圆形度大于矩形度
            if color == "red":
                print(">>> a red  light" * 10)
                print("wh_ratio == ", wh_ratio)
                # cv2.waitKey(0)
                return ["15", 1, [wh_ratio[2][0], wh_ratio[2][1], wh_ratio[2][2], wh_ratio[2][3]]]
            if color == "yellow":
                print(">>> a yellow light" * 10)
                print("wh_ratio == ", wh_ratio)
                # cv2.waitKey(0)
                return ["16", 1, [wh_ratio[2][0], wh_ratio[2][1], wh_ratio[2][2], wh_ratio[2][3]]]
            if color == "green":
                print(">>> a green light" * 10)
                print("wh_ratio == ", wh_ratio)
                # cv2.waitKey(0)
                return ["17", 1, [wh_ratio[2][0], wh_ratio[2][1], wh_ratio[2][2], wh_ratio[2][3]]]
            else:
                return None
    else:
        return None





def find_light_mask(frame, color):
    print("def find_light_mask(frame, color): >>> = ", color)
    redLower01 = np.array([0, 125, 120])  # 红色的阈值 标准H：0-10 and 160-179 S:43:255 V:46:255
    redUpper01 = np.array([10, 255, 255])
    redLower02 = np.array([156, 125, 120])  # 125 to 156
    redUpper02 = np.array([155, 255, 255])

    greenLower = np.array([50, 125, 100])  # 绿色的阈值 标准H：35:77 S:43:255 V:46:255
    greenUpper = np.array([95, 255, 255])  # V 60 调整到了150

    yellowLower = np.array([26, 125, 100])  # 黄色的阈值 标准H：26:34 S:43:255 V:46:255
    yellowUpper = np.array([34, 255, 255])  # 有的图 黄色变成红色的了
    # try:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red1_mask = cv2.inRange(hsv, redLower01, redUpper01)  # 根据阈值构建掩膜, 红色的两个区域
    red2_mask = cv2.inRange(hsv, redLower02, redUpper02)
    red_mask = red1_mask + red2_mask

    yellow_mask = cv2.inRange(hsv, yellowLower, yellowUpper)  # 根据阈值构建掩膜, 黄色的区域
    green_mask = cv2.inRange(hsv, greenLower, greenUpper)  # 根据阈值构建掩膜, 绿色的区域

    if color == "yellow":
        mask = yellow_mask
    elif color == "red":
        mask = red_mask
    elif color == "green":
        mask = green_mask
        # print(mask)
    else:
        mask = None
        print("Input color is wrong !!! input again !")
    return mask
    # except:
    #     return None




def find_ColorThings(frame, color, num=0, RETR=cv2.RETR_EXTERNAL):  # 默认返回最外层的轮廓
    print("def find_ColorThings(frame, color, num=0, RETR=cv2.RETR_EXTERNAL): >>>")
    mask = find_light_mask(frame, color)

    mask = cv2.dilate(mask, None, iterations=2)  # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    mask = cv2.erode(mask, None, iterations=num)  # 腐蚀操作
    BinColors = cv2.bitwise_and(frame, frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
    # an_ColorThings = cv2.bitwise_not(frame, frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
    # cv2.imshow("an_ColorThings:", BinColors)
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




def find_light_box(frame):
    boxs = []
    for color in ["red", "green", "yellow"]:  # 分别单独处理三个颜色的结果
        frame = cv2.GaussianBlur(frame, (3, 3), 0)  # 高斯消除噪音
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 直线提取
        # frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))  # 黑白图时 直线消除 小斑点
        # frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)  # 输出是二值化的图片， 后面用来作为轮廓使用 吧！！！！！
        try:
            BinColors, BinThings, contours, hierarchy = find_ColorThings(frame, color, num=0)  # num = 腐蚀的次数
            contours.sort(key=lambda cnt: cv2.contourArea(cv2.convexHull(cnt)), reverse=True)  # 根据轮毂的面积降序排列
            # contours.sort(key=lambda cnt: cv2.boundingRect(cnt)[1])  # 根据轮廓从上往往下排序
            for i in range(0, len(contours)):
                # print("\n>>> Path, color, i =", img_path, color, i)
                # cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
                # print("len(contours):", len(contours))
                area = cv2.contourArea(contours[i])
                if area < 25 or area > 3000:  # 排除面积判断 < 50
                    print(">>> cv2.contourArea(contours[%d]) < 20 :" % i, cv2.contourArea(contours[i]))
                    continue
                box = detection_light(BinColors, color, contours, i)  # 返回当前轮廓的坐标和类型
                print("box = ", box)
                # cv2.imshow("BinColors", BinColors)
                # cv2.waitKey(0)
                if box:  # 是需要的对象时
                    boxs.append(box)
        except:
            continue

    boxs = sorted(boxs, key=lambda box: box[2][1])  # 从上往下排序
    print("all boxs =" * 30)
    print(boxs)

    for box in boxs:
        if min(box[2][2], box[2][2]) < 8:
            boxs.remove(box)
    or_boxs = boxs.copy()

    # return or_boxs    # 6666666666666666666666666666666666666666666666666666666666666666666

    boxs = or_boxs[:4]
    x_error = 19

    print(boxs)
    if len(boxs) == 4:
        print("len(boxs) == 4 1 :")
        boxs_cp = boxs.copy()
        boxs_cp = sorted(boxs_cp, key=lambda box: box[2][2], reverse=True)  # by size
        del boxs_cp[0]
        boxs_cp = sorted(boxs_cp, key=lambda box: box[2][0])  # by x and  保证另外三个等间距时，删除其中最大的那个
        distance_x1 = abs(boxs_cp[1][2][0] - boxs_cp[0][2][0])
        distance_x2 = abs(boxs_cp[2][2][0] - boxs_cp[1][2][0])
        distance_y1 = abs(boxs_cp[1][2][1] - boxs_cp[0][2][1])
        distance_y2 = abs(boxs_cp[2][2][1] - boxs_cp[1][2][1])
        print("distance_x1, distance_x2 = ", distance_x1, distance_x2)
        print("distance_y1, distance_y2 = ", distance_y1, distance_y2)
        if abs(distance_x2 - distance_x1) < x_error and abs(distance_y2 - distance_y1) < 10 and distance_x1 > 40 and distance_x2 > 40 and distance_x1 < 300 and distance_y2 < 10:
            return boxs_cp[:3]

    boxs = or_boxs[:4]
    print(boxs)
    if len(boxs) == 4:
        print("len(boxs) == 4 2 :")
        boxs_cp = boxs.copy()
        boxs_cp = sorted(boxs_cp, key=lambda box: box[2][0])  # by size
        del boxs_cp[0]
        boxs_cp = sorted(boxs_cp, key=lambda box: box[2][0])  # by x and  保证另外三个等间距时，删除其中最大的那个
        distance_x1 = abs(boxs_cp[1][2][0] - boxs_cp[0][2][0])
        distance_x2 = abs(boxs_cp[2][2][0] - boxs_cp[1][2][0])
        distance_y1 = abs(boxs_cp[1][2][1] - boxs_cp[0][2][1])
        distance_y2 = abs(boxs_cp[2][2][1] - boxs_cp[1][2][1])
        print("distance_x1, distance_x2 = ", distance_x1, distance_x2)
        print("distance_y1, distance_y2 = ", distance_y1, distance_y2)
        if abs(distance_x2 - distance_x1) < x_error and abs(distance_y2 - distance_y1) < 10 and distance_x1 > 30 and distance_x1 < 300 and distance_y2 < 10:
            return boxs_cp[:3]

    boxs = or_boxs[:4]
    print(boxs)
    if len(boxs) == 4:
        print("len(boxs) == 4 3 :")
        boxs_cp = boxs.copy()
        boxs_cp = sorted(boxs_cp, key=lambda box: box[2][0])  # by size
        del boxs_cp[-1]
        boxs_cp = sorted(boxs_cp, key=lambda box: box[2][0])  # by x and  保证另外三个等间距时，删除其中最大的那个
        distance_x1 = abs(boxs_cp[1][2][0] - boxs_cp[0][2][0])
        distance_x2 = abs(boxs_cp[2][2][0] - boxs_cp[1][2][0])
        distance_y1 = abs(boxs_cp[1][2][1] - boxs_cp[0][2][1])
        distance_y2 = abs(boxs_cp[2][2][1] - boxs_cp[1][2][1])
        print("distance_x1, distance_x2 = ", distance_x1, distance_x2)
        print("distance_y1, distance_y2 = ", distance_y1, distance_y2)
        if abs(distance_x2 - distance_x1) < x_error and abs(distance_y2 - distance_y1) < 10 and distance_x1 > 30 and distance_x1 < 300 and distance_x2 > 30 and distance_x2 < 300 and distance_y2 < 10:
            return boxs_cp[:3]




    boxs = or_boxs[:3]
    if len(boxs) == 3:
        print("len(boxs) == 3 1:")
        boxs_cp = boxs.copy()
        boxs_cp = sorted(boxs_cp, key=lambda box: box[2][0], reverse=True)  # left to right by x
        distance_x1 = abs(boxs_cp[1][2][0] - boxs_cp[0][2][0])
        distance_x2 = abs(boxs_cp[2][2][0] - boxs_cp[1][2][0])
        distance_y1 = abs(boxs_cp[1][2][1] - boxs_cp[0][2][1])
        distance_y2 = abs(boxs_cp[2][2][1] - boxs_cp[1][2][1])

        area_01 = int(boxs_cp[0][2][2] * boxs_cp[0][2][3] / (boxs_cp[1][2][2] * boxs_cp[1][2][3]) + 0.5)
        area_02 = int(boxs_cp[1][2][2] * boxs_cp[1][2][3] / (boxs_cp[0][2][2] * boxs_cp[0][2][3]) + 0.5)
        area_bi = max(area_01, area_02)

        if abs(distance_x2 - distance_x1) < x_error and abs(distance_y2 - distance_y1) < 10 and distance_x1 > 30 and distance_x2 > 30 and distance_x1 < 200 and distance_y2 < 10 and area_bi == 1:
            return boxs_cp[:3]

    boxs = or_boxs[:3]
    if len(boxs) == 3:
        print("len(boxs) == 3 2 :")
        boxs_cp = boxs.copy()
        boxs_cp = sorted(boxs_cp, key=lambda box: box[2][2], reverse=True)  # by size
        del boxs_cp[0]
        distance_x1 = abs(boxs_cp[1][2][0] - boxs_cp[0][2][0])
        # distance_x2 = abs(boxs_cp[2][2][0] - boxs_cp[1][2][0])
        distance_y1 = abs(boxs_cp[1][2][1] - boxs_cp[0][2][1])
        # distance_y2 = abs(abs(boxs_cp[2][2][1] - boxs_cp[1][2][1]))
        area_01 = int(boxs_cp[0][2][2] * boxs_cp[0][2][3] / (boxs_cp[1][2][2] * boxs_cp[1][2][3]) + 0.5)
        area_02 = int(boxs_cp[1][2][2] * boxs_cp[1][2][3] / (boxs_cp[0][2][2] * boxs_cp[0][2][3]) + 0.5)
        area_bi = max(area_01, area_02)
        print("area_bi == 1", area_bi)
        if abs(distance_x2 - distance_x1) < x_error and abs(distance_y2 - distance_y1) < 10 and distance_x1 > 30 and distance_x1 < 200 and distance_y1 < 10 and area_bi == 1:
            print("len(boxs) == 3:")
            return boxs_cp[:2]

    boxs = or_boxs[:3]
    if len(boxs) == 3:
        print("len(boxs) == 3 3 :")
        boxs_cp = boxs.copy()
        boxs_cp = sorted(boxs_cp, key=lambda box: box[2][0], reverse=True)  # 删除右边那个
        del boxs_cp[-1]
        distance_x1 = boxs_cp[1][2][0] - boxs_cp[0][2][0]
        # distance_x2 = boxs_cp[2][2][0] - boxs_cp[1][2][0]
        distance_y1 = abs(boxs_cp[1][2][1] - boxs_cp[0][2][1])
        # distance_y2 = abs(boxs_cp[2][2][1] - boxs_cp[1][2][1])
        area_01 = int(boxs_cp[0][2][2] * boxs_cp[0][2][3] / (boxs_cp[1][2][2] * boxs_cp[1][2][3]) + 0.5)
        area_02 = int(boxs_cp[1][2][2] * boxs_cp[1][2][3] / (boxs_cp[0][2][2] * boxs_cp[0][2][3]) + 0.5)
        area_bi = max(area_01, area_02)
        print("area_bi == 1", area_bi)
        if distance_x1 > 30 and distance_x1 < 200 and distance_y1 < 10 and area_bi == 1:
            print("len(boxs) == 3:")
            return boxs_cp[:2]

    boxs = or_boxs[:3]
    if len(boxs) == 3:
        print("len(boxs) == 3 4:")
        boxs_cp = boxs.copy()
        boxs_cp = sorted(boxs_cp, key=lambda box: box[2][0], reverse=True)  # by size  x 删除三个中 最左边的那个
        del boxs_cp[0]
        distance_x1 = boxs_cp[1][2][0] - boxs_cp[0][2][0]
        # distance_x2 = boxs_cp[2][2][0] - boxs_cp[1][2][0]
        distance_y1 = abs(boxs_cp[1][2][1] - boxs_cp[0][2][1])
        # distance_y2 = abs(boxs_cp[2][2][1] - boxs_cp[1][2][1])
        area_01 = int(boxs_cp[0][2][2] * boxs_cp[0][2][3] / (boxs_cp[1][2][2] * boxs_cp[1][2][3]) + 0.5)
        area_02 = int(boxs_cp[1][2][2] * boxs_cp[1][2][3] / (boxs_cp[0][2][2] * boxs_cp[0][2][3]) + 0.5)
        area_bi = max(area_01, area_02)
        print("area_bi == 1", area_bi)
        if distance_x1 > 30 and distance_x1 < 200 and distance_y1 < 10 and area_bi == 1:
            print("len(boxs) == 3:")
            return boxs_cp[:2]



    boxs = or_boxs[:2]
    if len(boxs) == 2:
        print("len(boxs) == 2 1:")
        boxs_cp = boxs.copy()
        boxs_cp = sorted(boxs_cp, key=lambda box: box[2][2], reverse=True)  # by x
        # del boxs_cp[0]
        distance_x1 = abs(boxs_cp[1][2][0] - boxs_cp[0][2][0])
        # distance_x2 = boxs_cp[2][2][0] - boxs_cp[1][2][0]
        distance_y1 = abs(boxs_cp[1][2][1] - boxs_cp[0][2][1])
        # distance_y2 = abs(boxs_cp[2][2][1] - boxs_cp[1][2][1])
        area_01 = int(boxs_cp[0][2][2] * boxs_cp[0][2][3] / (boxs_cp[1][2][2] * boxs_cp[1][2][3]) + 0.5)
        area_02 = int(boxs_cp[1][2][2] * boxs_cp[1][2][3] / (boxs_cp[0][2][2] * boxs_cp[0][2][3]) + 0.5)
        area_bi = max(area_01, area_02)
        print("afasd")
        print(distance_x1 )
        print(distance_y1)
        print(area_bi)
        if distance_x1 > 35 and distance_x1 < 250 and distance_y1 < 10 and int(area_bi) == 1:
            return boxs_cp[:2]
        else:
            print("Dissatisfaction")
    # boxs = sorted(boxs, key=lambda box: box[2][1])

    print("retu rn None")

    return None


def dectect_light(frame):
    frame = frame[0:400, 0:1280]
    boxs = find_light_box(frame)  # return box of light

    if boxs:
        frame_show = frame.copy()
        for box in boxs[:]:
            Crop_frame = frame_show[int(box[2][1]):int(box[2][1] + box[2][3]), int(box[2][0]):int(box[2][0] + box[2][2])]
            light_type = judge_light_type(Crop_frame)
            box[0] = light_type  # update light
        count = 0
        for box in boxs:
            if box[0] == "27":
                count += 1
        if count >= 2:
            return None
        for box in boxs:
            box[2][0] = box[2][0] + box[2][2]/2 + 0.5
            box[2][1] = box[2][1] + box[2][3]/2 + 0.5
        return boxs  # box with type




if __name__ == "__main__":

    # img_path = "C:\\Users\\young\\Desktop\\TSD-Signal\\TSD-Signal-00207"
    # names = os.listdir(img_path)
    # for name in names:
    #     print("name = " * 88)
    #     print(name)
    #     img_path = os.path.join(img_path, name)
    #

    img_path = "C:\\Users\\young\\Desktop\\TSD-Signal\\TSD-Signal-00207\\TSD-Signal-00207-00008.png"
    # img_path = "C:\\Users\\young\\Desktop\\just\\2000\\TSD-Signal-00207-00002.png"
    save_dir = "C:\\Users\\young\\Desktop\\just\\2000-after"
    frame = cv2.imread(img_path)
    frame = frame[0:1024, 0:1280]   # Upper part
    # print(frame.shape)
    # frame = cv2.GaussianBlur(frame, (3, 3), 0)  # 高斯消除噪音
    # contours_demo(number, img_path, frame, save_dir)
    #  在图片中找到红色的目标并返回 编号和坐标
    boxs = find_light_box(frame)  # return box
    if boxs:

        # print("Final box_list = ", boxs)

        # print("before = ", boxs)
        frame_show = frame.copy()
        for box in boxs[:]:
            font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体
            Crop_frame = frame[int(box[2][1]):int(box[2][1] + box[2][3]), int(box[2][0]):int(box[2][0] + box[2][2])]
            # cv2.imshow("Crop_frame", cv2.resize(Crop_frame, (100, 100)))
            # cv2.waitKey(0)
            # judge_index(Crop_frame)
            light_type = judge_light_type(Crop_frame)  # return type
            print("light_type", light_type)
            box[0] = light_type
            cv2.rectangle(frame_show, (int(box[2][0]), int(box[2][1])),
                          (int(box[2][0] + box[2][2]), int(box[2][1] + box[2][3])),
                          (0, 0, 255), 2)
            cv2.putText(frame_show, light_type, (int(box[2][0]), int(box[2][1]) + 50), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), lineType=cv2.LINE_AA)
            cv2.imshow("Final frame_show :", frame_show)



    box2 = dectect_light(frame)  # return box and type
    print("Final box2222 removx 27 type= ", box2)
    cv2.waitKey(0)
