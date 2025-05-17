import cv2
import numpy as np

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)


def censor(image, size=(10, 10)):
    result = np.zeros_like(image)
    stepy = result.shape[0] // size[0]
    stepx = result.shape[1] // size[1]
    for y in range(0, image.shape[0], stepy):
        for x in range(0, image.shape[1], stepx):
            result[y : y + stepy, x : x + stepx] = np.mean(
                image[y : y + stepy, x : x + stepx]
            )
    return result


capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
capture.set(cv2.CAP_PROP_EXPOSURE, 350)

face_cascade = cv2.CascadeClassifier("./xml/haarcascade-frontalface-default.xml")
eye_cascade = cv2.CascadeClassifier("./xml/haarcascade-eye.xml")
glass = cv2.imread("./xml/deal-with-it.png")

while capture.isOpened():
    ret, frame = capture.read()
    key = chr(cv2.waitKey(1) & 0xFF)
    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    faces = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for x, y, w, h in faces:
        new_w = int(w * 1.5)
        new_h = int(h * 1.5)
        x -= (new_w - w) // 2
        y -= (new_h - h) // 2
        cv2.rectangle(frame, (x, y), (x + new_w, y + new_h), (255, 0, 0), 2)
        roi = frame[y : y + new_h, x : x + new_w]
        try:
            censored = censor(roi, (9, 9))
            frame[y : y + new_h, x : x + new_w] = censored
        except ValueError as e:
            pass
    if key == "q":
        break
    cv2.imshow("Camera", frame)

capture.release()
cv2.destroyAllWindows()

