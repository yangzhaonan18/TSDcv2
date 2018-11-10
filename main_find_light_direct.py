# -*- coding:utf-8 -*-
import cv2
import numpy as np




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
    img_path = "C:\\Users\\young\\Desktop\\just\\2000\\TSD-Signal-00205-00027.png"  # 纠正红绿灯的例子
    save_dir = "C:\\Users\\young\\Desktop\\just\\2000-after"
    frame = cv2.imread(img_path)
    results = [["19", 0.913, (800, 270, 30, 30)], ["19", 0.8, (850, 270, 30, 30)],["19", 0.85, (910, 270, 10, 30)]]  # 纠正红绿灯的例子
    frame_copy = frame.copy()
    draw_line(frame_copy, results)
    # results = correct_all_size(frame, results)
    # newResults = correct_light_box(frame, results)
    # newResults = correct_10(frame, results)  # ot "11"  yellow work man sign

    draw_line(frame, newResults)
    print("after  newResults", newResults)

