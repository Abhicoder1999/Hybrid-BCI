import numpy as np
import pandas as pd
import scipy.io
from matplotlib import pyplot as plt
from scipy.fftpack import fft
from scipy.signal import butter
from scipy.signal import sosfilt
from scipy.signal import spectrogram
from scipy.ndimage import gaussian_filter
import tensorflow as tf
import os
import zipfile



def segment (data,Fs):
    
    data["time"] = tmstamp[:,4];
    tmax = data["time"][308867]
    tmin = data["time"][0]
    k = (tmax-tmin)/3
    t1 = k + tmin
    t2 = 2*k + tmin
    wlen = 6;
    aseg = data[(data["time"]>=tmin+wlen/2.0) & (data["time"]<=t1-wlen/2.0)]
    useg = data[(data["time"]>t1+wlen/2.0) & (data["time"]<=t2-wlen/2.0)]
    sseg = data[(data["time"]>t2+wlen/2.0)&(data["time"]<=tmax-wlen/2.0)]
    
    return aseg,useg,sseg;

def preprocessing(data,Fs):
    N,nch = data.shape
    xfil = np.zeros((N,nch))
    yfil = np.zeros((N,nch))
    fpass = [2*0.5/Fs,2*20.0/Fs]#from 0.5 to 30hz bpf
    sos = butter(10, fpass, 'bandpass', output='sos')
    for i in range(nch):
            tdata = data[:,i]
            tdata_ = sosfilt(sos, tdata)
            fdata_ = np.abs(fft(tdata_))         
            xfil[:,i] = tdata_
            yfil[:,i] = fdata_
    return xfil,yfil
    
def normalize(data):
    data = data - data.mean(axis=0)
    data = data / (np.abs(data).max(axis = 0)-np.abs(data).min(axis = 0))
    return data
    
def fdesign(tdata,Fs):
    fdata = fft(tdata)
    T = np.divide(1,Fs)    
    N = len(tdata)
    l = np.linspace(0.0, 1.0/(2.0*T), N//2)
    nfdata =  2.0/N * np.abs(fdata[0:N//2])
    fpass = [2*0.5/Fs,2*30.0/Fs]
    sos = butter(10, fpass, 'bandpass', output='sos')
    fil_data = sosfilt(sos, tdata)
    fil_nfdata = 2.0/N * np.abs(fft(fil_data)[0:N//2])
    
    plt.subplot(2,1,1)
    plt.plot(tdata,'r')
    plt.subplot(2,1,2)
    plt.plot(l,nfdata,'r')
    
    plt.subplot(2,1,1)
    plt.plot(fil_data)
    plt.subplot(2,1,2)
    plt.plot(l,fil_nfdata)
    
def dualplt(tdata,fdata,Fs):
    T = np.divide(1,Fs)    
    N = len(fdata)
    l = np.linspace(0.0, 1.0/(2.0*T), N//2)
    nfdata =  2.0/N * np.abs(fdata[0:N//2])
    plt.subplot(2,1,1)
    plt.plot(tdata)
    plt.subplot(2,1,2)
    plt.plot(l,nfdata)
    

def spectro(tdata,Fs):
    f, t, Sxx = spectrogram(tdata, Fs,nfft = 1024,nperseg = 300)
    Sxx = gaussian_filter(Sxx, sigma=2)
    #add opening closing for more prominent effect
    plt.pcolormesh(t,f[0:513//3], Sxx[0:513//3,:])
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
    pass    

def ICA():
    pass

#####Data Extraction
file = scipy.io.loadmat('../data/EEG_Data/eeg_record8.mat')
mdata = file["o"]
mtype = mdata.dtype
ndata = {n: mdata[n][0,0] for n in mtype.names}

Fs = ndata["sampFreq"][0][0]
data_raw = ndata["data"]
marker = ndata["marker"]
tmstamp = ndata["timestamp"]
trials = ndata["trials"][0,:,:,:]

print("ok1")

data = pd.DataFrame(data_raw)
segments = segment(data,tmstamp)
data = np.array(data)
aseg = np.array(segments[0].iloc[0:50000 , 3:17])
useg = np.array(segments[1].iloc[0:50000 , 3:17])
sseg = np.array(segments[2].iloc[0:50000 , 3:17])

print("ok2")
#####Preprocessing
aseg = normalize(aseg)
useg = normalize(useg)
sseg = normalize(sseg)

print("ok3")
spectro(sseg[:,8],Fs)
#fdesign(aseg[:,4],Fs)
#xa,ya = preprocessing(aseg,Fs)
#xu,yu = preprocessing(useg,Fs)
#xs,ys = preprocessing(sseg,Fs)

#dualplt(xa[:,4],ya[:,4],Fs)
#fdesign(xs[:,5][1:3000],Fs)

#####Feature Exrtraction


#Model Representatino

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(512, activation=tf.nn.relu),
  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])

#Model Training

#Results
'''
Steps:

-import all the files data in a loop
-spectrogram
-ML model NN network for analysis
-display result
'''

#Data segmentation
