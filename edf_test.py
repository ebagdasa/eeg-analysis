from pyedf import read_edf_file
import os

subject = 'data/s01_2013_03_04/00000032_s01_a00.edf'
with open(subject,'rb') as f:
    edf = read_edf_file(f,os.path.getsize(subject))
    print edf['headers']
    print edf['records']

