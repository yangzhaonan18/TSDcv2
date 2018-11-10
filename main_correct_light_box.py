# -*- coding:utf-8 -*-
import cv2
import os
import numpy as np



def find_box(crop_frame, mask):
    BinColors = cv2.bitwise_and(crop_frame, crop_frame, mask=mask)
    # cv2.imshow("BinColors", BinColors)
    gray = cv2.cvtColor(BinColors, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
    # cv2.imshow("gray image", gray)
    ret, BinThings = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
    BinThings, contours, hierarchy = cv2.findContours(BinThings, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    cnt_max = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt_max)
    return x, y, w, h


def find_light_mask(frame):
    print(" def find_light_mask(frame, color): >>>")
    redLower01 = np.array([0, 43, 46])  # 红色的阈值 标准H：0-10 and 160-179 S:43:255 V:46:255
    redUpper01 = np.array([20, 255, 255])
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

def correct_light_box(frame, or_results):
    # [["19", 0.913, (830.6, 72.8, 22.2, 49.7)], ["19", 0.8, (990.3, 64.4, 24.0, 37.8)],["19", 0.85, (685.5, 82.4, 24.5, 52.2)]]
    light_num = ["15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]  # 交通灯的类型编号

    newResults = []
    for i in range(len(or_results)):
        newResult = []
        newResult.append(or_results[i][0])
        newResult.append(or_results[i][1])
        newResult.append(list(or_results[i][2]))
        newResults.append(newResult)
    results = newResults
    if len(results) > 0:
        for i in range(0, len(results)):
            # results[i][:] = [list(result) for result in results[i]]
            try:
                if str(results[i][0]) in light_num:
                    print("str(results[i][0]) in light_num:")
                    # print("results[i] =", results[i])
                    x1 = int(results[i][2][0] - results[i][2][2] / 2)  # 将中心点的坐标转换成 左上角的坐标
                    x2 = int(results[i][2][0] + results[i][2][2] / 2)
                    y1 = int(results[i][2][1] - results[i][2][3] / 2)
                    y2 = int(results[i][2][1] + results[i][2][3] / 2)
                    print("x1,y1,x2,y2 = ", x1, y1, x2, y2)
                    XL = 10
                    YU = 10
                    crop_frame = frame[max(y1 - XL, 0): y2 + 10,  max(x1 - YU, 0): x2 + 10]  # 上下左右都扩展10
                    mask = find_light_mask(crop_frame)
                    cv2.imshow("frame", frame)
                    cv2.waitKey(0)
                    x, y, w, h = find_box(crop_frame, mask)  # 坐标是相对于截图的坐标
                    print(" x, y, w, h",  x, y, w, h)
                    if w * h > 3:
                        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))

                        results[i][2][0] = x1 + x + w/2 - XL  # center point
                        results[i][2][1] = y1 + y + h/2 - YU
                        results[i][2][2] = w
                        results[i][2][3] = h
            except:
                continue
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

if __name__ == "__main__":
    img_path = "C:\\Users\\young\\Desktop\\just\\2000\\0885.jpg"  # 纠正红绿灯的例子
    save_dir = "C:\\Users\\young\\Desktop\\just\\2000-after"
    frame = cv2.imread(img_path)
    results = [["19", 0.913, (600, 30, 50, 50)], ["9", 0.8, (850, 270, 30, 30)], ["9", 0.85, (910, 270, 10, 30)]]  # 纠正红绿灯的例子
    print(results)
    frame_copy = frame.copy()
    draw_line(frame_copy, results)
    newResults = correct_light_box(frame, results)
    draw_line(frame, newResults)
    print("after  newResults", newResults)