# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 16:13:47 2019

@author: abhijeet
"""
import os
import numpy as np
from matplotlib import pyplot as plt
import cv2
import tensorflow as tf

def normalize(data):
    data = data - data.mean(axis=0)
    data = data / (np.abs(data).max(axis = 0)-np.abs(data).min(axis = 0))
    return data

###### Loading Features #######
exp_name = os.listdir( "../spectro/active/" )
active_data = "../spectro/active/"
drowsy_data = "../spectro/drowsy/"

l = len(exp_name)
container = np.zeros([2*l,200,200])
label = np.zeros([2*l])
for i in range(l):
        
    img_load = cv2.imread( active_data + exp_name[i])
    img_load = cv2.cvtColor(img_load, cv2.COLOR_BGR2GRAY)
    img_load = normalize(img_load)
    img_load = cv2.resize(img_load, (200,200), interpolation = cv2.INTER_AREA) 
    container[2*i] = img_load 
    label[2*i] = 1
    img_load = cv2.imread( drowsy_data + exp_name[i])
    img_load = cv2.cvtColor(img_load, cv2.COLOR_BGR2GRAY)
    img_load = normalize(img_load)
    img_load = cv2.resize(img_load, (200,200), interpolation = cv2.INTER_AREA)
    container[2*i+1] = img_load 
    label[2*i+1] = -1

#### CNN MODEL ########
container = container.reshape(2*l, 200, 200, 1)
model = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(20, (3,3), activation='relu', input_shape=(200, 200, 1)),
  tf.keras.layers.MaxPooling2D(2, 2),
  tf.keras.layers.Conv2D(20, (3,3), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(500, activation='relu'),
  tf.keras.layers.Dense(1, activation='softmax')
])  
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()
##### 
model.fit(container, label , epochs=5)
#test_loss = model.evaluate(test_images, test_labels)
