import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


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
            if z > 4:
                key = key_list[i]
                outlier.append(key)
        return outlier


cap = cv.VideoCapture(0)

while True:
    _, src = cap.read()
    src = cv.rotate(src, cv.ROTATE_90_CLOCKWISE)
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
    left = [[], []]
    right = [[], []]
    right_avg_x = 0
    right_avg_y = 0
    left_avg_x = 0
    left_avg_y = 0
    center_x = 0
    center_y = 0

    x_axis = val[1]
    y_axis = val[0]

    if len(x_axis) > 0:

        # Differentiate between Left side and Right side
        for i in range(len(x_axis)):

            if val[1][i] > 240:
                right[0].append(x_axis[i])
                right[1].append(y_axis[i])
            else:
                left[0].append(x_axis[i])
                left[1].append(y_axis[i])

        # Remove Outliers
        right_outliers = createDataMap(right)
        left_outliers = createDataMap(left)

        if right_outliers is not None:
            for i in range(len(right_outliers)):
                right[0].remove(right_outliers[i][0])
                right[1].remove(right_outliers[i][1])

        if left_outliers is not None:
            for i in range(len(left_outliers)):
                left[0].remove(left_outliers[i][0])
                left[1].remove(left_outliers[i][1])

        # Calculate centroids for Left side and Right side
        if len(right[0]) > 0:
            right_avg_x = int(round(np.average(right[0])))
            right_avg_y = int(round(np.average(right[1])))

            copy = cv.circle(color, (right_avg_x, right_avg_y),
                             radius=10, color=(0, 255, 0), thickness=-1)

        if len(left[0]) > 0:
            left_avg_x = int(round(np.average(left[0])))
            left_avg_y = int(round(np.average(left[1])))

            copy = cv.circle(copy, (left_avg_x, left_avg_y),
                             radius=10, color=(0, 255, 0), thickness=-1)

        # Find center point of the line
        if ((right_avg_x != 0) and (left_avg_x != 0)):
            center_x = int((right_avg_x + left_avg_x) / 2)
            center_y = int((right_avg_y + left_avg_y) / 2)
            if ((center_x > 0) and (center_y)):
                copy = cv.circle(copy, (center_x, center_y),
                                 radius=10, color=(255, 0, 0), thickness=-1)

    cv.imshow('masked', color)
    cv.imshow('Image', src)
    cv.imshow('img', copy)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
