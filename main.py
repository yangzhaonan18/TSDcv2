# -*- coding:utf-8 -*-
import cv2
import numpy as np
from collections import deque
import os
import cv2

from contours_demo import contours_demo




print("if __name__ == \"__main__\":  >>>")
print("*************** Python ********")
work_dir = "C:\\Users\\young\\Desktop\\just"
# img_dir = "2000"
img_dir = "TSD-Signal-00268"
save_dir = "2000-after"

img_dir = os.path.join(work_dir, img_dir)
save_dir = os.path.join(work_dir, save_dir)
img_list = os.listdir(img_dir)

for img in img_list:
    img_path = os.path.join(img_dir, img)
    save_name = os.path.splitext(img)[0] + ".png"
    save_path = os.path.join(save_dir, save_name)
    # 处理每一张图片并保存

    # watershed(img_path)
    ans = contours_demo(img_path, save_path, min_s=0.7, max_s=0.93)
    print("ans")

# src = cv2.imread(img_path)
# cv2.namedWindow("input image", cv2.WINDOW_AUTOSIZE)
# cv2.imshow("imput image", src)
# cv2.waitKey(0)
print("Finish")
#
# cv2.destroyAllWindows()
