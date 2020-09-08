#This is a prototype of the computer vision, this version will send a signal to a left or right motor to 
#make sure that the target can be in the center of the frame.

import cv2
import RPi.GPIO as GPIO
import time
import numpy as np
print(cv2.__version__)

middle = 0
right = 1
left = -1


output_pin_1 = 18 # Board pin 12
output_pin_2 = 23 # Board pin 16

def nothing(x):
    pass

GPIO.setmode(GPIO.BCM)
GPIO.setup(output_pin_1,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(output_pin_2,GPIO.OUT,initial=GPIO.HIGH)
current_val_1 = GPIO.HIGH
previous_coor_1 = GPIO.HIGH
current_val_2 = GPIO.HIGH

previous_state= middle;

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',1280,0)

cv2.createTrackbar('hueLower','Trackbars',29,179,nothing)
cv2.createTrackbar('hueHigher','Trackbars',71,179,nothing)
cv2.createTrackbar('SaturationLower','Trackbars',107,255,nothing)
cv2.createTrackbar('SaturationHigher','Trackbars',182,255,nothing)
cv2.createTrackbar('valLower','Trackbars',93,255,nothing)
cv2.createTrackbar('valHigher','Trackbars',223,255,nothing)

# 43,76,43,255,98,255 is for GREEN 
#

cam = cv2.VideoCapture(0) 

if cam.isOpened():
    width = cam.get(3)
    height = cam.get(4)

print('Width: ', width)
print('Height:',height)
while True:
    ret, frame=cam.read()



    hsv  = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    hueLow = cv2.getTrackbarPos('hueLower','Trackbars')
    hueUp = cv2.getTrackbarPos('hueHigher','Trackbars')

    sl = cv2.getTrackbarPos('SaturationLower','Trackbars')
    sh = cv2.getTrackbarPos('SaturationHigher','Trackbars')

    vLow = cv2.getTrackbarPos('valLower','Trackbars')
    vHigh = cv2.getTrackbarPos('valHigher','Trackbars')

    lowerBounds = np.array([hueLow,sl,vLow])
    UpperBouds = np.array([hueUp,sh,vHigh])

    fgmask = cv2.inRange(hsv,lowerBounds,UpperBouds)
    smallerfg = cv2.resize(fgmask,(480,360))
    cv2.imshow('FGmask',smallerfg)
    cv2.moveWindow('FGmask',500,0)

    
    contours,_ = cv2.findContours(fgmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key=lambda x:cv2.contourArea(x), reverse = True)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        (x1,y1,widht,height) = cv2.boundingRect(cnt) #top left coordinate (x1,y1) corner of blue box 
        if area>=50: #this only draws boxes around ROIs of at least 50x50 pixels
            # cv2.drawContours(frame,[cnt],0,(255,0,120),3)
            cv2.rectangle(frame,(x1,y1),(x1+widht,y1+height),(255,170),3) 

    #cv2.drawContours(frame,contours,-1,(255,0,120),3)
    current_state = middle;
    ##########################Here is the logic of turning###########

    RIGHT_BOUND = 375
    MID_RIGHT_BOUND = 350
    MID_LEFT_BOUND = 245
    LEFT_BOUND = 220


    if (x1 + widht)/2 > RIGHT_BOUND and previous_state != right:
      current_state = right
      current_val_1 = GPIO.HIGH
      current_val_2 = GPIO.LOW
    elif (x1 + widht)/2 < LEFT_BOUND  and previous_state != left:
        current_state = left
        current_val_1 = GPIO.LOW
        current_val_2 = GPIO.HIGH
    # Hysteresis implemented here
    elif (x1 + widht)/2 < MID_RIGHT_BOUND and (x1 + widht)/2 > MID_LEFT_BOUND and previous_state != middle:
        current_state = middle
        current_val_1 = GPIO.HIGH
        current_val_2 = GPIO.HIGH

    if previous_state != current_state:
        previous_state == current_state


    GPIO.output(output_pin_1,current_val_1)
    GPIO.output(output_pin_2,current_val_2)
    # frameSmall = cv2.resize(frame,(480,360))
    # cv2.imshow("Camera",frameSmall)
    cv2.imshow("Camera",frame)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
GPIO.cleanup()