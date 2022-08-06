from playsound import playsound
import cvzone as cz
import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller
import numpy as np
detector = HandDetector(detectionCon=0.8)
cap = cv2.VideoCapture(0)
cap.set(3, 1980)
cap.set(4, 1280)

finaltext = ""
keyboard = Controller()

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",",".", "/" ]]

def drawAll(img, buttonList):                    # For Transparent Keyboard
     imgNew = np.zeros_like(img, np.uint8)
     for button in buttonList:
         x, y = button.pos
         cz.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                           20, rt=0)
         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                       (255, 0, 0), cv2.FILLED)
         cv2.putText(imgNew, button.text, (x + 40, y + 60),
                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

     out = img.copy()
     alpha = 0.5
     mask = imgNew.astype(bool)
     print(mask.shape)
     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
     return out



# def drawAll(img, buttonList):          # For bold Keys Keyboard
#     for button in buttonList:
#         x, y = button.pos
#         w, h = button.size
#         cz.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
#                           20, rt=0)
#
#         cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
#         cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
#                    4, (255, 255, 255), 4)
#         cv2.circle(img, (1200, 50), 30, (128, 128, 128), cv2.FILLED)
#
#     return img

class Button():
    def __init__(self,pos, text, size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 100, 100 * i + 300], key))



while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    img = drawAll(img, buttonList)


    if lmList:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size

            if x< lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)

                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                            4, (255, 255, 255), 4)


                l, _, _ = detector.findDistance(8,12,img)
                print(l)
                if l<45:    # if distance is short the n consider it as click it can be changed for 3D by cheking the Area of boundary box
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0,255, 255), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                                4, (255, 255, 255), 4)
                    finaltext += button.text
                    #Uplaysound('keypress.mp3')
                    sleep(0.2)

    cv2.rectangle(img, (50,30),(700, 100), (175,0,175), cv2.FILLED)
    cv2.putText(img, finaltext, (60,88), cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)


    cv2.imshow("Image", img)
    cv2.waitKey(1)