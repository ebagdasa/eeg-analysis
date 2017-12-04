from pyedf import EDFObject
import os
import matplotlib.pyplot as plt
import numpy as np 

def extract_channel(edf_object,channel_number,seconds=1):
    return {'channel_name':edf_object.header['label'][channel_number],'array':np.concatenate([edf_object.converted[i][channel_number] for i in range(1)])}

subjects = ['data/TUH/train//01_tcp_ar/00000068/s01_2012_02_09/00000068_s01_a00.edf','data/TUH/train/01_tcp_ar/00000088/s02_2010_11_16/00000088_s02_a00.edf']
subject = subjects[0]

with open(subject,'rb') as f:
    edf = EDFObject(f)

    first_eeg = extract_channel(edf,0)
    second_eeg = extract_channel(edf,1)

    plt.figure(1)
    plt.subplot(2,1,1)
    plt.title(first_eeg['channel_name'])
    plt.plot(first_eeg['array'])
    plt.subplot(2,1,2)
    plt.title(second_eeg['channel_name'])
    plt.plot(second_eeg['array'])
    plt.show()
  

