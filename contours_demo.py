import os
import cv2
from find_ColorThings import find_ColorThings
from detection import detection
from find_class_name import find_class_name


def contours_demo(number, img_path, frame, save_dir, min_s=0.7, max_s=0.93):
    k = 0
    print("def contours_demo(img_path, save_path, min_s, max_s):  >>>")

    frame = cv2.GaussianBlur(frame, (3, 3), 0)  # 高斯消除噪音
    # frame = cv2.pyrMeanShiftFiltering(frame, 15, 15)  # 神奇 但5秒处理一张图
    # frame_best = frame.copy()
    # for color in ["red",  "blue", "black", "red+blue", "green", "yellow", "green+yellow",]:  # 分别单独处理三个颜色的结果
    for color in ["red", "green", "blue", "yellow"]:  # 分别单独处理三个颜色的结果
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 直线提取
        # frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        BinColors, BinThings, contours, hierarchy = find_ColorThings(frame, color, num=0)  # num = 腐蚀的次数
        # SomeThings = cv2.pyrMeanShiftFiltering( SomeThings, 15, 15)
        #         # cv2.imshow("firt SomeThings", SomeThings)
        # SomeThings = cv2.GaussianBlur(SomeThings, (5, 5), 0)  # 高斯消除噪音
        # cv2.imshow("opencv-result", SomeThings)
        # for i, contour in enumerate(contours):  # 将所有的轮廓添加到frame上
        #     cv2.drawContours(SomeThings, contours, i, (255, 255, 255), 1)  # 最后一个数字表示线条的粗细 -1时表示填充
        # SomeBinary = cv2.bitwise_and(frame, SomeBinary)
        # contours.sort(key=lambda cnt: cv2.contourArea(cv2.convexHull(cnt)), reverse=True)
        # for i, contour in enumerate(contours):  # 将所有的轮廓添加到frame上
        #     cv2.drawContours(frame, contours, i, (0, 0, 255), 2)  # 最后一个数字表示线条的粗细 -1时表示填充
        # cv2.imshow("SomeThings", SomeThings)
        # cv2.waitKey(0)  # ********************************
        if len(contours) < 1:  # 排除不存在轮廓的情况
            # contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
            print("\n>>> Path, color, len(contours) < 1 =", len(contours))
            continue
        contours.sort(key=lambda cnt: cv2.contourArea(cv2.convexHull(cnt)), reverse=True)  # 根据轮毂的面积降序排列
        for i in range(0, len(contours)):
            print("\n>>> Path, color, i =", img_path, color, i)
            # cnt_max = max(contours, key=cv2.contourArea)  # 找到面积最大的轮廓
            # print("len(contours):", len(contours))
            if cv2.contourArea(contours[i]) < 50:  # 排除面积判断 < 50
                print(">>> cv2.contourArea(contours[%d]) < 100 :" % i, cv2.contourArea(contours[i]))
                continue
            image, flag = detection(frame, BinColors, color, contours, i)  # 判断是否是 需要识别的对象， 是返回1 否为0
            print(image)
            if flag == 1:  # 是需要的对象时
                print("666" * 50)
                k += 1
                print(img_path)

                # direct_index, name = find_class_name(image, color, min_s, max_s)  # 路灯需要这个来判断方向

                # save_path = os.path.join(save_dir, direct_index)
                # save_path = os.path.join(save_dir, color)

                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                #     os.makedirs(os.path.join(os.path.join(save_dir, str(direct_index), color)))

                # save_dir = os.path.join(save_dir, color)
                save_name = str(color) + "+" + str(number) + ".png"
                save_path = os.path.join(save_dir, save_name)
                try:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
                    cv2.imwrite(save_path, image)
                except:
                    ""


            # identify_light(SomeThings, contours[i], color, min_s, max_s)

