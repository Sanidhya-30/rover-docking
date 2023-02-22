import cv2 as cv
import numpy as np


def createDataMap(array):
    outlier = []
    dict = {}
    mean_x = (np.average(array[0]))
    mean_y = (np.average(array[1]))

    center_p = np.array((mean_x, mean_y))

    for i in range(len(array[0])):
        point = np.array((array[0][i], array[1][i]))
        point_tuple = (array[0][i], array[1][i])
        distance = np.linalg.norm(center_p - point)
        data = {point_tuple: distance}
        dict.update(data)

    if len(dict) > 2:
        val_list = list(dict.values())
        key_list = list(dict.keys())
        mean = np.mean(val_list)
        sd = np.std(val_list)
        for i in range(len(val_list)):
            z = (val_list[i] - mean) / sd
            if z > 0.5 or z < -0.5: # check minus 4
                key = key_list[i]
                outlier.append(key)
        return outlier




def dock():
    cap = cv.VideoCapture(0)
    while True:
        _, src = cap.read()

        hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)

        # Define the range of red color in HSV
        lower1 = np.array([0, 160, 100])  # S = 155, V = 84
        upper1 = np.array([5, 255, 255])  # 10

        # upper boundary RED color range values; Hue (160 - 180)
        lower2 = np.array([175, 160, 100])  # 160
        upper2 = np.array([179, 255, 255])

        lower_mask = cv.inRange(hsv, lower1, upper1)
        upper_mask = cv.inRange(hsv, lower2, upper2)

        full_mask = lower_mask + upper_mask

        # Threshold the HSV image to get only red colors
        color = cv.bitwise_and(src, src, mask=full_mask)
        val = np.nonzero(color)
        copy = np.copy(color)
        avg_x = 0
        avg_y = 0
        center_x = 0
        center_y = 0

        x_axis = list(val[1])
        y_axis = list(val[0])
        data = [x_axis,y_axis]
        if len(x_axis) > 0:

            # Remove Outliers
            outliers = createDataMap(data)

            if outliers is not None:
                for i in range(len(outliers)):
                    data[0].remove(outliers[i][0])
                    data[1].remove(outliers[i][1])

            for i in range(len(outliers)):
                copy[outliers[i][1],outliers[i][0],0] = 0
                copy[outliers[i][1],outliers[i][0],1] = 0
                copy[outliers[i][1],outliers[i][0],2] = 0
            
            # Calculate centroids
            if len(data[0]) > 0:
                avg_x = int(round(np.average(data[0])))
                avg_y = int(round(np.average(data[1])))

                copy = cv.circle(copy, (avg_x, avg_y),
                                radius=10, color=(0, 255, 0), thickness=-1)

        cv.imshow('Image', src)
        cv.imshow('copy', copy)

        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()