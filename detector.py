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
    """
    returns angle between -1 to 1 corresponding to -90 to 90
    """
    img /= 255.
    
    # break the image into 2 channels (green and redblue)
    # and apply thresholds according to how red+blue or green a pixel is

    green = img[:, :, 1]
    redblue = img[:, :, 0] + img[:, :, 2]

    rbLThresh = redblue.mean()*0.6
    rbUThresh = redblue.mean()*1.
    
    green[redblue < rbLThresh] = 0
    green[redblue > rbUThresh] = 0

    green /= redblue
    # print(green.mean())
    greenThresh = green.mean()*3
    
    np.nan_to_num(green, copy=False)
    green = green > greenThresh  # finally `green` is a boolean matrix

    # find the average x and y coordinates and standard deviatons
    temp = indexarr*green[:, :, None]/np.sum(green)
    np.nan_to_num(temp, copy=False)
    x, y = temp[:, :, 0].sum(), temp[:, :, 1].sum()

    distx, disty = green.sum(1), green.sum(0)
    stdx, stdy = distx.std(), disty.std()

    # print(x, y, '\n', stdx, stdy)

    # remove outliers according to how far they are from the mean
    green[:max(int(y-6*stdy), 0), :]        = False
    green[min(int(y+6*stdy), height-1):, :] = False

    green[:, :max(int(x-6*stdx), 0)]        = False
    green[:, min(int(x+6*stdx), width-1)]   = False

    # calculate angle using means and deviations of scatter plot
    
##    distx, disty = green.sum(1), green.sum(0)
##    stdx, stdy = distx.std(), disty.std()
##    print(stdx/stdy)

    temp = indexarr*green[:, :, None]
    count = green.sum()
    
    xM, yM = temp[:,:,0].sum()/count, temp[:,:,1].sum()/count
    xyM = (temp[:,:,0]*temp[:,:,1]).sum()/count
    y2M = np.square(temp[:,:,1]).sum()/count

    angle = -np.arctan((xM*yM - xyM)/(yM**2-y2M))
    if yM**2==y2M or count==0:
        angle = 0
        
    return green, 2*angle/np.pi

    # plt.imshow(green, cmap='gray')
    # plt.plot(dist)
    # plt.show()


# image = mpimg.imread('test1.jpg')
# image = image/np.max(image)

# start video capture
cv2.namedWindow("video")                                                      #REMOVABLE
cv2.namedWindow("actual")                                                     #REMOVABLE

video = cv2.VideoCapture(0)
showing, image = video.read()


#image = mpimg.imread('test1.jpg')/255. ####

# indexarr is a matrix containing the index of each entry as its value (both x and y)
# [:,:,0] is x coordinate and [:,:,1] is y coordinate
height, width = image.shape[:2]

indexarr = np.zeros((height, width, 2))
indexarr[:, :, 0] = np.arange(width).reshape(1, -1)
indexarr[:, :, 1] = np.arange(height).reshape(-1, 1)

while showing:
    try:
        vision_img, angle = extractAngle(image.astype('float32'))
        print(angle)
        # vision_img = extractAngle(mpimg.imread('test1.jpg')/255.) #####
        
        vision_img = np.repeat(vision_img[:,:,None]*255, repeats=3, axis=2).astype(np.uint8)   #REMOVABLE

        cv2.imshow("video", vision_img)                                                        #REMOVABLE
        cv2.imshow("actual", image)                                                            #REMOVABLE
        showing, image = video.read()
        image = cv2.flip(image, 1)
        
        
        # exit if escape pressed
        key = cv2.waitKey(5)
        if key == 27:
            break
    except KeyboardInterrupt:
        break
    
# stop video capture
video.release()
cv2.destroyWindow("preview")
