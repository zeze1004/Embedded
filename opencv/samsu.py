import cv2

import numpy as np

import math

import serial

import picamera

import picamera.array

import time
from Image import *
from Utils import *
 

ser = serial.Serial("/dev/serial/by-id/usb-Arduino_Srl_Arduino_Uno_75439313737351613172-if00", 115200, timeout=1)           # linux

 

camera = picamera.PiCamera()

camera.resolution = (640, 480)

camera.framerate = 30

# camera zoom in

zoom = 0.25

camera.zoom = (0+zoom, 0+zoom, 1-2*zoom, 1-2*zoom)

rawCapture = picamera.array.PiRGBArray(camera, size = (640, 480))

time.sleep (0.1)

for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):

 

    image = frame.array

    image = cv2.resize(image,(160,120))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)

 

    # Color thresholding

    ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

 

    # Erode and dilate to remove accidental line detections

    mask = cv2.erode(thresh1, None, iterations=2)

    mask = cv2.dilate(mask, None, iterations=2)

 

    # Find the contours of the frame

    contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

 

    # Find the biggest contour (if detected)

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)

        M = cv2.moments(c)

 

        cx = int(M['m10']/M['m00'])

        cy = int(M['m01']/M['m00'])

        

 

        cv2.line(image,(cx,0),(cx,720),(255,0,0),1)

        cv2.line(image,(0,cy),(1280,cy),(255,0,0),1)

 

        cv2.drawContours(image, contours, -1, (0,255,0), 1)

 

        print(cx)

       

 

#약 좌회전

        if 35 <= cx <= 50:

            ser.write(chr(4).encode())

            print("Weak Left")

# 강 좌회전

       if cx < 35:
            ser.write(chr(4).encode())

            print("Strong Left")

#직진

        if cx < 100 and cx > 50:

            ser.write(chr(1).encode())

            print("Forward")

#약 좌회전

        if cx < 120 and cx >= 100:
            ser.write(chr(6).encode())
            print("Weak Right")

#강 우회전
        if cx >=120:
            ser.write(chr(5).encode())
            print("Strong Right")

#후진

    else:

        ser.write(chr(2).encode())
        print("Reverse")


        

    cv2.imshow("Frame",image)    

    rawCapture.truncate(0)

 

    # Press Q on keyboard to  exit

    if cv2.waitKey(1) == ord('q'):

        print('Streaming Stopped because of key pressed event')

        break

 

# Closes all the frames

cv2.destroyAllWindows()