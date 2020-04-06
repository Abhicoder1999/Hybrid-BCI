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




def tm_segment (data,Fs):

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

def mk_segment (data,marker):
    temp = np.where(marker == 1)[0]
    ind1 = temp[1];
    ind2 = temp[len(temp)-2]
    win = len(marker)//12
    data = np.array(data)

    i1 = ind1//2-win
    i2 = ind1//2+win
    aseg = data[i1:i2,:]
    print(i1,i2)
    i1 = (ind1+ind2)//2-win
    i2 = (ind1+ind2)//2+win
    useg = data[i1:i2,:]
    print(i1,i2)
    i1 = (ind2+len(marker))//2-win
    i2 = (ind2+len(marker))//2+win
    sseg = data[i1:i2,:]
    print(i1,i2)
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

exp_list = [1,2,3,5,8,12,13,14,15,18,19,21,22,24,26,27,28,30]
channel_list = [2,3,6,7,10,11] 
#2-F3,3-FC5,6-O1,7-O2,10-FC6,11-F4
    #####Data Extraction

for exp_name in exp_list:
    print(exp_name)
    file = scipy.io.loadmat('../data/EEG_Data/eeg_record'+str(exp_name)+'.mat')
    mdata = file["o"]
    mtype = mdata.dtype
    ndata = {n: mdata[n][0,0] for n in mtype.names}

    Fs = ndata["sampFreq"][0][0]
    data_raw = ndata["data"]
    marker = ndata["marker"]
    plt.plot(marker)
    tmstamp = ndata["timestamp"]
    trials = ndata["trials"][0,:,:,:]
    plt.plot(marker)

    data = pd.DataFrame(data_raw)
    
    segments = tm_segment(data,tmstamp)
#    segments =  mk_segment(data,marker)

    aseg = np.array(segments[0])[: , channel_list]
    useg = np.array(segments[1])[: , channel_list]
    sseg = np.array(segments[2])[: , channel_list]


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
        #sdesign(xa[:,10],Fs)
            #dualplt(xa[:,4],ya[:,4],Fs)


            ######Storing

    store_spect(xa,Fs,'../spectro/active/exp'+str(exp_name))
    store_spect(xu,Fs,'../spectro/unattentive/exp'+str(exp_name))
    store_spect(xs,Fs,'../spectro/drowsy/exp'+str(exp_name))


    #image.imsave('../spectro/active/name2.png', Sa)
    #img_load = img.open('name2.png')
