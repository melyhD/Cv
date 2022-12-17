import cv2
import numpy as np
from copy import deepcopy
from keyboard import is_pressed

img_name = "Lada.jpg"
img_name_det = "Lada Color Detection.jpg"
img_path = ""

width, height = 600, 400

img = cv2.imread(img_path + img_name)
img = cv2.resize(img, (width, height))
img_display = deepcopy(img)

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
    global img_display
    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 450:
                x, y, w, h = cv2.boundingRect(contour)
                ctr = int(y + h/2), int(x + w/2)
                color = (int(img[ctr][0]), int(img[ctr][1]), int(img[ctr][2]))
                cv2.rectangle(img_display, (x, y), (x + w, y + h), color, 1)
                cv2.putText(img_display, color_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

hsv = cv2.medianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), blur_value)

blue_mask = cv2.inRange(hsv, dark_blue, light_blue)
green_mask = cv2.inRange(hsv, dark_green, light_green)
red_mask = cv2.inRange(hsv, dark_red, light_red)

b_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
g_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
r_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
draw(b_contours, "Blue")
draw(g_contours, "Green")
draw(r_contours, "Red")
    
b_result = cv2.bitwise_and(img, img, mask=blue_mask)
g_result = cv2.bitwise_and(img, img, mask=green_mask)
r_result = cv2.bitwise_and(img, img, mask=red_mask)

def mouse_click(event, x, y, flags, param):
    if is_pressed("alt"):
        if event == cv2.EVENT_RBUTTONDOWN:
            cv2.imwrite(img_path + img_name_det, img_display)

cv2.imshow("Color Detector", img_display)
cv2.imshow("Blue Color Detector", b_result)
cv2.imshow("Green Color Detector", g_result)
cv2.imshow("Red Color Detector", r_result)

cv2.setMouseCallback("Color Detector", mouse_click)

cv2.waitKey(0)
cv2.destroyAllWindows()