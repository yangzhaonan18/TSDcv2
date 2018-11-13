import cv2
import numpy as np



def cal_circleAndRect_ratio(crop_frame, color):
    # shape = "circle" or "rect"
    mask = find_mask(crop_frame, color)
    # mask = cv2.dilate(mask, None, iterations=0)  # can not set 1 or 2
    BinColors = cv2.bitwise_and(crop_frame, crop_frame, mask=mask)
    dst = cv2.GaussianBlur(BinColors, (3, 3), 0)  # 彩色图时 高斯消除噪音
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
    # cv2.imshow("gray image", gray)

    ret, BinThings = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
    # cloneImage, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 边界不是封闭的
    # cloneImage, contours, hierarchy = cv2.findContours(BinThings, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的
    BinThings, contours, hierarchy = cv2.findContours(BinThings, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的
    cv2.imshow("BinThings", BinThings)
    cv2.waitKey(0)
    # contours.sort(key=lambda cnt: cv2.contourArea(cnt), reverse=True)
    if len(contours) > 1:
        cnt_max = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(cnt_max)  # circle
        rect = cv2.minAreaRect(cnt_max)
        rect_area = rect[1][0] * rect[1][1]
        cnt_area = cv2.contourArea(cnt_max)  # area of cnt
        c_area = 3.1416 * radius * radius

        circle_ratio = cnt_area / c_area
        rect_ratio = cnt_area / rect_area
        print("cnt_area = ", cnt_area)
        print("circle_area = ", c_area)
        print("circle_ratio = cnt_area / c_area = ", circle_ratio)
        print("rect_ratio = ", rect_ratio)
        print("rect_ratio = cnt_area / rect_area = ", rect_ratio)
        # cv2.imshow("BinThings", BinThings)
        # cv2.waitKey(0)
        return circle_ratio, rect_ratio

    if len(contours) == 0:
        print("circle_ratio = 0")
        return 0, 0



def find_mask(frame, color):
    print(" def find_light_mask(frame, color): >>>")
    whiteLower = np.array([0, 0, 46])  # 白的阈值 标准H：0:180 S:0:30 V:221:255
    whiteUpper = np.array([180, 43, 255])  # white and gray

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

    blueLower = np.array([100, 80, 46])  # 蓝H:100:124 紫色H:125:155
    blueUpper = np.array([130, 255, 255])

    yellowLower = np.array([26, 80, 100])  # 黄色的阈值 标准H：26:34 S:43:255 V:46:255
    yellowUpper = np.array([34, 255, 255])  # 有的图 黄色变成红色的了
    try:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        white_mask = cv2.inRange(hsv, whiteLower, whiteUpper)  # 根据阈值构建掩膜, 红色的两个区域


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
        elif color == "white":
            mask = white_mask
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
        elif color == "red+blue+white":
            mask = red_mask + blue_mask + white_mask
        else:
            print("Input a wrong color : %f" % color)
            mask = None
        return mask

    except:
        print("Can not find mask: ", color)
        return None






if __name__ == "__main__":
    path = "C:\\Users\\young\\Desktop\\just\\2000\\rect.jpg"
    crop_frame = cv2.imread(path)
    cv2.imshow("asdf", crop_frame)
    # cv2.waitKey(0)
    color = "blue"
    a, b = cal_circleAndRect_ratio(crop_frame, color)  #circle or rect
    if a > b:
        print(">")
    else:
        print("<=")