import cv2
import time
import handtrackingmodule as htm
import pyautogui
import numpy as np


def mouse():
    wCam, hCam = 640, 480
    frameR = 100  # frame reduction
    smoothening = 8
    pTime = 0
    plocX, plocY = 0, 0  # previous locations of x and y
    clocX, clocY = 0, 0  # current locations of x and y

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)  # width
    cap.set(4, hCam)  # height
    detector = htm.handDetector(detectionCon=0.60, maxHands=1)  # only one hand at a time
    wScr, hScr = pyautogui.size()

    while True:
        # 1. Find hand Landmarks
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        # 2. Get the tip of the index and middle fingers
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp()

            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

            if len(lmList) != 0:

                fingers = detector.fingersUp()
                s = ""
                for i in fingers:
                    s += str(fingers[i]);
                if (s == "00000"):
                    pass
                elif (s == "01000"):
                    #5. Convert Coordinates as our cv window is 640*480 but my screen is full HD so have to convert it accordingly
                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))  # converting x coordinates
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))  # converting y

                    # 6. Smoothen Values avoid fluctuations
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening

                    # 7. Move Mouse
                    pyautogui.moveTo(clocX, clocY)                            # wscr-clocx for avoiding mirror inversion
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)  # circle shows that we are in moving mode
                    plocX, plocY = clocX, clocY
                    pass

                elif (s == "01100"):
                    pyautogui.click()
                    time.sleep(0.5)
                    pass

                elif (s == "01110"):
                    pyautogui.click(button='right')
                    time.sleep(0.5)
                    pass

                elif (s == "01111"):
                    pyautogui.scroll(50)
                    pass

                elif (s == "11111"):
                    pyautogui.scroll(-50)
                    pass


        # 11. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # 12. Display
        cv2.imshow("Image", img)
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
    main()


def vol():
    wCam, hCam = 640, 480
    pTime = 0
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)  # width
    cap.set(4, hCam)  # height
    detector = htm.handDetector(detectionCon=0.60, maxHands=1)        # only one hand at a time

    while True:
        # 1. Find hand Landmarks
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        # 2. Get the tip of the index and middle fingers
        if len(lmList) != 0:

            fingers = detector.fingersUp()
            s = ""
            for i in fingers:
                s += str(fingers[i]);
            if (s == "00000"):
                pass

            elif (s == "01000"):
                cv2.putText(img, "Volume up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                pyautogui.hotkey('volumeup')
                pass

            elif (s == "01100"):
                cv2.putText(img, "Volume Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                pyautogui.hotkey('volumedown')
                pass

            elif (s == "01110"):
                cv2.putText(img, "Mute", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                pyautogui.hotkey('volumemute')
                time.sleep(0.5)
                pass

            elif (s == "01111"):
                cv2.putText(img, "Play", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                pyautogui.hotkey('playpause')
                time.sleep(0.5)
                pass

            elif (s == "11111"):
                cv2.putText(img, "Pause", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                pyautogui.hotkey('playpause')
                #pyautogui.hotkey('stop')
                time.sleep(0.5)
                pass

            elif (s == "01001"):
                cv2.putText(img, "Forward", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                pyautogui.hotkey('alt','right')
                time.sleep(0.5)
                pass

            elif (s == "01011"):
                cv2.putText(img, "Backward", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                pyautogui.hotkey('alt','left')
                time.sleep(0.5)
                pass

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 3)
        cv2.imshow("image", img)
        # if(cv2.waitKey(1) & 0xFF== ord('q')):
        #     break
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
    main()


def task_execution():
    wCam, hCam = 640, 480

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    detector = htm.handDetector(detectionCon=0.70)
    totalFingers = 0
    while True:

        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            fingers = detector.fingersUp()
            totalFingers = fingers.count(1)

            if (totalFingers == 1):

                print("INSTRUCTIONS-")
                print("Based on number of fingers up the software will perform following functions : ")
                print("1 finger : Move Mouse ")
                print("2 finger : Left Click")
                print("3 finger : Right Click")
                print("4 finger : Scroll Up")
                print("5 finger : Scroll Down")

                mouse()

            elif (totalFingers == 2):
                print("INSTRUCTIONS-")
                print("Based on number of fingers up the software will perform following functions : ")
                print("1 finger : Volume Up ")
                print("2 finger : Volume Down")
                print("3 finger : Mute")
                print("4 finger : Play")
                print("5 finger : Pause")
                print("Index and Little Finger Up : Forward")
                print("Index, Ring and Little Finger Up : Backward")

                vol()

        cv2.imshow("Image", img)
        cv2.waitKey(1)


def main():
    print("INSTRUCTIONS-")
    print("A screen will be open once you type START")
    print("Show 1/2 Fingers according to numbering given to the tasks below")
    print("Tasks which you can perform-")
    print("1.AI Virtual Mouse")
    print("2.Gesture Volume control")
    print("Once you are doing a task the only way to end the task is by pressing Escape key")
    query = input("Type START to continue or EXIT to terminate: ")
    if "start" in query or "START" in query or "Start" in query:
        task_execution()
    else:
        exit()


if __name__ == "__main__":
    main()