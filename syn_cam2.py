from threading import Thread
import cv2 as cv
import time
import numpy as np

class vStream:
    def __init__(self,src,width,height):
        self.width = width
        self.height = height
        self.capture = cv.VideoCapture(src)
        self.thread = Thread(target=self.update,args=())
        self.thread.daemon = True
        self.thread.start()
    def update(self):
        while True:
            _,self.frame = self.capture.read()
            self.frame2 = cv.resize(self.frame,(self.width,self.height))
    def getFrame(self):
        return self.frame2

dispW=640
dispH=480
flip = 2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam1=vStream("/dev/video1",dispW,dispH)
cam2=vStream(camSet,dispW,dispH)
font=cv.FONT_HERSHEY_SIMPLEX
# FPS calculation
fpsReport = 0
timestamp = time.time()

while True:
    try:
        myFrame1=cam1.getFrame()
        myFrame2=cam2.getFrame()
        myFrame3=np.hstack((myFrame1,myFrame2))
        
         # time stamp FPS
        dt = time.time() - timestamp
        fps = 1 / dt
        fpsReport = 0.9 * fpsReport + 0.1 * fps
        timestamp = time.time()
        #print('fps is',fpsReport)
        
        cv.putText( myFrame3, str(round(fpsReport, 1)) + " FPS", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2,)
        cv.imshow('combocam',myFrame3)
        
    except:
        #print('Frame no available')
        pass
    if cv.waitKey(1)==ord('q'):
        cam1.capture.release()
        cam2.capture.release()
        cv.destroyAllWindows()
        exit(1)
        break