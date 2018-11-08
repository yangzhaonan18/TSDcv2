# -*- coding: utf-8 -*-
import cv2
import sys

tracker_type = str(sys.argv[1])
if tracker_type == 'BOOSTING':
    tracker = cv2.TrackerBoosting_create()
if tracker_type == 'MIL':
    tracker = cv2.TrackerMIL_create()
if tracker_type == 'KCF':
    tracker = cv2.TrackerKCF_create()
if tracker_type == 'TLD':
    tracker = cv2.TrackerTLD_create()
if tracker_type == 'MEDIANFLOW':
    tracker = cv2.TrackerMedianFlow_create()
if tracker_type == 'GOTURN':
    tracker = cv2.TrackerGOTURN_create()
cap = cv2.VideoCapture(0)
if cap.isOpened() is False:
    raise ("IO error")  # 抛出异常
ret, frame1 = cap.read()
box = cv2.selectROI(frame1)  # 返回一个元组（x,y,w,h)


##笔者试过不能追踪点
##如point=(12,21),ok=tracker.init(frame1,point),报错参数少于4
def centerxy(frame1, box):  # 计算选择区域的质心
    box_img = frame1[int(box[1]):int(box[1] + box[3]), int(box[0]):int(box[0] + box[2])]
    box_gray = cv2.cvtColor(box_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(box_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, cnts, h = cv2.findContours(thresh, 0, 1)
    cnt_max = sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True)[0]
    M = cv2.moments(cnt_max)
    cx = M["m10"] / M["m00"]
    cy = M["m01"] / M["m00"]
    point = (int(cx), int(cy))
    return box_img, point


_, point1 = centerxy(frame1, box)
ok = tracker.init(frame1, box)
while 1:
    ret, frame = cap.read()
    if ret == False:
        sys.exit()
    time1 = cv2.getTickCount()
    ok, box_new = tracker.update(frame)  # 更新追踪
    time2 = cv2.getTickCount()
    if ok:
        p1 = (int(box_new[0]), int(box_new[1]))
        p2 = (int(box_new[0] + box_new[2]), int(box_new[1] + box_new[3]))
        #         p2=(int(point_new[0]), int(point_new[1]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        box_im, point2 = centerxy(frame, box_new)
        cv2.line(box_im, point1, point2, (255, 0, 0), 2)
        cv2.circle(box_im, point2, 10, (0, 0, 255), 2)
        print(point2)
        point1 = point2  # 前一帧位置和当前帧位置，线越长，运动距离越大
    else:
        cv2.putText(frame, "failure", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    fps = cv2.getTickFrequency() / (time2 - time1)
    cv2.putText(frame, str(fps), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("frame", frame)
    k = cv2.waitKey(10)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
