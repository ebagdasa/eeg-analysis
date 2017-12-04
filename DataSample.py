import pyedf
import os
import re
import json
from pyedf import EDFObject

class DataSample:

    def __init__(self,PatientId,Session,FileName):
        with open('config.json','r') as target:
            j=json.load(target)
            self.DATA_DIR=j["DATA_DIR"]
            self.PHASE=j["PHASE"]
            self.EEG_RECORD_TYPE=j["EEG_RECORD_TYPE"]
            self.FULL_DATA_PATH=os.path.join(self.DATA_DIR,self.PHASE,self.EEG_RECORD_TYPE)
        
        with open(os.path.join(self.FULL_DATA_PATH,PatientId,Session,FileName),'rb') as f:
            self.EdfObject = EDFObject(f)
        self.Annotations = EdfAnnotation(os.path.join(self.FULL_DATA_PATH,PatientId,Session), FileName)

class EdfAnnotation:
    #Time-synchronous event (TSE) files use a simple format that looks like this:
    #  0.0000 490.0000 bckg 1.0000
    #
    # Label files (LBL) are more complicated and essentially describe a graph
    # that can represent a hierarchical annotation (e.g., FNSZ and GNSZ map to
    # SEIZ). They contain the start and stop times, a channel index, a level
    # index and probabilities for each class or symbol.

    __re_ann = re.compile('([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) (\S+) ([0-9]*\.?[0-9]*)')

    __types=('TSE','TSE_BI','LBL','LBL_BI')

    annotations = []

    def __init__(self,Path ,EdfName,Type='TSE_BI'):
        self.__edf_name = os.path.splitext(EdfName)[0]
        
        assert Type in self.__types,"Uknown type"
        
        if Type == 'TSE_BI':
            self.__edf_name=self.__edf_name+'.tse_bi'
        if Type == 'TSE':
            self.__edf_name=self.__edf_name+'.tse'
        if Type == 'LBL':
            self.__edf_name=self.__edf_name+'.lbl'
        if Type == 'LBL_BI':
            self.__edf_name=self.__edf_name+'.lbl_bi'

        with open(os.path.join(Path,self.__edf_name),'r') as f:
            for line in f:
                annotation_line_match = self.__re_ann.match(line)
                if annotation_line_match:
                    start_time = annotation_line_match.group(1)
                    end_time = annotation_line_match.group(2)
                    seizure =  annotation_line_match.group(3)
                    propability =  annotation_line_match.group(4)
                    annotation = {'start_time':float(start_time)
                    , 'end_time':float(end_time), 'seizure':seizure
                    , 'propability':float(propability)}
                    self.annotations.append(annotation)
        
        assert len(self.annotations) > 0,"Attentions not loaded"

