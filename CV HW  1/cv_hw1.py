import cv2 as cv
from keyboard import *
from math import *
from copy import deepcopy

state_l = ""
state_r = ""
state_cr = ""

start = None

green = (0, 255, 0)
red = (0, 0, 255)

ln_wdt = 1

text = "Ekrem"

img_name = "Lada.jpg"
win_name = "Lada"
cropped_img_name = "Lada (cropped).jpg"
edited_img_name = "Lada (edited).jpg"

width, height = 800, 800
img = cv.resize(cv.imread(img_name), (width, height))
img_2 = deepcopy(img)

def mouse_click(event, x, y, flags, param):
    global img, img_2, cropped_img, start, end, state_l, state_r, state_cr
    
    if is_pressed("ctrl"):
        if event == cv.EVENT_LBUTTONDOWN:
            start = (x, y)
            state_l = "rect"
        if state_l == "rect":
            end = (x, y)
            img_3 = deepcopy(img_2)
            img = cv.rectangle(img_3, start, end, green, ln_wdt)
            cv.imshow(win_name, img)

        if event == cv.EVENT_RBUTTONDOWN:
            start = (x, y)
            state_r = "circle"
        if state_r == "circle":
            end = (x, y)
            radius = int(sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2))
            img_3 = deepcopy(img_2)
            img = cv.circle(img_3, start, radius, red, ln_wdt)
            cv.imshow(win_name, img)

    if is_pressed("alt"):
        if event == cv.EVENT_LBUTTONDOWN:
            color = (int(img[y, x][0]), int(img[y, x][1]), int(img[y, x][2]))
            img_2 = cv.putText(img_2, text, (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            img = deepcopy(img_2)
            cv.imshow(win_name, img)
            state_l = "text"

        if event == cv.EVENT_RBUTTONDOWN:
            cv.imwrite(edited_img_name, img_2)
            state_r = "saved"

    if is_pressed("shift"):
        if event == cv.EVENT_RBUTTONDOWN and state_cr == "cropped":
            cv.imwrite(cropped_img_name, cropped_img)
            state_cr = "saved"
            state_r = "saved"

    if event == cv.EVENT_LBUTTONUP:
        if state_l == "rect" and (abs(start[0] - end[0]) > 2*ln_wdt + 1 and abs(start[1] - end[1]) > 2*ln_wdt + 1):
            if start[1] + ln_wdt < end[1]:
                if start[0] + ln_wdt < end[0]:
                    cropped_img = img[start[1] + ln_wdt:end[1], start[0] + ln_wdt:end[0]]
                else:
                    cropped_img = img[start[1] + ln_wdt:end[1], end[0] + ln_wdt:start[0]]
            else:
                if start[0] + ln_wdt < end[0]:
                    cropped_img = img[end[1] + ln_wdt:start[1], start[0] + ln_wdt:end[0]]
                else:
                    cropped_img = img[end[1] + ln_wdt:start[1], end[0] + ln_wdt:start[0]]

            cv.imshow(cropped_img_name , cropped_img)
            state_cr = "cropped"

        elif state_l == "":
            img_2 = cv.rotate(img_2, cv.ROTATE_90_COUNTERCLOCKWISE)
            img = deepcopy(img_2)
            cv.imshow(win_name, img)
            
        state_l = ""

    if event == cv.EVENT_RBUTTONUP:
        if state_r == "circle":
            img_2 = deepcopy(img)
        elif state_r == "":
            img_2 = cv.rotate(img_2, cv.ROTATE_90_CLOCKWISE)
            img = deepcopy(img_2)
            cv.imshow(win_name, img)
            
        state_r = ""

cv.imshow(win_name, img)
cv.setMouseCallback(win_name, mouse_click)

cv.waitKey(0)
cv.destroyAllWindows()
