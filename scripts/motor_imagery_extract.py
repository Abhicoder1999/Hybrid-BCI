# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 01:34:26 2020

@author: abhijeet
"""

import pandas as pd
import scipy.io
import numpy as np

def extract_data(efile,dfile,eno,tfile):
    '''
    efile = events type list
    dfile = data file of all channels
    eno = event number
    tfile = appending target file with data
    '''
    index=[]
    duration=[]
    for i in range(len(efile)):  
        if(int(efile[i][0]) == eno):
            index.append(int(efile[i][1]))
            duration.append(int(efile[i][2]))
     
    for i in range(len(index)):
        if len(tfile) == 0:
            tfile = np.array(dfile[0:3,index[i]:index[i]+duration[i]])
        else:
            temp = np.array(dfile[0:3,index[i]:index[i]+duration[i]])
            tfile = np.vstack((tfile,temp)) #dynamically appending array

    return tfile


ldata = []
rdata = []
exp_name = [11,12,21,22,31,32,41,42,51,52,61,62,71,72,81,82,91,92];
for i in range(len(exp_name)):
#Intialising Variables
    print(exp_name[i])
    mat = scipy.io.loadmat('../data/MI_data/EEG'+str(exp_name[i])+'.mat')
    data = np.array(mat['EEG']['data'][0][0])
    time=np.array(mat['EEG']['times'][0][0])
    events = mat['EEG']['event'][0][0][0]
    df_events = pd.DataFrame(mat['EEG']['event'][0][0][0])

    ldata = extract_data(events,data,769,ldata)
    rdata = extract_data(events,data,770,rdata)
    print(ldata.shape,rdata.shape)


#Storing the extracted data in local
np.savetxt('../data/csv_file/ldata.csv',ldata,delimiter=',')
np.savetxt('../data/csv_file/rdata.csv',rdata,delimiter=',')