from pyfirmata import Arduino ,SERVO,util
from time import sleep

port='COM7' #chose port in arduino IDE
#Roll = [0,30,60,90,135,180]
pin=9   
board=Arduino(port)
board.digital[pin].mode=SERVO #Set mode of pin

def rotateservo(pin,angle):#creat function to controll servo
    board.digital[pin].write(angle)
    sleep(0.015)
    
def servo(total):#creat condition to controll servo
    if (total)==0:
            rotateservo(pin,0)
    elif (total)==1:
            rotateservo(pin,30)
    elif (total)==2:
            rotateservo(pin,60)
    elif (total)==3:
            rotateservo(pin,90)
    elif (total)==4:
            rotateservo(pin,135)
    elif (total)==5:
            rotateservo(pin,180)                         



