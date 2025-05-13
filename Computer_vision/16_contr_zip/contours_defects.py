import cv2

image = cv2.imread("png/defects.png")


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
arrow = contours[0]

cv2.drawContours(image, contours, 0, (255, 0, 0), 3)

rect = contours[0]

hull = cv2.convexHull(rect)
for i in range(1, len(hull)):
    cv2.line(image, tuple(*hull[i - 1]), tuple(*hull[i]), (0, 255, 0), 2)
cv2.line(image, tuple(*hull[-1]), tuple(*hull[0]), (0, 255, 0), 2)

indexes = cv2.convexHull(rect, returnPoints=False)
defects = cv2.convexityDefects(rect, indexes)
for p in defects:
    s, t, f, d = p[0]
    cv2.circle(image, tuple(*rect[s]), 6, (0, 0, 255), 3)
    cv2.circle(image, tuple(*rect[f]), 6, (0, 255, 255), 2)
    cv2.circle(
        image,
        tuple(*rect[t]),
        7,
        (0, 255, 0),
    )


cv2.namedWindow("Defects", cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Defects", image)
cv2.waitKey()
cv2.destroyAllWindows()
