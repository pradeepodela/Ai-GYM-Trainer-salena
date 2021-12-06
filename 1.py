import cv2
import numpy as np
import posemodule as pm
import time
import pyttsx3
from cvzone.HandTrackingModule import HandDetector
import cvzone

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices)-1].id)

cap2 = cv2.VideoCapture(1)
cap2.set(3, 1280)
cap2.set(4, 720)
detector2 = HandDetector(detectionCon=0.8)

def get_frame():

    success, img = cap2.read()
    img = cv2.flip(img, 1)
    hands, img = detector2.findHands(img, flipType=False)
    img, bbox = cvzone.putTextRect(img, "Welcome to Ai GYM ", [550, 150], 2, 2, offset=50, border=5)
    img, bbox1 = cvzone.putTextRect(img, 'Start', [680, 300], 2, 2, offset=50, border=5)
    img, bbox2 = cvzone.putTextRect(img, 'Stop', [680, 450], 2, 2, offset=50, border=5)
    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]
        length, info = detector2.findDistance(lmList[8], lmList[12])       
        if length < 35:
            bboxs = [bbox, bbox1, bbox2]
            for x, bbox in enumerate(bboxs):
                x1, y1, x2, y2 = bbox
                if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                    userAns = x + 1
                    print(userAns)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
                    if userAns == 2:
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
                        print('correct completed')
                        return userAns
                    if userAns == 3:
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
                        print('correct completed')
                        return userAns
                        
    cv2.imshow("Img", img)
    cv2.waitKey(1)



def speak(audio):
    engine.say(audio)
    engine.runAndWait()
class poseest():
    def __init__(self):
        self.cap = cv2.VideoCapture(1)
        self.detector = pm.poseDetector()
        self.count = 0
        self.dir = 0
        self.pTime = 0

    def get_pose_data(self,x1, x2, x3):

        while True:
            
            success, img = self.cap.read()
            if success:
                img = cv2.resize(img, (1280, 720))
                img = self.detector.findPose(img, False)
                lmList = self.detector.findPosition(img, False)
                if len(lmList) != 0:
                        angle = self.detector.findAngle(img, x1, x2, x3)
                        print(f'this is angle {angle}')
            cv2.imshow("pose", img)

 



    def run(self,countNo,x1,x2,x3,anglemin,anglemax):
        
        
        while True:

            success, img = self.cap.read()
            
            if success:

                img = cv2.resize(img, (1280, 720))
                img = cv2.flip(img, 1)
                
                # img = cv2.imread("AiTrainer/test.jpg")
                img = self.detector.findPose(img, False)
                lmList = self.detector.findPosition(img, False)
                # print(lmList)
                if len(lmList) != 0:
                    # Right Arm
                    angle = self.detector.findAngle(img, x1, x2, x3)
                    # # Left Arm
                    #angle = detector.findAngle(img, 11, 13, 15,False)
                    per = np.interp(angle, (anglemin, anglemax), (0, 100))
                    bar = np.interp(angle, (anglemin, anglemax), (650, 100))
                    # print(f'this is angle {angle}, this is pre {per}')

                    # Check for the dumbbell curls
                    color = (255, 0, 255)
                    if per == 100:
                        color = (0, 255, 0)
                        if self.dir == 0:
                            self.count += 0.5
                            self.dir = 1
                    if per == 0:
                        color = (0, 255, 0)
                        if self.dir == 1:
                            self.count += 0.5
                            self.dir = 0
                    print(self.count)

                    # Draw Bar
                    cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
                    cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
                    cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                                color, 4)

                    # Draw Curl Count
                    
                    cv2.putText(img, str(int(self.count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                                (255, 0, 0), 25)
                    
                    if self.count == countNo:
                        cv2.putText(img, 'DONE', (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                                    (255, 0, 0), 25)
                        print('DONE')
                        
                        self.cap.release()
                        cv2.destroyAllWindows()
                        break
                    
                    cv2.imshow("pose", img)


                

                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print('Error')
                self.cap.release()
        self.cap.release()
        cv2.destroyAllWindows()
        return 'completed'

if __name__ == '__main__':
    while True:
        nm = get_frame()
        print(nm)
        if nm == 3:
            
            cap2.release()
            cv2.destroyAllWindows()
            break
            # poseest().get_pose_data(x1=23, x2=25, x3=27)
        
        if nm == 2:
            
            cap2.release()
            cv2.destroyAllWindows()
            
            speak('welcome   to   Ai   trainer    this   is    your   Ai   gym   trainer   selena   to   train you')

            pst = poseest()
            speak('lets     start     with     the      first      exercise      dumble      lifting     lift     the     dumble     for    5 times     and   then    we    will       move      to     next    exercise')
            #sataus = pst.run(countNo=10,x1=23, x2=25, x3=27,anglemin=150,anglemax=180) 
            sataus = pst.run(countNo=5,x1=11, x2=13, x3=21,anglemin=210,anglemax=310) 
            if sataus == 'completed':
                speak('successfully completed your first exercise take a break for next 10 seconds')
                print('changing to next exercise')
                time.sleep(10)
                speak('starting exercise 2')
                pst = poseest()
                speak('clap your hands for 5 times')
                sataus = pst.run(countNo=5,x1=13,x2=11,x3=23,anglemin=150,anglemax=170) 
                print('exercise started')
                speak('congratulations you have completed your training for the day ')
                speak('meet   you tomorrow good bye')
                break
            # poseest().get_pose_data(x1=23, x2=25, x3=27)
        