# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 21:07:27 2023

@author: Shree
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

angle = 0
shoot = False

def stats(img):
    return np.min(img), np.mean(img), np.max(img)


def extractAngle(img):
    """
    returns angle between -1 to 1 corresponding to -90 to 90
    """
    global height, width, indexarr
    img /= 255.

    # break the image into 2 channels (green and redblue)
    # and apply thresholds according to how red+blue or green a pixel is
    
    green = img[:, :, 1]
    redblue = img[:, :, 0] + img[:, :, 2]

    rbLThresh = 0.2
    rbUThresh = 1.2
    
    green[redblue < rbLThresh] = 0
    green[redblue > rbUThresh] = 0

    green /= redblue
    greenThresh = 0.6
    np.nan_to_num(green, copy=False)
    green = green > greenThresh  # finally `green` is a boolean matrix

    # break matrix into two halves, left for angle, right for shoot
    w, h = width//2, height
    lImg = green[:,:w]
    rImg = green[:,w:]

    #############DETECT ANGLE################

    # find the average x and y coordinates and standard deviatons
    temp = indexarr*lImg[:, :, None]/np.sum(lImg)
    np.nan_to_num(temp, copy=False)
    x, y = temp[:, :, 0].sum(), temp[:, :, 1].sum()

    distx, disty = lImg.sum(1), lImg.sum(0)
    stdx, stdy = distx.std(), disty.std()

    # print(x, y, '\n', stdx, stdy)

    # remove outliers according to how far they are from the mean
    size = 4
    lImg[:max(int(y-size*stdy), 0), :]        = False
    lImg[min(int(y+size*stdy), h-1):, :] = False

    lImg[:, :max(int(x-size*stdx), 0)]        = False
    lImg[:,min(int(x+size*stdx), w-1):]   = False

    # calculate angle using means and deviations of scatter plot

    temp = indexarr*lImg[:, :, None]
    count = lImg.sum()
    
    xM, yM = temp[:,:,0].sum()/count, temp[:,:,1].sum()/count
    xyM = (temp[:,:,0]*temp[:,:,1]).sum()/count
    y2M = np.square(temp[:,:,1]).sum()/count

    angle = -np.arctan((xM*yM - xyM)/(yM**2-y2M))
    if yM**2==y2M or count==0:
        angle = 0

    #############DETECT SHOOT################
    #print(rImg.sum()/(w*h))
    shoot = rImg.sum()/(w*h) < 0.002

    return green, 2*angle/np.pi, shoot

    # plt.imshow(green, cmap='gray')
    # plt.plot(dist)
    # plt.show()

def detector_init():
    global angle, shoot, height, width, indexarr
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

    indexarr = np.zeros((height, width//2, 2))
    indexarr[:, :, 0] = np.arange(width//2).reshape(1, -1)
    indexarr[:, :, 1] = np.arange(height).reshape(-1, 1)

    while showing:
        try:
            vision_img, angle, shoot = extractAngle(image.astype('float32'))
            
            #print(angle, shoot)
            # vision_img = extractAngle(mpimg.imread('test1.jpg')/255.) #####
            
            vision_img = np.repeat(vision_img[:,:,None]*255, repeats=3, axis=2).astype(np.uint8)   #REMOVABLE

            cv2.imshow("video", vision_img)                                                        #REMOVABLE
            cv2.imshow("actual", image)                                                            #REMOVABLE
            showing, image = video.read()
            image = cv2.flip(image, 1)
            image[:, width//2-10:width//2+10 :] = [0,0,255]
            
            
            # exit if escape pressed
            key = cv2.waitKey(5)
            if key == 27:
                break
        except KeyboardInterrupt:
            break
        
    # stop video capture
    video.release()
    cv2.destroyWindow("preview")

if __name__ == '__main__':
    detector_init()