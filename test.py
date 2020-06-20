import numpy as np
import cv2 as cv
import time
import os
print(cv.__version__)


def gstreamer_pipeline(
        sensor_id=0,
        sensor_mode=3,
        display_width=640,
        display_height=360,
        framerate=60,
        flip_method=2,
):
    return (
            "nvarguscamerasrc sensor-id=%d sensor-mode=%d ! "
            "video/x-raw(memory:NVMM), "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                sensor_id,
                sensor_mode,
                framerate,
                flip_method,
                display_width,
                display_height,
        )
    )






cap = cv.VideoCapture(gstreamer_pipeline(), cv.CAP_GSTREAMER)
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




























