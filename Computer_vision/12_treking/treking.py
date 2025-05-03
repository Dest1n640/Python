import cv2
import numpy as np

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
cv2.namedWindow("ROI", cv2.WINDOW_NORMAL)

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
min_area = 1000
capture.set(cv2.CAP_PROP_EXPOSURE, 100)

roi = None
while capture.isOpened():
    ret, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        break
    if key == "r":
        x, y, w, h = cv2.selectROI("ROI selection", gray)
        roi = gray[y : y + h, x : x + w]
        cv2.imshow("ROI", roi)
        cv2.destroyWindow("ROI selection")
    if roi is not None:
        result = cv2.matchTemplate(gray, roi, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        x1, y1 = max_loc
        x2, y2 = x1 + roi.shape[1], y1 + roi.shape[0]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow("COR", result)
    cv2.imshow("Camera", frame)

capture.release()
cv2.destroyAllWindows()
