import cv2

I = cv2.imread("2001 (39).png")
I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

contours = cv2.Canny(I, 125, 350)
# cv2.threshold(I, contours, 128, 255, cv2.THRESH_BINARY)
cv2.namedWindow("Canny")
cv2.imshow("Canny", contours)
cv2.waitKey()
