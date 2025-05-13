import cv2

image = cv2.imread("png/figures.png")


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
arrow = contours[0]

for contour in contours:
    eps = 0.01 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, eps, True)
    for p in approx:
        cv2.circle(image, tuple(*p), 6, (0, 266, 0), 2)

cv2.namedWindow("Figures", cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Figures", image)
cv2.waitKey()
cv2.destroyAllWindows()
