import cv2
from .util import keyboard_shutdown
import math
from .Camera import camera

length = 45
breadth = 30

def moveF(rover, spd):
    rover.moveForward(speed=spd)

def moveB(rover, spd):
    rover.moveForward(speed=spd)

def moveF_L(rover, spd, d):
    rover.moveForward_L(speed=spd,d=d)

def moveB_L(rover, spd, d):
    rover.moveBackward_L(speed=spd,d=d)

def changeDirection(rover, angle):
        rover.changeYaw(angle=angle,speed=0.02)

def Align(change):
    changeDirection(angle=90,speed=0.02)
    moveF_L(spd=2, d=change)
    changeDirection(angle=90,speed=0.02)



def dock(rover):
    
    label_font = cv2.FONT_HERSHEY_SIMPLEX
   
    while True:
        
        dock_x, masked_image, src_image = rover.camera.capture()
        src_image = cv2.rotate(src_image, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow('mask', src_image)
        cv2.waitKey(1)

        FrameCenter = src_image.shape[1]/2
        drift = (dock_x-FrameCenter)
        # determine K
        K = 1
        print(FrameCenter)
        print(dock_x)


        if (drift) > 25:
            cv2.putText(masked_image, "Move Right", (50, 50), label_font, 0.5, (255, 0, 0), 2)
            Align(K*drift)
            print("Moving Right by",K*drift)
            
        elif (drift) < -25:
            cv2.putText(masked_image, "Move Left", (50, 50), label_font, 0.5, (255, 0, 0), 2)
            Align(K*drift)
            print("Moving Left by",K*drift)
        
        elif -25 < (drift) < 25 :
            cv2.putText(masked_image, "Move Left", (50, 50), label_font, 0.5, (255, 0, 0), 2)
            moveF(rover,spd=2)
            print("Docking")


if __name__ == '__main__':
    pass