import sys
sys.path.append('./TICC')
import TICC_solver as TICC
from DataSample import DataSample,EdfAnnotation
import os
import matplotlib.pyplot as plt
import numpy as np 
import time as time


def run():

    fname = prepare_edf_to_txt()
    t = time.time()
# do stuff
    (cluster_assignment, cluster_MRFs) = TICC.solve(window_size = 30,number_of_clusters = 2, lambda_parameter = 11e-2, beta = 600, maxIters = 100, threshold = 2e-5, write_out_file = False, input_file = fname, prefix_string = "output_folder/", num_proc=1)
    elapsed = time.time() - t

    print elapsed,cluster_assignment
    np.savetxt('Results.txt', cluster_assignment, fmt='%d', delimiter=',')
def extract_channel(edf_object,channel_number):
    return {'channel_name':edf_object.header['label'][channel_number]
,'array':edf_object.converted[channel_number]
,'bytes':edf_object.header['number_samples'][channel_number]}

def prepare_edf_to_txt():
    ds = DataSample('00000068','s01_2012_02_09','00000068_s01_a00.edf')
    return ds.save_to_file()



def show_plot(ds):
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
  

if __name__ == "__main__":
    run()
