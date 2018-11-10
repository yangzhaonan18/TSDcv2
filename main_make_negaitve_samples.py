import os
import cv2
import random

dir = "C:\\Users\\young\\Desktop\\test1031\\before\\base"
save_dir = "K:\\negative_sample"
names = os.listdir(dir)
for name in names:
    img_path = os.path.join(dir, name)
    frame = cv2.imread(img_path)
    for i in range(15):
        x1 = random.randint(20, 800)
        y1 = random.randint(0, 500)
        crop_frame = frame[x1: x1 + random.randint(20, 40), y1: y1 + random.randint(20, 40)]
        save_name = os.path.splitext(name)[0] + str(i) + ".jpg"
        save_path = os.path.join(save_dir, save_name)
        cv2.imwrite(save_path, crop_frame)
        print("save:", save_path)
