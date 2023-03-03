import cv2
from .util import keyboard_shutdown
import math
from .Camera import camera
import time

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

def align(rover, change):
    changeDirection(rover, angle=-90)
    moveF_L(rover, spd=2, d=change)
    changeDirection(rover, angle=-90)



def dock(rover):
    
    label_font = cv2.FONT_HERSHEY_SIMPLEX
    rover.setupAndArm()
    rover.changeVehicleMode('GUIDED')
   
    while True:
        
        dock_x, masked_image = rover.camera.capture()
        masked_image = cv2.rotate(masked_image, cv2.ROTATE_180)
        #cv2.imshow('OG', src_image)
        FrameCenter_X = round(masked_image.shape[1]/2)
        FrameCenter_Y = round(masked_image.shape[0]/2)
        masked_image = cv2.circle(masked_image, (FrameCenter_X, FrameCenter_Y), radius=10, color=(255, 0, 0), thickness=-1)
        drift = (dock_x-FrameCenter_X)
        # print('drift', drift)
        K=1
        
        if dock_x is not 0:
            
            if (drift) > 25:
                cv2.putText(masked_image, "Move Left", (50, 50), label_font, 0.5, (255, 0, 0), 2)
                align(rover, (K*drift))

            elif (drift) < -25:
                cv2.putText(masked_image, "Move Right", (50, 50), label_font, 0.5, (255, 0, 0), 2)
                align(rover, (-K*drift))

            elif -25 < (drift) < 25 :
                cv2.putText(masked_image, "Move Forward", (50, 50), label_font, 0.5, (255, 0, 0), 2)
                moveF(rover,spd=2)
        
        else:
            print("Drone not detected")
            # changeDirection(rover, angle=90)
            # moveF_L(rover, spd=2, d=length)
            # changeDirection(rover, angle=-90)
        
        cv2.imshow('masked', masked_image)
        cv2.waitKey(1)


if __name__ == '__main__':
    pass