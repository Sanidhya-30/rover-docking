import cv2

cap = cv2.VideoCapture(0)
while True:
    _, src = cap.read()
    src = cv2.rotate(src, cv2.ROTATE_180)
    cv2.imshow("OG",src)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()