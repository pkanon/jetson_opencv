

import numpy as np
import cv2
import urllib.request

print(cv2.__version__)

dispW=640
dispH=480
#cam = cv2.VideoCapture("/dev/video0") # check this
#cam = cv2.VideoCapture(0) # check this
cam = cv2.VideoCapture("http://anonhome.ddns.net:11111/videostream.cgi?user=admin&pwd=025737683")
urlup = 'http://anonhome.ddns.net:11111/decoder_control.cgi?loginuse=admin&loginpas=025737683&command=0&onestep=1&15909189408710.7370865373212729&_=1590918940876'
urldown = 'http://anonhome.ddns.net:11111/decoder_control.cgi?loginuse=admin&loginpas=025737683&command=2&onestep=1&15909189408710.7370865373212729&_=1590918940876'
urlleft = 'http://anonhome.ddns.net:11111/decoder_control.cgi?loginuse=admin&loginpas=025737683&command=4&onestep=1&15909189408710.7370865373212729&_=1590918940876'
urlright = 'http://anonhome.ddns.net:11111/decoder_control.cgi?loginuse=admin&loginpas=025737683&command=6&onestep=1&15909189408710.7370865373212729&_=1590918940876'

cam.set(cv2.CAP_PROP_FRAME_WIDTH,dispW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,dispH)

#ip cam resulution parameter
urllib.request.urlopen('http://anonhome.ddns.net:11111/camera_control.cgi?loginuse=admin&loginpas=025737683&param=15&value=0&15909238006480.7146201871845146&_=1590923800650')

height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
print(str(width)+","+str(height))

while(True):
    # Capture frame-by-frame
    ret, frame = cam.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameSize=cv2.resize(frame,(1280,720))
    # Display the resulting frame
    
    cv2.imshow('frame',frame)
    cv2.imshow('frame2',frameSize)
    #cv2.moveWindow('frame',0,0)
    #cv2.moveWindow('frame2',0,420)   
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('w'): #up
        urllib.request.urlopen(urlup)
    if key == ord('s'): #down
        urllib.request.urlopen(urldown)
    if key == ord('a'): #left
        urllib.request.urlopen(urlleft)
    if key == ord('d'): #right
        urllib.request.urlopen(urlright)
    if key == ord('q'): #break
        break

    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()