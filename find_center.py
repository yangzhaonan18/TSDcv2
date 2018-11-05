# -*- coding:utf-8 -*-


def find_center(CropThing, center, direction, part=0.1):
    """
    :param CropThing:
    :param center:列表
    :param direction:  0 横向 1 纵向
    :return:
    """
    radius = float("inf")
    if len(center) > 1:  # 处理检测到多个圆的情况，查看是否中间有漏检
        center = sorted(center, key=lambda x: x[direction])  # 升序排列
        print("sorted center", center)
        # radius = int((center[-1][0] - center[0][0]) / (2 * (len(contours) - 1)))  # 中间有缺点时，不能使用
        for i in range(1, len(center)):  # 找到的两个圆心的最近距离/2
            if (center[i][direction] - center[i-1][direction]) / 2 < radius:
                radius = int((center[i][direction] - center[i-1][direction]) / 2)

        num = int(2 * radius / min(CropThing.shape[0], CropThing.shape[1]) + 0.5)  # 转成四舍五入 调成0.纠正一点图片尺寸带来的误差
        # 判断这个变径是否是对的，num = 1表示对，=2表示中间有一个圆的空隙，=3表示有两个圆的间隙

        radius = int(radius / num)  # 纠正误有漏检圆的半径值
        radius = min(radius, CropThing.shape[0] / 2, CropThing.shape[1] / 2)

        for i in range(1, len(center)):  # 查找任意两个圆中间存在空缺圆的情况
            if (center[i][direction] - center[i-1][direction]) > int(3 * radius) and (center[i][direction] - center[i-1][
                direction]) < int( 5 * radius):  # 这是中间空缺一个圆的情况
                center.insert(i, (int((center[i][0] + center[i-1][0]) / 2), int((center[i][1] + center[i-1][1]) / 2)))
            elif (center[i][direction] - center[i-1][direction]) > int(5 * radius) and (center[i][direction] - center[i-1][
                direction]) < int(7 * radius):  # 这是中间连续空缺两个个圆的情况
                center.insert(i, (center[i][direction] - 2 * radius - 1, int((center[i][1 ^ direction] + center[i - 1][1 ^ direction]) / 2)))
                center.insert(i, (center[i][direction] - 2 * radius - 1, int((center[i][1 ^ direction] + center[i - 1][1 ^ direction]) / 2)))

    if len(center) == 1:  # 只检测到一个圆，但长宽比不是一的情况，漏检了周围的圆
        radius = int(min(CropThing.shape[0] / 2, CropThing.shape[1] / 2)) - 1
        print("len(center) == 1,  radius= ", radius)

    flag01 = False
    flag02 = False
    while not(flag01 and flag02):  # 两个flag都是true的时候停止循环添加。（程序技巧，先写里面在写判断条件）
        print(direction)
        if center[0][direction] - radius > 2 * part * radius:  # 左边有大半圆的话
            if direction == 0:  # 横向 左边缺
                center.insert(0, (center[0][direction] - 2 * radius, center[0][1 ^ direction]))
            else:  # 横向 右边缺
                center.insert(0, (center[0][1 ^ direction], center[0][direction] - 2 * radius))
        else:
            flag01 = True
        if CropThing.shape[1 ^ direction] - center[-1][direction] - radius > 2 * part * radius:  # 右边有大半圆的话
            if direction == 0:  # 纵向 上边缺
                center.append((center[-1][direction] + 2 * radius, center[-1][1 ^ direction]))
            else:  # 纵向 下边缺
                center.append((center[-1][1 ^ direction], center[-1][direction] + 2 * radius))
        else:
            flag02 = True


    print("after:", center)
    return center, radius
