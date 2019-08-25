import numpy as np
import pandas as pd
import scipy.io


def segment (data,Fs):
    l = data.shape[0]
    t_total = l/(Fs*60.0)
    ti
    data = data
    win_l = 6;#reading time interval for each segment
    t_seg = np.array([t_total/6.0 -win_l/2.0,t_total/6 +win_l/2.0,
                  t_total/2.0-win_l/2.0,t_total/2.0+win_l/2.0,
                  5*t_total/6.0-win_l/2.0,5*t_total/6.0+win_l/2.0])               
    return t;

file = scipy.io.loadmat('../data/EEG_Data/eeg_record1.mat')
#print(file.keys())
#mdata = pd.DataFrame.from_dict(file["o"][0,:])
#marker = pd.DataFrame.from_dict(file["o"]["marker"][0,0])
#tag = pd.DataFrame.from_dict(file["o"]["tag"][0,0])
#data = pd.DataFrame.from_dict(file["o"]["data"][0,0])
#timestamp = data = pd.DataFrame.from_dict(file["o"]["timestamp"][0,0])


mdata = file["o"]
mtype = mdata.dtype
ndata = {n: mdata[n][0,0] for n in mtype.names}

Fs = ndata["sampFreq"][0][0]
data_raw = ndata["data"]
marker = ndata["marker"]
tmstamp = ndata["timestamp"]
trials = ndata["trials"][0,:,:,:]
data = pd.DataFrame(data_raw)
t = segment(data,Fs)

'''
Steps:
-import all the files data in a loop
-divide data to 3segments of 8 mins as 128Fs 
-find eachs frequency response
-5 division of the component frequency depending upon region
-add time kurtosis of the signal
-ML model NN network for analysis
-display result
'''

#Data segmentation
