import cv2
import numpy as np
from copy import deepcopy

cap = cv2.VideoCapture(0)

width, height = 600, 400

dark_blue = np.array([95, 20, 20])
light_blue = np.array([125, 255, 255])

dark_green = np.array([25, 20, 20])
light_green = np.array([95, 255, 255])

dark_red = np.array([165, 85, 85])
light_red = np.array([180, 255, 255])

blur_value = 5

blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)

def draw(contours, color_name):
    global frame_display
    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 450:
                x, y, w, h = cv2.boundingRect(contour)
                ctr = int(y + h/2), int(x + w/2)
                color = (int(frame[ctr][0]), int(frame[ctr][1]), int(frame[ctr][2]))
                cv2.rectangle(frame_display, (x, y), (x + w, y + h), color, 1)
                cv2.putText(frame_display, color_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (width, height))
    frame_display = deepcopy(frame)

    hsv = cv2.medianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), blur_value)

    blue_mask = cv2.inRange(hsv, dark_blue, light_blue)
    green_mask = cv2.inRange(hsv, dark_green, light_green)
    red_mask = cv2.inRange(hsv, dark_red, light_red)

    b_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    g_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    r_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    draw(b_contours, "Blue")
    draw(g_contours, "Green")
    draw(r_contours, "Red")
    
    b_result = cv2.bitwise_and(frame, frame, mask=blue_mask)
    g_result = cv2.bitwise_and(frame, frame, mask=green_mask)
    r_result = cv2.bitwise_and(frame, frame, mask=red_mask)

    cv2.imshow("Color Detector", frame_display)
    cv2.imshow("Blue Color Detector", b_result)
    cv2.imshow("Green Color Detector", g_result)
    cv2.imshow("Red Color Detector", r_result)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
