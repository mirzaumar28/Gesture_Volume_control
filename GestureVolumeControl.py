import cv2 as cv
import mediapipe as mp
import time 
import numpy as np 
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################################
wCam, hCam = 640, 480
################################


cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.HandDetector(detection_confidence = 1)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)\

# volume.GetMute()
# volume.GetMasterVolumeLevel()
volume_range  = volume.GetVolumeRange()

# print({volume.GetVolumeRange()})
minVol = volume_range[0]
maxVol = volume_range[1]
vol = 0
volbar = 400
volper = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv.circle(img, (x1, y1), 15, (255, 0, 255), cv.FILLED)
        cv.circle(img, (x2, y2), 15, (255, 0, 255), cv.FILLED)
        cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)
        cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        # print(length)

        if length < 50:
            cv.circle(img, (cx, cy), 15, (0, 255, 0), cv.FILLED)

        # hand range 50 - 300
        # volume range -65 - 0

        vol = np.interp(length, [10, 240], [minVol, maxVol])
        volbar = np.interp(length, [10, 240], [400, 150])
        volper = np.interp(length, [10, 240], [0, 100])
        # print(vol, int(length))
        volume.SetMasterVolumeLevel(vol, None)


    cv.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv.rectangle(img, (50, int(volbar)), (85, 400), (0, 255, 0), cv.FILLED)
    cv.putText(img, f"{int(volper)}%", (50,450), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2 )


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv.putText(img, f"FPS:{int(fps)}", (20, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2 )


    cv.imshow("Image", img)
    cv.waitKey(1)