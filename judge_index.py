# -*- coding:utf-8 -*-
import cv2
import numpy as np
from cal_point import cal_point



def judge_index(ColorThings, contours, color, min_s, max_s, max_item):
    print(" def judge_index(ColorThings, contours, color, min_s, max_s, max_item): >>>")
    solidity = 0.85
    direct_index = 4
    ilter_num = 1
    while solidity > min_s and solidity < max_s and ilter_num < max_item:
        cnts = np.array(contours[0])
        # for i in range(1, len(contours)):
        #     if cv2.contourArea(contours[i]) > 25:
        #         cnts = np.insert(cnts, 0, values=contours[i], axis=0)  # 添加其他的点
        hull = cv2.convexHull(cnts)  # 轮廓转成凸包
        ColorThings_line = ColorThings.copy()
        cv2.polylines(ColorThings_line, [hull], True, (0, 0, 255), 2)  # 3.绘制凸包

        rect = cv2.minAreaRect(cnts)  # 外接矩形
        box = cv2.boxPoints(rect)

        # box = np.int0(box)
        # cv2.drawContours(ColorThings_line, [box], 0, (0, 0, 255), 2)   # 画外接矩形

        rows, cols = ColorThings_line.shape[:2]
        [vx, vy, x, y] = cv2.fitLine(cnts, cv2.DIST_L2, 0, 0.01, 0.01)
        # print("[vx, vy, x, y] :", [vx, vy, x, y])
        lefty = int((-x * vy / vx) + y)
        righty = int(((cols - x) * vy / vx) + y)
        # ColorThings_line = cv2.line(ColorThings_line, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)
        ColorThings_line = cv2.drawContours(ColorThings_line, contours, -1, (0, 255, 0), 1)  # 画边框
        ((x, y), radius) = cv2.minEnclosingCircle(cnts)  # 确定面积最大的轮廓的外接圆  返回圆心坐标和半径

        x = int(x)
        y = int(y)
        area = cv2.contourArea(cnts)  # 轮廓面积
        hull = cv2.convexHull(cnts)  # 计算出凸包形状(计算边界点)
        hull_area = cv2.contourArea(hull)  # 计算凸包面积
        solidity = float(area) / hull_area

        if solidity > max_s:
            direct_index = 0
            break
        elif solidity < min_s:
            direct_index = 4
            # cv2.imshow("%d %fimput image" % (ilter_num, solidity), ColorThings_line)
            # cv2.waitKey(0)  # ********************************
            break

        cnts_ColorThings = ColorThings.copy()
        hull_ColorThings = ColorThings.copy()
        cnts_ColorThings = cv2.drawContours(cnts_ColorThings, [cnts], -1, (255, 255, 255), -1)
        hull_ColorThings = cv2.drawContours(hull_ColorThings, [hull], -1, (255, 255, 255), -1)
        BinThings = ~cnts_ColorThings & hull_ColorThings & ~ColorThings
        direct_index = cal_point(BinThings, x, y, radius)

        font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体
        # cv2.destroyAllWindows()
        index_dict = {0: "circle", 1: "<- ", 2: "/\\", 3: "->", 4: "V"}
        cv2.putText(ColorThings_line, "%s %s %.02f" % (index_dict[direct_index], ilter_num, solidity), (5, 20), font,
                    0.8, (0, 255, 255), 2)  # 添加文字
        cv2.imshow("ColorThings_line", ColorThings_line)
        # print("solidity:", solidity)
        # print("ilter_num:", ilter_num)
        # cv2.waitKey(0)  # ********************************
        # cv2.imshow("BinThings:", BinThings)
        # cv2.waitKey(0)  # ********************************

        ilter_num += 1
        BinThings, BinColors, contours, hierarchy = find_ColorThings(ColorThings, color, num=ilter_num)
        contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
        if not contours or cv2.contourArea(contours[0]) < 5:
            break

        # cv2.imwrite(save_path, SomeBinary)  # 保存修改像素点后的图片
        # cv2.imshow("%d %fimput image" % (ilter_num, solidity), BlackThings)
        # cv2.waitKey(0)  # ********************************

    return direct_index

