import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector =  HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0,0] 


while True:
    imgBG = cv2.imread("C:/My files/Coding/Python/games/Rock Paper Scisor/resources/BG.png")
    success, img = cap.read()
    
    imgscaled = cv2.resize(img,(0,0),None,0.416,0.416) #adjusting height of image
    imgscaled = imgscaled[:,116:416] #adjusting width of image


    # Find hands
    hands, img = detector.findHands(imgscaled)

    if startGame:
        
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG,f"Sec: {int(timer)}",(430,480),cv2.FONT_ITALIC,1,(255,0,255),4)

            if timer>3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1
                    if fingers == [1,1,1,1,1]:
                        playerMove = 2
                    if fingers == [0,1,1,0,0]:
                        playerMove = 3

                    randomnum = random.randint(1,3)
                    imgAI = cv2.imread(f'resources/{randomnum}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG,imgAI,(66,315))

                    # Player wins
                    if (playerMove==1 and randomnum == 3) or \
                        (playerMove==2 and randomnum == 1) or \
                        (playerMove==3 and randomnum == 2):
                        scores[1] += 1

                    # AI wins
                    # Player wins
                    if (playerMove==3 and randomnum == 1) or \
                        (playerMove==1 and randomnum == 2) or \
                        (playerMove==2 and randomnum == 3):
                        scores[0] += 1     

                    print(playerMove)

    imgBG[317:617 , 594:894] = imgscaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG,imgAI,(66,315))
        cv2.putText(imgBG, str(scores[0]),(235,270),cv2.FONT_ITALIC,2,(0,205,50),6)
        cv2.putText(imgBG, str(scores[1]),(787,270),cv2.FONT_ITALIC,2,(0,205,50),6)
        
    
    # cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    # cv2.imshow("Scaled", imgscaled)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False

    elif key == 27:  # 27 is the ASCII code for the Esc key
        break

cap.release()
cv2.destroyAllWindows()