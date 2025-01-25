<<<<<<< HEAD
import cv2
import mediapie as mp
import time

cap =cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands(False)
mpDraw = mp.solutions.drawing_utils

pTime=0
cTime=0

while True:
    success, ing = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.mult_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h,w,c = img.share
                cx,cy = int (lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id == 0:
                    cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mphands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cap.release()
    cv2.destroyAllWindows()
=======
import cv2
import mediapie as mp
import time

cap =cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands(False)
mpDraw = mp.solutions.drawing_utils

pTime=0
cTime=0

while True:
    success, ing = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.mult_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h,w,c = img.share
                cx,cy = int (lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id == 0:
                    cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mphands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cap.release()
    cv2.destroyAllWindows()
>>>>>>> 355883d162ae7de750fded4728fb61c2e1a44af3
