# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 16:13:47 2019

@author: abhijeet
"""

from PIL import Image as img
import os
from numpy import asarray
from matplotlib import pyplot as plt

active = os.listdir( "../spectro/active/" )
drowsy = os.listdir( "../spectro/drowsy/" )

img_load = img.open("../spectro/drowsy/" + active[4])
plt.imshow(img_load)
training_data = asarray(img_load)[:,:,:]

