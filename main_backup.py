#without using multiprocessing 

import os, time, numpy
from pynput import keyboard
from game_aks import *
from detector import *

#flag = False
#controls the execution of program

global_angle = 0
#this is the global value to be used
#it stores angle and bool for shoot/not_shoot

def detector_task():
    '''
    takes the angle from the image processing file
    '''
    global global_angle

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
            vision_img, global_angle = extractAngle(image.astype('float32'))
            print(global_angle)
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


if __name__ == '__main__': 
    detector_task()
    main_game_execution()