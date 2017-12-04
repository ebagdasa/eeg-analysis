#!/usr/bin/env python
# encoding: utf-8
"""
pyedf.py
Created by Ray Slakinski on 2010-09-14.
Copyright (c) 2010 Ray Slakinski. All rights reserved.
"""
import sys
import argparse
import re
import struct
import numpy as np

def read_edf_file(fileobj,filesize):
    data = fileobj.read()
    header = {}
    # Parse header information based on the EDF/EDF+ specs
    # http://www.edfplus.info/specs/index.html
    header['version'] = data[0:7].strip()
    header['patient_id'] = data[7:88].strip()
    header['rec_id'] = data[88:168].strip()
    header['startdate'] = data[168:176].strip()
    header['starttime'] = data[176:184].strip()
    header['header_bytes'] = int(data[184:192].strip())
    header['num_items'] = int(data[236:244].strip())
    header['data_duration'] = float(data[244:252].strip())
    header['num_signals'] = int(data[252:256].strip())
    # more data 256 chars down. in header, but ignoring for now


    all_headers = [[],[],[],[],[],[],[],[],[]]
    records = []
    for i in range(header['num_signals']):
        records.append([])

    offsets_edf=[16,80,8,8,8,8,8,80,8]
    
    assert(len(all_headers) == len(offsets_edf))
    
    rec_pos = 256

    for counter,offset in enumerate(offsets_edf):
        for ns in range(0,header['num_signals']):
            all_headers[counter].append(data[rec_pos:rec_pos+offset].strip())
            rec_pos += offset
    
    #offset reserved space to data records
    rec_pos += 32*header['num_signals']
    dt = np.dtype(int)
    dt = dt.newbyteorder('<')
    for i,num_samples in enumerate(all_headers[len(all_headers)-1]):
        ints = np.frombuffer(data[rec_pos:rec_pos +2*int(all_headers[len(all_headers)-1][i])], dtype=np.dtype(np.int16))
        rec_pos +=2*int(all_headers[len(all_headers)-1][i])
        records[i].append(ints)

    return {'header': header, 'headers': all_headers,'records':records}