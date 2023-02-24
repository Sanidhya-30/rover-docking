import cv2
from .util import keyboard_shutdown
import math
from .Camera import camera

length = 45
breadth = 30

def coverForwardArea(rover, d, spd):
    rover.moveForward(x=d,speed=spd)

def coverBackwardArea(rover, d, spd):
    rover.moveBackward(x=d,speed=spd)

def changeDirection(rover, angle):
        rover.changeYaw(angle=angle,speed=0.02)


def dock(rover): #take frame and avgX as argument
    
    label_font = cv2.FONT_HERSHEY_SIMPLEX
   
    while True:
        
        dock_x, masked_image, src_image = rover.camera.capture()
        cv2.imshow('mask', masked_image)
        cv2.waitKey(1)
        print('docking')

        FrameCenter = src_image.shape[1]/2
        drift = (dock_x-FrameCenter)
        # determine K
        K = 1

        if (drift) > 25:
            cv2.putText(masked_image, "Move Right", (50, 50), label_font, 0.5, (255, 0, 0), 2)
            changeDirection(rover, (K*drift))
            print("Moving Right by",drift)
            
        elif (drift) < -25:
            cv2.putText(masked_image, "Move Left", (50, 50), label_font, 0.5, (255, 0, 0), 2)
            changeDirection(rover, (K*drift))
            print("Moving Left by",drift)
        
        elif -25 < (drift) < 25 :
            cv2.putText(masked_image, "Move Left", (50, 50), label_font, 0.5, (255, 0, 0), 2)
            coverForwardArea(rover,spd=2)
            print("Moving Left by",drift)
            

# def changeLane(rover,drift=breadth):
    
#     H = math.sqrt(((length/2)**2)+(drift**2))
#     theta = math.atan((drift)/(length/2))

#     try:
#         while(rover.back_edge.checkDriveOk() == True):
            
#             coverForwardArea(rover,d=int((drift/2)),spd=2)
#             changeDirection(rover, theta)
            
#             if (rover.front_edge.checkDriveOk() == True):
#             # Lane End
#                 changeDirection(rover, -theta)
#                 coverBackwardArea(rover,d=int((drift/2)),spd=2)
#                 #check drone status
#                 #call dock function()
#                 break

#             else:
#                 coverForwardArea(rover,d=int((H)),spd=2)
#                 changeDirection(rover, (-theta))
#                 coverBackwardArea(rover,d=int((3*drift)/2),spd=2)

#     except KeyboardInterrupt:
#         keyboard_shutdown() 


if __name__ == '__main__':
    pass