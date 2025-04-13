import cv2
import numpy as np
import time

cam = cv2.VideoCapture(0)
prev_time = time.perf_counter()
if cam.isOpened():
    while True:
        ret, frame = cam.read()
        curr_time = time.perf_counter()
        print(f"{1 / (curr_time - prev_time):.1f}")
        prev_time = curr_time
        frame = np.fliplr(frame)
        print(frame.shape)
        cv2.imshow("Camera", frame)
        key = cv2.waitKey(10)
        if (key & 0xFF) == ord("y"):
            break
cam.release()
