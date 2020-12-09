import cv2
import numpy as np
import math
import serial
import picamera
import picamera.array
import time

ser = serial.Serial("/dev/serial/by-id/usb-Arduino_Srl_Arduino_Uno_75439313737351613172-if00", 115200, timeout=1)           # linux
# 파이카메라 설정
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

    # 색 임계점 설정
    ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    # Cv2.Erode: 침식함수, 바이너리 이미지에서 흰색 오브젝트 외각을 검은색으로 변경
    # 이진화 이미지에서 작은 흰색노이즈를 제거하거나, 합쳐진 오브젝트를 분리하는데 사용
    mask = cv2.erode(thresh1, None, iterations=2)
    # Cv2.Dilate 팽창함수, 바이너리 이미지에서 흰색 오브젝트 주변에 흰색을 추가
    # 이진화 이미지에서 침식으로 줄어든 오브젝트를 원복하거나, 인접한 오브젝트를 하나로 만드는데 사용가능
    mask = cv2.dilate(mask, None, iterations=2)

    # 외곽선 프레임 찾기
    contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # 외곽선 찾았을 시
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])     # x 좌표 중심
        cy = int(M['m01']/M['m00'])     # y 좌표 중심

        # 좌표 라인 생성
        cv2.line(image,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(image,(0,cy),(1280,cy),(255,0,0),1)
        # 화면에 라인 표시
        cv2.drawContours(image, contours, -1, (0,255,0), 1)
        # x 좌표 중심값 출력
        print(cx)

        # 강 좌회전
        if cx <= 50:
            ser.write(chr(3).encode())
            print("Strong Left")
            read_serial = ser.readline()    # 아두이노에서 값 입력 받기
            print("%s" % (read_serial))
        #직진
        if cx < 90 and cx > 50:
            ser.write(chr(1).encode())
            print("Forward")
            read_serial = ser.readline()
            print("%s" % (read_serial))
        #강 우회전
        if cx >=90:
            ser.write(chr(5).encode())
            print("Strong Right")
            read_serial = ser.readline()
            print("%s" % (read_serial))
    
    # 라인 발견 못했을 시
    #후진
    else:
        ser.write(chr(2).encode())
        print("Reverse")
        read_serial = ser.readline()
        print("%s" % (read_serial))

    # 화면에 출력
    cv2.imshow("Frame",image)    
    rawCapture.truncate(0)

    # q 눌렀을 시 종료
    if cv2.waitKey(1) == ord('q'):
        print('system quit')
        break
 
# 화면 끄기
cv2.destroyAllWindows()