#!/usr/bin/env python

import cv2
import sys

#determine what the parameters are for our vision system process
#get the image size and frame rate, and weather or not to use mjpeg or x264 encoder
#program to be extended later

vidfile = "/dev/video0"
if len(sys.argv) > 1:
    vidfile = sys.argv[1]


framerate = 15.0


cap = cv2.VideoCapture(vidfile)

out = cv2.VideoWriter('appsrc ! videoconvert ! videoscale ! video/x-raw,format=I420,width=640,height=480,framerate=15/1 ! x264enc tune=zerolatency speed-preset=ultrafast  ! rtph264pay ! udpsink host=127.0.0.1 port=5000', cv2.CAP_GSTREAMER, 0, framerate, (640, 480), True)

while(True):
    ret, frame = cap.read()
    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
