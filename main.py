#using multiprocessing to parallely execute the 2 processes

import multiprocessing as mp
import os, time, numpy
#from pynput import keyboard
from game import *
from detector import *

#flag = False
#controls the execution of program

#state of the bullet
bullet_state = False

global_angle = 0
#this is the global value to be used
#it stores angle and bool for shoot/not_shoot


class detectorProcess(mp.Process):
    def __init__(self):
        #assign the detector task function to this process
        super().__init__(target= detector_task)

    def __del__(self):
        # stop video capture
        video.release()
        cv2.destroyWindow("preview")


class gameProcess(mp.Process):

    def __init__(self):
        #assigning the game to this process target
        super().__init__(target= main_game_execution)


    def start(self):
        #init()
        super().start()

    def __del__(self):
        pygame.quit()


def main():
    p1 = detectorProcess()
    p2 = gameProcess()
    p1.start()
    p2.start()


if __name__ == '__main__': 
    main()