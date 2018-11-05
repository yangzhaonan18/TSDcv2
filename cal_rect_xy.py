# -*- coding:utf-8 -*-


def cal_rect_xy(box):  # box是倾斜矩阵四个点的坐标
    print("def cal_rect_xy(box):   >>>")
    # # print("box:", box)  # [[310 525] [307 254] [399 253] [402 524]]
    # heigh = box[0][1] - box[1][1]
    # width = box[2][0] - box[1][0]
    # ((355.1850891113281, 389.43994140625), (92.04371643066406, 270.73419189453125), -0.7345210313796997)
    x1 = max(min(i[0] for i in box), 0)  # 外接矩形的点，可能在边框外面，即有可能出现负数。
    x2 = max(max(i[0] for i in box), 0)
    y1 = max(min(i[1] for i in box), 0)
    y2 = max(max(i[1] for i in box), 0)
    return int(x1), int(x2), int(y1), int(y2)  # 返回倾斜矩形的最小外接矩形的左上角和右下角的点坐标

