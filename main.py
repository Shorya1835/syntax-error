#using multiprocessing to parallely execute 2 processes

import multiprocessing as mp
import os, time, numpy
from pynput import keyboard

flag = False
#controls the execution of program

tup = (90, True)
#this is the global value to be used
#it stores angle and bool for shoot/not_shoot

def input_task():
    '''
    takes the tup from the image processing file
    '''
    global tup
    tup = send_tuple()
    

def output_task():
    '''
    gives the tup to the game process
    '''
    global tup
    receive_tuple(tup)

def main_process():
    inputProcess = mp.Process(target= input_task)
    outputProcess = mp.Process(target= output_task)

    inputProcess.start()
    outputProcess.start()

    inputProcess.join()
    outputProcess.join()
     
def on_press(key):
    if key == keyboard.Key.esc:
        return False
    else:
        main_process()

if __name__ == '__main__': 
    with keyboard.Listener(on_press= on_press) as listener:
        listener.join()
