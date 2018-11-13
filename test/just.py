# results = [["19", 0.913, (830.6, 72.8, 22.2, 49.7)], ["19", 0.8, (990.3, 64.4, 24.0, 37.8)],["19", 0.85, (685.5, 82.4, 24.5, 52.2)]]
# # # print(list(a))
# # newResults = []
# # for i in range(len(results)):
# #     newResult = []
# #     newResult.append(results[i][0])
# #     newResult.append(results[i][1])
# #     newResult.append(list(results[i][2]))
# #     newResults.append(newResult)
# #
# # print(results)
# # print( newResults)
# #
# # # ColorThings_line = Crop_frame.copy()
# # # cv2.polylines(ColorThings_line, [hull], True, (0, 0, 255), 2)  # 3.绘制凸包
# #
# # # rect = cv2.minAreaRect(cnts)  # 外接矩形
# # # box = cv2.boxPoints(rect)
# # # box = np.int0(box)
# # # cv2.drawContours(ColorThings_line, [box], 0, (0, 0, 255), 2)   # 画外接矩形
# #
# # # rows, cols = ColorThings_line.shape[:2]
# # # [vx, vy, x, y] = cv2.fitLine(cnts, cv2.DIST_L2, 0, 0.01, 0.01)
# # # # print("[vx, vy, x, y] :", [vx, vy, x, y])
# # # lefty = int((-x * vy / vx) + y)
# # # righty = int(((cols - x) * vy / vx) + y)
# # # # ColorThings_line = cv2.line(ColorThings_line, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)
# # # ColorThings_line = cv2.drawContours(ColorThings_line, contours, -1, (0, 255, 0), 1)  # 画边框


#
# print( 1 in [1, 2])
print("6666")

def is_in(list_a, b):
    for a in list_a:
        if a == b:
            return True
    return False



cs = [1, 2,3, 4,5, 7,8,3,4,5, 9,8,0,12,5,8,]
#
# temp_list = []
# for c in cs:
#     print(c)
#     if not is_in(temp_list, c):
#         temp_list.append(c)
#
#
#
# print(temp_list)
print("1")
print(cs.remove(1))