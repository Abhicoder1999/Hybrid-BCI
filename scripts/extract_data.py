import numpy as np
import pandas as pd
import scipy.io
from matplotlib import pyplot as plt
from matplotlib import image
from scipy.fftpack import fft
from scipy.signal import butter
from scipy.signal import sosfilt
from scipy.signal import spectrogram
from scipy.ndimage import gaussian_filter
from PIL import Image as img
import os




def segment (data,Fs):

    data["time"] = tmstamp[:,4]
    l = data.shape[0]
    tmax = data["time"][l-1]
    tmin = data["time"][0]
    if tmax < tmin:
        tmax = tmax + 60
        temp1 = data["time"] >= 0
        temp2 = data["time"] < tmin        
        temp = temp1 & temp2
        temp = temp*60
        data["time"] += temp
    
    k = (tmax-tmin)/3
    t1 = k + tmin
    t2 = 2*k + tmin
    wlen = k//1.5;

    aseg = data[(data["time"]>=tmin+wlen/2.0) & (data["time"]<=t1-wlen/2.0)]
    useg = data[(data["time"]>t1+wlen/2.0) & (data["time"]<=t2-wlen/2.0)]
    sseg = data[(data["time"]>t2+wlen/2.0)&(data["time"]<=tmax-wlen/2.0)]
  
    return aseg,useg,sseg;

def preprocessing(data,Fs):
    N,nch = data.shape
    xfil = np.zeros((N,nch))
    yfil = np.zeros((N,nch))
    fpass = [2*0.5/Fs,2*30.0/Fs]#from 0.5 to 30hz bpf
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
    return Sxx[0:513//3,:] # only till 20hz matters

def sdesign(tdata,Fs):
    f, t, Sxx = spectrogram(tdata, Fs,nfft = 1024,nperseg = 300)
    Sxx = gaussian_filter(Sxx, sigma=2)
    #add opening closing for more prominent effect
    plt.pcolormesh(t,f[0:513//3], Sxx[0:513//3,:])
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()


def ICA():
    pass

def store_spect(x,Fs,filename):
    for i in range(x.shape[1]):    
        s = spectro(x[:,i],Fs)
        image.imsave(filename +'ch'+ str(i) + '.png', s)
    pass
    
    

    #####Data Extraction
file = scipy.io.loadmat('../data/EEG_Data/eeg_record3.mat')
mdata = file["o"]
mtype = mdata.dtype
ndata = {n: mdata[n][0,0] for n in mtype.names}

Fs = ndata["sampFreq"][0][0]
data_raw = ndata["data"]
marker = ndata["marker"]
plt.plot(marker)
tmstamp = ndata["timestamp"]
trials = ndata["trials"][0,:,:,:]



data = pd.DataFrame(data_raw)

segments = segment(data,tmstamp)
    
data = np.array(data)
aseg = np.array(segments[0].iloc[:, 3:17])
useg = np.array(segments[1].iloc[: , 3:17])
sseg = np.array(segments[2].iloc[: , 3:17])


    #####Preprocessing
aseg = normalize(aseg)
useg = normalize(useg)
sseg = normalize(sseg)

    #fdesign(sseg[:,2],Fs)

xa,ya = preprocessing(aseg,Fs)
xu,yu = preprocessing(useg,Fs)
xs,ys = preprocessing(sseg,Fs)


    #####Feature Exrtraction
    #Sa = spectro(xa[:,0],Fs)
    #sdesign(xu[:,10],Fs)
    #dualplt(xa[:,4],ya[:,4],Fs)


    ######Storing

store_spect(xa,Fs,'../spectro/active/exp3')
store_spect(xu,Fs,'../spectro/unattentive/exp3')
store_spect(xs,Fs,'../spectro/drowsy/exp3')


#image.imsave('../spectro/active/name2.png', Sa)
#img_load = img.open('name2.png')




#Model Representatino


#Model Training

#Results
'''
Steps:

-import all the files data in a loop
-spectrogram
- then acording to division put those in different files
-ML model NN network for analysis
-display result
'''

#Data segmentation
