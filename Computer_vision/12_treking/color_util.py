import cv2
import numpy as np

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
capture.set(cv2.CAP_PROP_EXPOSURE, 120)
position = [0, 0]


def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global position
        position = [y, x]
        print(position)


cv2.setMouseCallback("Camera", on_mouse_click)

while capture.isOpened():
    ret, frame = capture.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    key = chr(cv2.waitKey(1) & 0xFF)
    hsv_color = hsv[
        position[0] - 5 : position[0] + 5, position[1] - 5 : position[1] + 5
    ]
    hsv_color = np.array(
        (
            hsv_color[:, :, 0].mean(),
            hsv_color[:, :, 1].mean(),
            hsv_color[:, :, 2].mean(),
        ),
        dtype="uint8",
    )
    if key == "q":
        break
    cv2.circle(frame, (position[1], position[0]), 5, (255, 0, 0))
    cv2.putText(
        frame,
        f"HSV = {hsv_color}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 0, 0),
    )
    cv2.imshow("Camera", frame)

capture.release()
cv2.destroyAllWindows()
