import cv2 as cv
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from HandTrackingModule import HandDetector

detector = HandDetector(detection_con=0.7)
cam = cv.VideoCapture(0)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volrange=volume.GetVolumeRange()
min=volrange[0]
max=volrange[1]
while True:
    istrue, frame = cam.read()
    frame = detector.FindHands(frame)
    lmst = detector.DisplayPoints(frame)
    length_hands=0
    if (lmst):
        cv.circle(frame, (lmst[4][1], lmst[4][2]), 10, (255, 255, 255), cv.FILLED)
        cv.circle(frame, (lmst[8][1], lmst[8][2]), 10, (255, 255, 255), cv.FILLED)
        x1, y1 = lmst[4][1], lmst[4][2]
        x2, y2 = lmst[8][1], lmst[8][2]
        cv.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 3)
        length_hands=math.hypot(x2 - x1,y2 - y1)
        print(length_hands)
        volume_meter = np.interp(length_hands, [10, 250], [min, max])
        rect_range=np.interp(volume_meter,[min,max],[0,100])
        print(rect_range)
        cv.putText(frame,"Volume : "+str(int(rect_range))+"%",(130,130),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),thickness=2)
        cv.rectangle(frame,(150,150),(180,150+int(rect_range)),(0,255,0),cv.FILLED)
        volume.SetMasterVolumeLevel(volume_meter, None)
    cv.imshow("Hands", frame)
    if cv.waitKey(20) & 0xFF == ord("d"):
        break


