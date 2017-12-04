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


class EDFObject:


    def __init__(self, fileobj):
        self.__file = fileobj
        self.header = self.read_header(self.__file)
        h = self.header
        # calculate ranges for rescaling
        self.dig_min = h['digital_min']
        self.phys_min = h['physical_min']
        phys_range = h['physical_max'] - h['physical_min']
        dig_range = h['digital_max'] - h['digital_min']
        assert np.all(phys_range > 0)
        assert np.all(dig_range > 0)

        self.gain = phys_range / dig_range

        self.raw=self.read_raw_records(self.__file)

        self.converted = self.convert_records_to_phys(self.raw)



    def read_header(self,file_obj):
        data = file_obj.read(256)
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

        data = file_obj.read(header['header_bytes']-256)

        all_headers = []
        records = []
        for i in range(header['num_signals']):
            records.append([])

        offsets_edf=[{'name':'label','offset':16,'type':np.dtype(np.str)}
        ,{'name':'transducer','offset':80,'type':np.dtype(np.str)}
        ,{'name':'physical_dimension','offset':8,'type':np.dtype(np.str)}
        ,{'name':'physical_min','offset':8,'type':np.dtype(np.float)},
        {'name':'physical_max','offset':8,'type':np.dtype(np.float)},
        {'name':'digital_min','offset':8,'type':np.dtype(np.int)},
        {'name':'digital_max','offset':8,'type':np.dtype(np.int)},
        {'name':'prefiltering','offset':80,'type':np.dtype(np.str)},
        {'name':'number_samples','offset':8,'type':np.dtype(np.int)}]
        
        
        rec_pos = 0

        for counter,item in enumerate(offsets_edf):
            temp_array = []
            for ns in range(0,header['num_signals']):
                temp_array.append(data[rec_pos:rec_pos+item['offset']].strip())
                rec_pos += item['offset']
            header[item['name']] = np.array(temp_array,dtype=item['type'])  

        assert (self.__file.tell()==header['header_bytes']),"End of header unexpected"
        return header

    def read_raw_records(self,file_obj):
        data = file_obj.read()

        rec_pos = 0
        
        records=[]
        #offset reserved space to data records
        rec_pos += 32*self.header['num_signals']
        for record_index in range(self.header['num_items']):
            record=[]
            for i,num_samples in enumerate(self.header['number_samples']):
                ints = np.fromstring(data[rec_pos:rec_pos + 2*num_samples], dtype=np.dtype(np.int16))
                rec_pos +=2*num_samples
                record.append(ints)
            records.append(record)

        return records

    def convert_records_to_phys(self,raw_records):
        signals =[]
        for (i, record_samples) in enumerate(raw_records):
            signal=[]
            for j,sample in enumerate(record_samples):
                dig = sample.astype(np.float32)
                phys = (dig - self.dig_min[j]) * self.gain[j] + self.phys_min[j]
                signal.append(phys)
            signals.append(signal)

        return signals