# importing required modules
import cv2
import numpy as np
import pyautogui

# capturing video
cap = cv2.VideoCapture(0)

# we can use any sort of color , here blue color is used for virtual movement control. so we need to set upper and lower limit for
# it to detect it on screen
blue_lower=np.array([100,150,0])
blue_upper=np.array([140,255,255])

# to move screen need to store previous y axis value to a variable
prev_y = 0

# capturing continue till user input s in keyboard
while True:

    # captures the frame from video
    ret, frame = cap.read()
    # converting frames to hue saturated to detect only colors
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # masking only blue color using provided limit
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    # detecting contours of object using color range
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # traversing through contours to get object area
    for contour in contours:
        area = cv2.contourArea(contour)
        # if object found to be on screen area will be greater than normal values
        if area > 1200:
            # if object is found , it will be displayed in a bounding box
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # if y-axis of object moves down, it will enter down button on keyboard
            if y < prev_y:
                pyautogui.press('down')
            # if y-axis of object moves up, it will enter up button on keyboard
            elif y > prev_y:
                pyautogui.press('up')
            else:
                pass
            # resetting previous value to new value
            prev_y = y
    # displaying original image to user
    cv2.imshow('frame', frame)

    # iif user struck s on keyboard, capturing will stop
    if cv2.waitKey(10) == ord('s'):
        break
# destroy al running windows
cap.release()
cv2.destroyAllWindows()
