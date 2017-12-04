from DataSample import DataSample,EdfAnnotation
import os
import matplotlib.pyplot as plt
import numpy as np 

def extract_channel(edf_object,channel_number):
    return {'channel_name':edf_object.header['label'][channel_number]
,'array':edf_object.converted[channel_number]
,'bytes':edf_object.header['number_samples'][channel_number]}

subjects = ['s01_2012_02_09/00000068_s01_a00.edf'
,'s02_2010_11_16/00000088_s02_a00.edf']
subject = subjects[0]

ds = DataSample('00000068','s01_2012_02_09','00000068_s01_a00.edf')
annot = ds.Annotations

lines_x=[]
lines_colors=[]
for item in annot.annotations:
    lines_x.append([int(item['start_time']*250),int(item['start_time']*250)])
    if item['seizure'] == 'bckg':
        lines_colors.append('green')
    else:
        lines_colors.append('red')

first_eeg = extract_channel(ds.EdfObject,0)
second_eeg = extract_channel(ds.EdfObject,1)

plt.figure(1)

plt.subplot(2,1,1)
plt.title(first_eeg['channel_name'])
plt.axis([0,len(first_eeg['array']),-200,200])
plt.plot(first_eeg['array'])

plt.subplot(2,1,2)
plt.title(second_eeg['channel_name'])
plt.axis([0,len(second_eeg['array']),-200,200])
plt.plot(second_eeg['array'])

for i,line in enumerate(lines_x):
    plt.plot(line, [-200, 200], color=lines_colors[i], linestyle='-', lw=3)

plt.show()
  

