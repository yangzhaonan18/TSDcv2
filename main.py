# -*- coding:utf-8 -*-
import os
from contours_demo import contours_demo


print("*************** Python ********")
work_dir = "C:\\Users\\young\\Desktop\\just"
# img_dir = "2000"
img_dir = "TSD-Signal-00205"
save_dir = "2000-after"

img_dir = os.path.join(work_dir, img_dir)
save_dir = os.path.join(work_dir, save_dir)
img_list = os.listdir(img_dir)
number = 0
for img in img_list:
    img_path = os.path.join(img_dir, img)

    # 处理每一张图片并保存
    # save_name = os.path.splitext(img)[0] + "i" + ".jpg"
    # watershed(img_path)
    number += 1
    contours_demo(number, img_path, save_dir, min_s=0.7, max_s=0.93)


# src = cv2.imread(img_path)
# cv2.namedWindow("input image", cv2.WINDOW_AUTOSIZE)
# cv2.imshow("imput image", src)
# cv2.waitKey(0)
print("Finish")
#
# cv2.destroyAllWindows()
