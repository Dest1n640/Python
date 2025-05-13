import cv2

image = cv2.imread("png/hierarchy.png")


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
arrow = contours[0]

print(hierarchy)  # [next, previous, first_child, parent]

for i, contour in enumerate(contours):
    cv2.putText(
        image,
        f"{hierarchy[0, i]}",
        contour[0, 0],
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2,
    )

cv2.drawContours(image, contours, 0, (255, 0, 0), 3)

cv2.namedWindow("Hierrachy", cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Hierrachy", image)
cv2.waitKey()
cv2.destroyAllWindows()
