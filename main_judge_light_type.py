
import cv2
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

    yellowLower = np.array([26, 43, 46])  # 黄色的阈值 标准H：26:34 S:43:255 V:46:255
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




def cal_circle_xy(frame, x, y, radius):
    print("def cal_circle_xy(frame, x, y, radius):  >>>")
    x1 = x - radius if x - radius > 0 else 0
    x2 = x + radius if x + radius < frame.shape[1] else frame.shape[1]  # cv里面横坐标是x 是shape[1]
    y1 = y - radius if y - radius > 0 else 0
    y2 = y + radius if y + radius < frame.shape[0] else frame.shape[0]  # cv里面纵坐标是y 是shape[0]
    return int(x1), int(x2), int(y1), int(y2)



def cal_point(SomeBinary, x, y, radius):  # 返回最大方向的编号int
    cv2.imshow("SomeBinary", SomeBinary)
    cv2.waitKey(0)
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
    # if SS10 > SS00 + SS01 + SS11 or SS11 > SS00 + SS01 + SS10:
    #     return "D"  # direct # 图形有空缺的时候
    if SS01 in value[0:2] and SS11 in value[0:2]:  # 箭头右侧需要补齐的东西多
        return "L"  # left
    elif SS10 in value[0:2] and SS11 in value[0:2]:
        return "D"  # direct
    elif SS00 in value[0:2] and SS10 in value[0:2]:
        return "R"  # right
    else:
        return "D"  # circle


def find_cnt(Crop_frame, mask):
    try:
        mask = cv2.dilate(mask, None, iterations=1)
        BinColors = cv2.bitwise_and(Crop_frame, Crop_frame, mask=mask)  # 提取感兴趣的颜色区域  背景黑色+彩色的图像
        dst = cv2.GaussianBlur(BinColors, (3, 3), 0)  # 彩色图时 高斯消除噪音
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)  # 转成灰色图像
        ret, BinThings = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 灰色图像二值化（变黑白图像）
        BinThings, contours, hierarchy = cv2.findContours(BinThings, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 边界是封闭的
        cv2.imshow("B", BinThings)
        cv2.waitKey(0)
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
    # mask = cv2.erode(mask, None, iterations=5)  # 腐蚀操作
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






if __name__ == "__main__":
    # img_path = "C:\\Users\\young\\Desktop\\TSD-Signal\\TSD-Signal-00207\\TSD-Signal-00207-00008.png"
    img_path = "C:\\Users\\young\\Desktop\\just\\2001\\23.jpg"
    frame = cv2.imread(img_path)
    # frame = frame[200:250, 630:650]   # Upper part
    cv2.imshow("frame :", frame)
    cv2.waitKey(0)
    box2 = judge_light_type(frame)  # return box and type
    print("Final box2222 removx 27 type= ", box2)


