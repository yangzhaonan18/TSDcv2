from find_ColorThings  import find_ColorThings
from find_center import find_center
import cv2
import numpy as np


def find_crop_center(CropThing, color):
    print("def find_crop_center(CropThing, color):  >>>")
    try:
        CropThing_show = CropThing.copy()
        BinThings, BinColors, contours, hierarchy = find_ColorThings(CropThing, color, num=0)
        i = contours.index(max(contours, key=cv2.contourArea))  # 列表最大数的 索引
        # contours[i] = cv2.convexHull(contours[i])  # 不能是引用外包的填充方法，外面的线条会干扰 凸包的生成
        img01 = cv2.drawContours(BinThings, contours, i, (0, 0, 255), -1)
        cv2.imshow("BinThings -1 ", img01)

        img01 = cv2.cvtColor(img01, cv2.COLOR_BGR2GRAY)
        dist = cv2.distanceTransform(img01, cv2.DIST_L2, 3)  # 单通道灰度图才可以转化成 彩色图不行
        dist_output = cv2.normalize(dist, 0, 1.0, cv2.NORM_MINMAX)
        cv2.imshow("distance-t", dist_output * 50)

        # ret, surface = cv2.threshold(dist, 1, dist.max()*0.5, cv2.THRESH_BINARY)
        ret, surface = cv2.threshold(dist, dist.max() * 0.8, 255, cv2.THRESH_BINARY)  # 只保留中心点周围的图
        cv2.imshow("surface", surface)
        surface_fg = np.uint8(surface)
        BinThings, contours, hierarchy = cv2.findContours(surface_fg, cv2.RETR_EXTERNAL,
                                                          cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的
        print("len(contours) = ", len(contours))
        x_list = []  # 中心的x坐标
        y_list = []  # 中心的y坐标
        center = []  # 中心的坐标


        for k in range(len(contours)):
            cnt = contours[k]
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            x_list.append(cx)
            y_list.append(cy)
            center.append((cx, cy))
        print("before center is :", center)
        part = 0.5  # 边缘部分比例大于part的都需要找出（返回中心坐标和半径）
        print(CropThing.shape)
        if CropThing.shape[0] < CropThing.shape[1]:  # 横向有多个图标，找到半径
            print(" heng " * 10)
            center, radius = find_center(CropThing, center, direction=0)
            print("center: ", center)

        elif CropThing.shape[0] > CropThing.shape[1]:
            print(" shu " * 10)
            center, radius = find_center(CropThing, center, direction=1)
            print("center: ", center)

        else:
            print("after len(contours) = 1")
            radius = []

        for i in range(len(center)):
            cv2.circle(CropThing_show, center[i], int(radius), (0, 0, 255), 2)  # 画圆
        cv2.imshow("CropThing_show", CropThing_show)
        print("after center is :", center)
        return CropThing_show, center, radius

    except:
        return None, [], -1

