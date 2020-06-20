

import numpy as np
import cv2



print(cv2.__version__)

dispW=1080
dispH=720
flip = 2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)

#cam = cv2.VideoCapture("/dev/video1") # check this
#cam = cv2.VideoCapture(1) # check this
#cam = cv2.VideoCapture(0) # check this
#cam = cv2.VideoCapture("http://anonhome.ddns.net:11111/videostream.cgi?user=admin&pwd=025737683")
#cam.set(cv2.CAP_PROP_FRAME_WIDTH,dispW)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT,dispH)
print(cv2.CAP_PROP_FRAME_COUNT)
print(cam.get(cv2.CAP_PROP_FPS))
while(True):
    # Capture frame-by-frame
    ret, frame = cam.read()
   
    # Our operations on the frame come here
    frameSmall=cv2.resize(frame,(320,240))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    graySmall=cv2.resize(gray,(320,240))
    # Display the resulting frame
    #cv2.namedWindow('frame',0)
      
    
    cv2.imshow('frame',frame)
    cv2.moveWindow('frame',0,0)
   
    cv2.imshow('frame2',frameSmall)
    cv2.moveWindow('frame2',720,0)

    cv2.imshow('frame3',gray)
    cv2.moveWindow('frame3',0,540)

    cv2.imshow('frame4',graySmall)
    cv2.moveWindow('frame4',720,540)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()