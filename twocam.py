import numpy as np
import cv2 as cv
import time
import os
print(cv.__version__)
Scale = 1
dispW = int(1280*Scale)
dispH = int(720*Scale)
flip = 2
# CSI CAM width=3264, height=2464 BGRx
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cap= cv.VideoCapture(camSet)


#cap2 = cv.VideoCapture("vtest.avi")
cap2 = cv.VideoCapture("/dev/video1")

# FPS calculation
fpsReport = 0
scalefactor = 0
timestamp = time.time()


while cap.isOpened():
    ret, frame = cap.read()
    ret, frame2 = cap2.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # time stamp FPS
    dt = time.time() - timestamp
    fps = 1 / dt
    fpsReport = 0.85 * fpsReport + 0.15 * fps
    # print('fps is',fpsReport)
    timestamp = time.time()
    # str(round(fpsReport,2))
    cv.putText( gray, str(round(fpsReport, 1)) + " FPS", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2,)
    cv.putText( frame, str(round(fpsReport, 1)) + " FPS", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2,)
    cv.putText( frame2, str(round(fpsReport, 1)) + " FPS", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2,)
    
    #
    #
    #
    
    cv.imshow("gray", gray)
    #cv.moveWindow("gray",0,0)
    cv.imshow("frame", frame)
    #cv.moveWindow("frame",0,0)
    cv.imshow("frame2", frame2)
    #cv.moveWindow("frame2",0,0)
    if cv.waitKey(1) == ord("q"):
        break
cap.release()
cap2.release()
cv.destroyAllWindows()
