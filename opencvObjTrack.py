import cv2 as cv
import numpy as np
import urllib.request
import time
import os


#CSI cam
dispW = 640
dispH = 480
flip = 2
# Uncomment These next Two Line for Pi Camera
#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#cap = cv.VideoCapture(camSet)




#cap = cv.VideoCapture('vtest.avi')
#cap = cv.VideoCapture("/dev/video1")
cap = cv.VideoCapture("http://anonhome.ddns.net:11111/videostream.cgi?user=admin&pwd=025737683")
frame_width = int( cap.get(cv.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv.CAP_PROP_FRAME_HEIGHT))

fourcc = cv.VideoWriter_fourcc('X','V','I','D')

out = cv.VideoWriter("output.avi", fourcc, 5.0, (1280,720))  # write to file

ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)

#FPS calculation
fpsReport=0
scalefactor=0
timestamp=time.time()

while cap.isOpened():
    diff = cv.absdiff(frame1, frame2)
    gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh, None, iterations=3)
    contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv.boundingRect(contour)

        if cv.contourArea(contour) < 1500:
            continue
        cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 1)
        #cv.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 3)
    #cv.drawContours(frame1, contours, -1, (0, 0, 255), 1)

    image = cv.resize(frame1, (1280,720))
    out.write(image)   # write to file
    
    #time stamp FPS
    dt=time.time()-timestamp
    fps=1/dt
    fpsReport=0.85*fpsReport+0.15*fps
    #print('fps is',fpsReport)
    timestamp=time.time()
    #str(round(fpsReport,2))
    cv.putText(frame1,str(round(fpsReport,1))+' FPS',(50,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    
    
    cv.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv.waitKey(1)==ord('q'):
        break

cv.destroyAllWindows()
cap.release()
out.release()