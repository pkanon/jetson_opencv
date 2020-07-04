from threading import Thread
import cv2 as cv
import time
import numpy as np

class vStream:
    def __init__(self,src):
        self.capture = cv.VideoCapture(src)
        self.thread = Thread(target=self.update,args=())
        self.thread.daemon = True
        self.thread.start()
    def update(self):
        while True:
            _,self.frame = self.capture.read()
    def getFrame(self):
        return self.frame


#3264x2464  1280x720
def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=480,
    framerate=30,
    flip_method=2,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


dispW=640
dispH=480
flip = 2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam1=vStream("/dev/video1")
#cam2=vStream(camSet)
cam2=vStream(gstreamer_pipeline())
face_cascade = cv.CascadeClassifier(
    "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
)
eye_cascade = cv.CascadeClassifier(
    "/usr/share/opencv4/haarcascades/haarcascade_eye.xml"
)





# FPS calculation
fpsReport = 0
timestamp = time.time()

while True:
    try:
        #myFrame1=cam1.getFrame()
        myFrame2=cam2.getFrame()
        img=cam1.getFrame()
        
        
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                      
        for (x, y, w, h) in faces:
            cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y : y + h, x : x + w]
            roi_color = img[y : y + h, x : x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            
            for (ex, ey, ew, eh) in eyes:
                cv.rectangle(
                roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2
                )
        cv.imshow('roi_color',roi_color)
         # time stamp FPS
        dt = time.time() - timestamp
        fps = 1 / dt
        fpsReport = 0.9 * fpsReport + 0.1 * fps
        timestamp = time.time()
        #print('fps is',fpsReport)

        cv.putText(img, str(round(fpsReport, 1)) + " FPS", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2,)
        #cv.putText( myFrame2, str(round(fpsReport, 1)) + " FPS", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2,)
        
        
        cv.imshow('webcam',img)
        
        cv.imshow('picam',myFrame2)

    except:
        #print('Frame no available')
        pass
        
    if cv.waitKey(1)==ord('q'):
        cam1.capture.release()
        cam2.capture.release()
        cv.destroyAllWindows()
        exit(1)
        break