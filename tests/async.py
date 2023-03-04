from pymavlink import mavutil
import argparse
from ..src.Rover import *

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()
print ('Connecting to vehicle on: %s' % args.connect)

rover = Rover(roverSerial='abc', connection=args.connect)

label_font = cv2.FONT_HERSHEY_SIMPLEX
rover.setupAndArm()
rover.changeVehicleMode('GUIDED')

def align(rover):
    print('Aligning')
    rover.changeYaw(angle=90,speed=0.02)
    rover.moveForward_L(speed=2,d=2)
    rover.changeYaw(angle=-90,speed=0.02)
    print('Done Aligning')

def dock():
    while True:
        dock_x, masked_image = rover.camera.capture()
        masked_image = cv2.rotate(masked_image, cv2.ROTATE_180)
        
        FrameCenter_X = round(masked_image.shape[1]/2)
        FrameCenter_Y = round(masked_image.shape[0]/2)
        masked_image = cv2.circle(masked_image, (FrameCenter_X, FrameCenter_Y), radius=10, color=(255, 0, 0), thickness=-1)
        drift = (dock_x-FrameCenter_X)
        
        K=1
        
        if dock_x is not 0:
            print('Looping.....')
            if (drift) > 25:
                cv2.putText(masked_image, "Move Left", (50, 50), label_font, 0.5, (255, 0, 0), 2)
                align(rover, (K*drift))

            elif (drift) < -25:
                cv2.putText(masked_image, "Move Right", (50, 50), label_font, 0.5, (255, 0, 0), 2)
                align(rover, (-K*drift))

            elif -25 < (drift) < 25 :
                cv2.putText(masked_image, "Move Forward", (50, 50), label_font, 0.5, (255, 0, 0), 2)
                rover.moveForward(speed=2)
        
        else:
            print("Drone not detected")
        
        cv2.imshow('masked', masked_image)
        cv2.waitKey(1)

dock()