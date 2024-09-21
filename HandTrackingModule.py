import mediapipe as mp
import cv2 as cv 

import time 

class HandDetector():
    def __init__(self, mode = False, maxHands = 2,
                  detection_confidence = 1, tracking_confidence = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detection_confidence,
                                        self.tracking_confidence)
        self.mpdraw = mp.solutions.drawing_utils



    def findHands(self, img, draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for hand_landmarks in self.result.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, hand_landmarks, 
                                               self.mpHands.HAND_CONNECTIONS)
                
        return img



    def findPosition(self, img, handNo = 0, draw = True):
        self.lmList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                                h, w, c = img.shape
                                cx, cy = int(lm.x * w), int(lm.y * h)
                                # print(id, cx, cy)
                                self.lmList.append([id, cx, cy])
                                if draw:
                                    cv.circle(img, (cx, cy), 15, (255, 255, 0), cv.FILLED)

        return self.lmList
    
    def count_fingers(self):
        count = 0
        #  thumb
        if len(self.lmList) != 0:
            if self.lmList[8][2] < self.lmList[6][2]:
                count = count+1 
            #     print(f"open {lmList[8][2]}, {lmList[6][2]}")
            # else:
            #     print(f"closed {lmList[8][2]}, {lmList[6][2]}")
            if self.lmList[12][2] < self.lmList[10][2]:
                count = count+1 
            if self.lmList[16][2] < self.lmList[14][2]:
                count = count+1 
            if self.lmList[20][2] < self.lmList[18][2]:
                count = count+1 
            if self.lmList[4][1] > self.lmList[3][1]:
                count = count+1 

        return count
    
    def find_distance(self, p1, p2, img, draw = True, r = 15, t = 3):
        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2 

        if draw:
            cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv.circle(img, (x1, y1), r, (255, 0, 255), cv.FILLED)
            cv.circle(img, (x2, y2), r, (255, 0, 255), cv.FILLED)
            cv.circle(img, (cx, cy), r, (0, 0, 255), cv.FILLED)

        length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5

        return length, img, [x1, y1, x2, y2, cx, cy
                             ]




def main():
    pTime = 0 
    cTime = 0 
    cap = cv.VideoCapture(0)
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw= False)
        # if len(lmList) != 0:
            # print(lmList[4])

        count = detector.count_fingers()
        # print(count)

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv.putText(img, str(int(fps)), (10,70), cv.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), thickness = 3 )
        cv.imshow('Image', img)
        cv.waitKey(1)



if __name__ == "__main__":
    main()


