# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 21:07:27 2023

@author: Shree
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

def stats(img):
    return np.min(img), np.mean(img), np.max(img)


def extractAngle(img):

    img /= 255.
    
    # break the image into 2 channels (green and redblue)
    # and apply thresholds according to how gray or green a pixel is

    green = img[:, :, 1]
    redblue = img[:, :, 0] + img[:, :, 2]

    grayThresh = img.mean()/0.4
    green[green+redblue < grayThresh] = 0

    greenThresh = 0.2
    green /= redblue
    green = green > greenThresh  # finally `green` is a boolean matrix

    # find the average x and y coordinates and standard deviatons
    temp = indexarr*green[:, :, None]/np.sum(green)
    x, y = temp[:, :, 0].sum(), temp[:, :, 1].sum()

    distx, disty = green.sum(1), green.sum(0)
    stdx, stdy = distx.std(), disty.std()

    # remove outliers according to how far they are from the mean
    green[:int(y-6*stdy), :] = False
    green[int(y+6*stdy):, :] = False

    green[:, :int(x-6*stdx)] = False
    green[:, int(x+6*stdx):] = False

    # calculate angle using deviation
    distx, disty = green.sum(1), green.sum(0)
    stdx, stdy = distx.std(), disty.std()

    return stdx/stdy

    # plt.imshow(green, cmap='gray')
    # plt.plot(dist)
    # plt.show()


# image = mpimg.imread('test1.jpg')
# image = image/np.max(image)

# start video capture
cv2.namedWindow("Video")
video = cv2.VideoCapture(0)
showing, image = video.read()

# indexarr is a matrix containing the index of each entry as its value (both x and y)
# [:,:,0] is x coordinate and [:,:,1] is y coordinate
height, width = image.shape[:2]

indexarr = np.zeros((height, width, 2))
indexarr[:, :, 0] = np.arange(width).reshape(1, -1)
indexarr[:, :, 1] = np.arange(height).reshape(-1, 1)

while showing:
    try:
        cv2.imshow("Video", image)
        showing, image = video.read()
        print(extractAngle(image.astype('float32')))

        # exit if escape pressed
        key = cv2.waitKey(10)
        if key == 27:
            break
    except KeyboardInterrupt:
        break
    
# stop video capture
video.release()
cv2.destroyWindow("preview")
