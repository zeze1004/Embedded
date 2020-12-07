# -*- coding: utf-8 -*-
import socket
import sys
import os
import numpy as np
import pdb
import math
import serial
import picamera
import picamera.array
import cv2
import time

from Image import *
from Utils import *

#############
enable_c = []   
dif_c = []
sum = 0
dif_av = 0
#############

font = cv2.FONT_HERSHEY_SIMPLEX
direction = 0

ser = serial.Serial("/dev/serial/by-id/usb-Arduino_Srl_Arduino_Uno_75439313737351613172-if00", 115200, timeout=1)           # linux

camera = picamera.PiCamera()

camera.resolution = (640, 480)

camera.framerate = 30

#N_SLICES만큼 이미지를 조각내서 Images[] 배열에 담는다
Images=[]
N_SLICES = 3
width = 320
HEIGHT = 240
TOLERANCE = 145
TURN_MAX = 190
TURN_MID = 90

# camera zoom in

zoom = 0.25

camera.zoom = (0+zoom, 0+zoom, 1-2*zoom, 1-2*zoom)

rawCapture = picamera.array.PiRGBArray(camera, size = (640, 480))

time.sleep (0.1)

for q in range(N_SLICES):
    Images.append(Image())

def in_tolerance(n):
    if n < -TOLERANCE:
        return False
    if n > TOLERANCE:
        return False
    return True

def get_cmd(y1, y2, y3, y4, y5, y6):
    
    num_valid = 6
    
    y1 -= WIDTH/2
    y2 -= WIDTH/2
    y3 -= WIDTH/2
    y4 -= WIDTH/2
    y5 -= WIDTH/2
    y6 -= WIDTH/2
    
    master_point = 0

'''
# 라인트레이싱 
for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
    image = frame.array
    image = cv2.resize(image,(160,120))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # Color thresholding
    ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    #이미지를 조각내서 윤곽선을 표시하게 무게중심 점을 얻는다
    Points = SlicePart(img, Images, N_SLICES)
    print('Points : ', Points)

    #N_SLICES 개의 무게중심 점을 x좌표, y좌표끼리 나눈다
    x = Points[::2]
    y = Points[1::2]

    #조각난 이미지를 한 개로 합친다
    fm = RepackImages(Images)

    # 3개의 무게 중심으로 방향 결정
    def direction(s1, s2, s3):
        enable_num = 3
        all_center = [s1, s2, s3]
'''


        # +: 오른쪽, -: 왼쪽
     if in_tolerance(y1) == False:
        num_valid -= 1
        y1 = 0
    if in_tolerance(y2) == False:
        num_valid -= 1
        y2 = 0
    if in_tolerance(y3) == False:
        num_valid -= 1
        y3 = 0
    if in_tolerance(y4) == False:
        num_valid -= 1
        y4 = 0
    if in_tolerance(y5) == False:
        num_valid -= 1
        y5 = 0
    if in_tolerance(y6) == False:
        num_valid -= 1
        y6 = 0
    
    master_point = 2.65 * (y1 * 0.7 + y2 * 0.85 + y3 + y4 * 1.1 + y5 * 1.2 + y6 * 1.35) / (num_valid + 0.1)

    master_point += y1 * 0.5
    master_point += y2 * 0.4
    master_point += y3 * 0.3
    master_point -= y4 * 0.4
    master_point -= y5 * 0.5
    master_point -= y6 * 0.6

    # back
    if num_valid < 2:
        direction = 'B'
    else:
        direction = 'G'
        if master_point > TURN_MID and master_point < TURN_MAX :
            direction = 'l'
        if master_point < -TURN_MID and master_point > -TURN_MAX :
            direction = 'r'
        if master_point >= TURN_MAX :
            direction = 'L'
        if master_point <= -TURN_MAX :
            direction = 'R'

    cmd = ("%c\n" % (direction)).encode('ascii')

    print(">>> master_point:%d, cmd:%s" % (master_point, cmd))
    
    ser.write(cmd)
    print("send")
    # read cmd from arduino and print it    
    read_serial = ser.readline()
    print("<<< %s" % (read_serial))

img = cv2.VideoCapture(0)
img.set(cv2.CAP_PROP_FPS, 30)
img.set(cv2.CAP_PROP_SATURATION, 0)
img.set(cv2.CAP_PROP_BRIGHTNESS, 0.61)
img.set(cv2.CAP_PROP_CONTRAST, 0.54)
img.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
img.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

skip = 30
while True:
    ret , fram = img.read()
    if skip > 0:
        skip -= 1
    elif fram is not None:
        skip = 6
        #이미지를 조각내서 윤곽선을 표시하게 무게중심 점을 얻는다
        Points = SlicePart(fram, Images, N_SLICES)
        print('Points : ', Points)
           
        #조각난 이미지를 한 개로 합친다
        fm = RepackImages(Images)       





    
    #완성된 이미지를 표시한다
    cv2.imshow('frame', fm)
    rawCapture.truncate(0)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        
        # command
        get_cmd(Points[0][0], Points[1][0], Points[2][0], Points[3][0], Points[4][0], Points[5][0])

    else:
        print('not even processed')

