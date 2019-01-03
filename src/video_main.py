#!/usr/bin/env python

import cv2
import sys
import os
import time

#determine what the parameters are for our vision system process
#get the image size and frame rate, and weather or not to use mjpeg or x264 encoder
#program to be extended later


vidfile = os.environ.get("TANK_VIDEO_PATH","/dev/video0")
raw_height = os.environ.get("TANK_VIDEO_HEIGHT", 480)
raw_width = os.environ.get("TANK_VIDEO_WIDTH", 640)
framerate = os.environ.get("TANK_VIDEO_FPS", 15)
autofocus = os.environ.get("TANK_VIDEO_AUTOFOCUS", 0)
portno = os.environ.get("TANK_VIDEO_UDP_PORT", 5000)


#build the gstreamer string
streamer_string = 'appsrc ! videoconvert ! videoscale ! video/x-raw,format=I420,width=$WIDTH$,height=$HEIGHT$,framerate=$FPS$/1 ! x264enc tune=zerolatency speed-preset=ultrafast  ! rtph264pay ! udpsink host=127.0.0.1 port=$PORT$'
streamer_string = streamer_string.replace('$WIDTH$', str(raw_width))
streamer_string = streamer_string.replace('$HEIGHT$', str(raw_height))
streamer_string = streamer_string.replace('$PORT$', str(portno))
streamer_string = streamer_string.replace('$FPS$', str(framerate))

print "Using the following parameters\n"
print "Video Path: " + vidfile+"\n"
print "Height: " + str(raw_height) +"\n"
print "Width: " + str(raw_width)+"\n"
print "Port: " + str(portno)+"\n"
print "FPS: " + str(framerate) + "\n"
print "Autofocus " + str(autofocus) + "\n"




#open the gstreamer pipeline
out = cv2.VideoWriter(streamer_string, cv2.CAP_GSTREAMER, 0, framerate, (raw_width, raw_height), True)
#open the camera
cap = cv2.VideoCapture(vidfile)

#change the autofocus parameter
cap.set(cv2.CAP_PROP_AUTOFOCUS, autofocus)

#pump frames into the camera
while(True):
    ret, frame = cap.read()
    out.write(frame)
    time.sleep(1/framerate)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
