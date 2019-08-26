import numpy as np
import pandas as pd
import scipy.io
from matplotlib import pyplot as plt
from scipy.fftpack import fft
from scipy.signal import butter
from scipy.signal import sosfilt

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
    data = data - data.mean(axis=0)
    data = data / (np.abs(data).max(axis = 0)-np.abs(data).min(axis = 0))
    N,nch = data.shape
    xfil = np.zeros((N,nch))
    yfil = np.zeros((N,nch))
    for i in range(nch):
            tdata = data[:,i]
            sos = butter(10, 0.35, 'lowpass', output='sos')
            tdata_ = sosfilt(sos, tdata)
            fdata_ = np.abs(fft(tdata_))         
            xfil[:,i] = tdata_
            yfil[:,i] = fdata_
    return xfil,yfil
    
def fdesign(tdata,Fs):
    fdata = fft(tdata)
    T = np.divide(1,Fs)    
    N = len(tdata)
    l = np.linspace(0.0, 1.0/(2.0*T), N//2)
    nfdata =  2.0/N * np.abs(fdata[0:N//2])
    
    sos = butter(10, 0.35, 'lowpass', output='sos')
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
    N = len(tdata)
    l = np.linspace(0.0, 1.0/(2.0*T), N//2)
    nfdata =  2.0/N * np.abs(fdata[0:N//2])
    plt.subplot(2,1,1)
    plt.plot(tdata,'r')
    plt.subplot(2,1,2)
    plt.plot(l,nfdata,'r')
    

def spectrum (segments):
    pass    


#Data Extraction
file = scipy.io.loadmat('../data/EEG_Data/eeg_record1.mat')
mdata = file["o"]
mtype = mdata.dtype
ndata = {n: mdata[n][0,0] for n in mtype.names}

Fs = ndata["sampFreq"][0][0]
data_raw = ndata["data"]
marker = ndata["marker"]
tmstamp = ndata["timestamp"]
trials = ndata["trials"][0,:,:,:]


data = pd.DataFrame(data_raw)
segments = segment(data,tmstamp)
aseg = np.array(segments[0].iloc[0:50000 , 3:17])
useg = np.array(segments[1].iloc[0:50000 , 3:17])
sseg = np.array(segments[2].iloc[0:50000 , 3:17])


#Preprocessing

x1,y1 = preprocessing(aseg,Fs)

dualplt(x1[:,4][1:1000],y1[:,4][1:1000],Fs)
#ploting(useg[:,4])

#Feature Exrtraction

#Model Representatino

#Model Training

#Results
'''
Steps:

-import all the files data in a loop
-5 division of the component frequency depending upon region
-add time kurtosis of the signal
-ML model NN network for analysis
-display result
'''

#Data segmentation
