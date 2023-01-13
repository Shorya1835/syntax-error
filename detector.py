# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 21:07:27 2023

@author: Shree
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img

image = img.imread('test1.jpg')
width, height = image.shape[:2]
plt.imshow(image)