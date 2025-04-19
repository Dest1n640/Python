import numpy as np
import cv2

background = cv2.imread("news.jpg")
foreground = cv2.imread("cheburashka.jpg")

cv2.namedWindow("TV", cv2.WINDOW_NORMAL)

capture = cv2.VideoCapture(0)

while capture.isOpened():
    ret, frame = capture.read()
    key = chr(cv2.waitKey(1) & 0xFF)
    foreground_points = np.array(
        [
            [0, 0],
            [0, frame.shape[0]],
            [frame.shape[1], 0],
            [frame.shape[1], frame.shape[0]],
        ],
        dtype="f4",
    )
    tv_points = np.array([[17, 25], [38, 292], [431, 54], [432, 264]], dtype="f4")

    M = cv2.getPerspectiveTransform(foreground_points, tv_points)
    print(M)

    result = cv2.warpPerspective(frame, M, (background.shape[1], background.shape[0]))

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

    bg = cv2.bitwise_and(background, background, mask=cv2.bitwise_not(thresh))

    tvchebu = cv2.add(bg, result)

    cv2.imshow("Cbeburashka", tvchebu)
    if key == "q":
        break


# foreground_points = np.array(
#     [
#         [0, 0],
#         [0, foreground.shape[0]],
#         [foreground.shape[1], 0],
#         [foreground.shape[1], foreground.shape[0]],
#     ],
#     dtype="f4",
# )
# tv_points = np.array([[17, 25], [38, 292], [431, 54], [432, 264]], dtype="f4")
#
# M = cv2.getPerspectiveTransform(foreground_points, tv_points)
# print(M)
#
# result = cv2.warpPerspective(foreground, M, (background.shape[1], background.shape[0]))
#
# gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
#
# thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
#
# bg = cv2.bitwise_and(background, background, mask=cv2.bitwise_not(thresh))
#
# tvchebu = cv2.add(bg, result)
#
# cv2.imshow("Cbeburashka", tvchebu)
# cv2.waitKey()
