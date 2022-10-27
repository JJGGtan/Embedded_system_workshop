import cv2
import mediapipe as mp
import time
import controller as cnt
from pyfirmata import Arduino ,SERVO,util

time.sleep(2.0)

mp_draw=mp.solutions.drawing_utils  #use f#convert color BGR to RGBunction drawing_utils to draw straight connect landmark point
mp_hand=mp.solutions.hands  #use function hands to find hand on camera


tipIds=[4,8,12,16,20]  # media-pipe position  of fingertips

def check_user_input(input):
    try:
        # Convert it into integer
        val = int(input)
        # print("Input is an integer number. Number = ", val)
        bv = True
    except ValueError:
        try:
            # Convert it into float
            val = float(input)
            # print("Input is a float  number. Number = ", val)
            bv = True
        except ValueError:
            # print("No.. input is not a number. It's a string")
            bv = False
    return bv            

cport = input('Enter the camera port: ')
while not (check_user_input(cport)):
    print('Please enter a number not string')
    cport = input('Enter the camera port: ')

comport = input('Enter the arduino board COM port: ')
while not (check_user_input(comport)):
    print('Please enter a number not string')
    comport = input('Enter the arduino board COM port: ')

board=Arduino('COM'+comport)  
pin=9   
board.digital[pin].mode=SERVO #Set mode of pin

video=cv2.VideoCapture(0)  #OpenCamera at index position 0 

with mp_hand.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as hands:  #(min_detection_confidence, min_tracking_confidence) are Value to considered for detect and tracking image
    while True:
        ret,image=video.read()  #Read frame in camera video
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #convert color BGR to RGB
        image.flags.writeable=False  #to improve nothing drawed in image
        results=hands.process(image)  #process image
        image.flags.writeable=True   #can drawing  image
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #convert color RGB to BGR
        lmList=[]

        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy]) #input number hand_landmark position and position of spot position hand_landmark
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS) #drawing hand skeleton from hand_landmark point
        fingers=[]
        if len(lmList)!=0:
            if lmList[9][1]<lmList[5][1]:
                if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:#creat condition for count thumb
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)    
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]: #creat condition for count fingers 
                    fingers.append(1)
                else:
                    fingers.append(0)
            total=fingers.count(1)
            cnt.servo(total,pin) #import function in module to controll arduino output
            """
            creat condition to put text in frame

            """
            if ((results.multi_hand_landmarks))!="None":
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, str(total), (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "Servo", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
            

        cv2.imshow("Frame",image)#show edited image
        k=cv2.waitKey(1)
        if k==ord('q'):#press "q" to exit programe
            break
video.release()
cv2.destroyAllWindows()

