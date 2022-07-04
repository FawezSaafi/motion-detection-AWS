import numpy as np
import imutils
import cv2
import classifier
from classifier import OpenCV

MODULE_PATH = r"C:\Users\21658\anaconda3\Lib\site-packages\cv2\__init__.py"
MODULE_NAME = "cv2"
OpenCV.import_layer(MODULE_PATH, MODULE_NAME)
def frame_draw_detections(frame, first_frame, gray):
    detected = False

    frame_delta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    eroded = cv2.erode(thresh, np.ones((3, 3), np.uint8), iterations=1)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # calcul de la taille max

    # height, width of image
    height = first_frame.shape[0]
    width = first_frame.shape[1]
    # print(height,width)

    # 720x1280 = 921600 aire total
    min_area = height * width * 0.001
    min_area = height * width * 0.0005
    min_area = height * width * 0.00025

    Y1 = 0
    X1 = 0
    Y2 = 0
    X2 = 0
    bFirst = False
    # loop over the contours
    for c in cnts:
        if cv2.contourArea(c) < min_area:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)

        # calcul de la taille max de la boite anglobante du mouvement
        if bFirst == False:
            bFirst = True
            Y1 = y
            X1 = x
            Y2 = y + h
            X2 = x + w

        else:

            X1 = min(X1, x)
            Y1 = min(Y1, y)
            X2 = max(X2, x + w)
            Y2 = max(Y2, y + h)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        detected = True

    cv2.rectangle(frame, (X1, Y1), (X2, Y2), (0, 0, 255), 2)
    return frame, detected