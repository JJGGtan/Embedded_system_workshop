import math
import cv2 as cv
import mediapipe as mp
import controller as cnt
import pyfirmata

mp_draw=mp.solutions.drawing_utils#use function drawing_utils to draw straight connect landmark point
mp_hand=mp.solutions.hands#use function hands to find hand on camera

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

board=pyfirmata.Arduino('COM'+comport)  
led_1=board.get_pin('d:13:o') #Set pin to output
led_2=board.get_pin('d:12:o')
led_3=board.get_pin('d:11:o')
led_4=board.get_pin('d:10:o')
led_5=board.get_pin('d:9:o')

Video=cv.VideoCapture(int(cport)) #OpenCamera


def show_PER(Percent):#function to show percent on display
    if 0<=int(Percent)<=100:
       cv.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv.FILLED)
       cv.putText(image, str(int(Percent)), (45, 375), cv.FONT_HERSHEY_SIMPLEX,
        2, (255, 0, 0), 5)
       cv.putText(image, "  %", (100, 375), cv.FONT_HERSHEY_SIMPLEX,
        2, (255, 0, 0), 5)
    elif int(Percent)>100:
        cv.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv.FILLED)
        cv.putText(image, str(100), (45, 375), cv.FONT_HERSHEY_SIMPLEX,
            2, (255, 0, 0), 5)
        cv.putText(image, "  %", (100, 375), cv.FONT_HERSHEY_SIMPLEX,
            2, (255, 0, 0), 5)
    elif int(Percent)<0:
        cv.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv.FILLED)
        cv.putText(image, str(100), (45, 375), cv.FONT_HERSHEY_SIMPLEX,
            2, (255, 0, 0), 5)
        cv.putText(image, "  %", (100, 375), cv.FONT_HERSHEY_SIMPLEX,
            2, (255, 0, 0), 5)


def distance(x1,y1,x2,y2):#function to calculate distance and draw line between (x1,y1) and (x2,y2)
    MIDLE_BX,MIDLE_BY=int((int(x1)+int(x2))/2),int((int(y1)+int(y2))/2)
    DX,DY=x1-x2,y1-y2
    DT=int(math.sqrt((DX**2)+(DY**2)))
    cv.circle(image,(x1,y1),8,(255,0,255), cv.FILLED)
    cv.circle(image,(x2,y2),8,(255,0,255), cv.FILLED)
    cv.circle(image,(MIDLE_BX,MIDLE_BY),8,(0,0,255), cv.FILLED)
    cv.line(image,(x1,y1),(x2,y2),(0,0,255),5, cv.FILLED)
    return DT



with mp_hand.Hands(min_detection_confidence=0.5,
              min_tracking_confidence=0.5) as hands:#(min_detection_confidence, min_tracking_confidence) are Value to considered for detect and tracking image
    while True:
        ret,image=Video.read()#Read frame in camera video
        image=cv.cvtColor(image,cv.COLOR_BGR2RGB) #convert color BGR to RGB
        image.flags.writeable=False #to improve nothing drawed in image
        results=hands.process(image) #process image
        image.flags.writeable=True #can drawing  image
        image=cv.cvtColor(image,cv.COLOR_RGB2BGR) #convert color RGB to BGR

        lmList=[]
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id,lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy=int(lm.x*w),int(lm.y*h)
                    lmList.append([id,cx,cy]) #input number hand_landmark position and position of spot position hand_landmark
                mp_draw.draw_landmarks(image,hand_landmark,mp_hand.HAND_CONNECTIONS) #drawing hand skeleton from hand_landmark point
                FIXR=math.sqrt(((lmList[17][1]-lmList[0][1])**2)+((lmList[17][2]-lmList[0][2])**2))# Ratio of picture for calculate
                
                POSF_1x,POSF_1y=(lmList[4][1],lmList[4][2])#position of index fingertip 
                POSF_2x,POSF_2y=(lmList[8][1],lmList[8][2])#position of thumb fingertip

                Distance_1=distance(POSF_1x,POSF_1y,POSF_2x,POSF_2y)
                PER=(int(Distance_1*100/(FIXR*1.4)))-9
                print((PER))
                
                cnt.PERLED(PER,led_1,led_2,led_3,led_4,led_5) #import function in module to controll arduino output
                """
                create condition to output on display
                """
                if int(PER)%5==0:
                    show_PER(PER)
                elif int(PER)%5!=0:
                    MAP=int(PER/5)*5
                    show_PER(MAP)
                






        cv.imshow("frame",image) #out put frame of video processed

        EXit=cv.waitKey(1)
        if EXit==ord("q"):
            break













