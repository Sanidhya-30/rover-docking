import cv2

def dock(rover):
    label_font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        dock_x, dock_y, masked_image, src_image = rover.camera.capture()
        cv2.imshow('mask', masked_image)
        cv2.waitKey(1)

        if (dock_x - 320) > 25:
            cv2.putText(masked_image, "Move Right", (50, 50), label_font, 0.5, (255, 0, 0), 2)
            print("Right Logged")
            
        if (dock_x - 320) < -25:
            cv2.putText(masked_image, "Move Left", (50, 50), label_font, 0.5, (255, 0, 0), 2)
            print("Left Logged")


        print('docking')

if __name__ == '__main__':
    pass