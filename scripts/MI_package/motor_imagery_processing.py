# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 17:07:06 2020

@author: abhijeet
"""

import matplotlib.pyplot as plt
import numpy as np
import cv2
import scipy.io as sio
import CSP

data_dir = "../data/BCI-IVa/"
person = 1
file_name = "Person" + str(person)
data = sio.loadmat(data_dir + file_name)



