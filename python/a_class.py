# -*- coding: utf-8 -*-
"""
kineticcross
Sun Feb  9 19:47:25 2020

each sample has a set of scans
each scan has an h5 and a set electrical settings
"""

import h5py
import pandas as pd



class Sample():
    def __init__(self):
        self.scans = []; self.h5data = []; self.lockin = []
        self.maps = []; self.stack = {}
    def import_scan_data(self, data_path):
        str_list = [str(scan_number) for scan_number in self.scans]
        filenames = [data_path+'/2idd_0'+scan+'.h5' for scan in str_list]
        self.h5data = [h5py.File(file, 'r') for file in filenames]
    def get_lockin(self, data_path):
        data = pd.read_csv(data_path)
        for scan in self.scans:
            # get lockin data for a specific scan
            # if 'index out of bounds error', check if scan in datafile
            settings = data.loc[data['scan']==scan]
            # check if scan is XBIC or XBIV
            bic_or_biv = settings['XBIC/V'].values[0]
            # then calc factor (cts-->ampere) for XBIC channel in h5
            if bic_or_biv == 'C':
                stanford = settings['stanford'].values[0]
                V2F = settings['V2F'].values[0]
                lockin = settings['lockin'].values[0]
                scaler_factor = (stanford*1E-9) / (V2F*lockin)
            elif bic_or_biv == 'V':
                V2F = settings['V2F'].values[0]
                lockin = settings['lockin'].values[0]
                scaler_factor = 1 / (V2F*lockin)
            self.lockin.append(scaler_factor)
    def import_maps(self, electrical_scaler, elements, ):
        scaler_chs = ['SRCurrent', 'us_ic', 'ds_ic']
        scaler_idx = scaler_chs.index(electrical_scaler)
        for h5, factor in zip(self.h5data, self.lockin):
            maps_for_scan = []
            electrical_map = h5['/MAPS/scalers'][scaler_idx]
            electrical_map = electrical_map * factor
            maps_for_scan.append(electrical_map)
            print('okay...')
            
            
data_path = '/home/kineticcross/Desktop/data'
# create sample objects
NBL32 = Sample(); NBL33 = Sample(); TS58A = Sample()

# define stack and scans of each sample
NBL32.stack = {'Mo':   [10.2, 500E-7], 
                 'ZnTe': [6.34, 375E-7], 
                 'Cu':   [8.96, 2.5E-7], 
                 'CdTe': [5.85, 10.85E-4], 
                 'CdS':  [4.82, 80E-7], 
                 'SnO2': [100E-7]}
NBL32.scans =  [422,423,424,550,538,575, 419,420,421,551]

NBL33.stack = {'Mo':   [10.2, 500E-7], 
                 'ZnTe': [6.34, 375E-7], 
                 'Cu':   [8.96, 10E-7], 
                 'CdTe': [5.85, 10.85E-4], 
                 'CdS':  [4.82, 80E-7], 
                 'SnO2': [100E-7]}
NBL33.scans =  [261,262,263,472, 264,265,266, 475,491]

TS58A.stack = {'Mo':   [10.2, 500E-7], 
                 'ZnTe': [6.34, 375E-7], 
                 'Cu':   [8.96, 2.5E-7], 
                 'CdTe': [5.85, 10.85E-4], 
                 'CdS':  [4.82, 80E-7], 
                 'SnO2': [100E-7]}
TS58A.scans =  [385,386,387, 439,427,408, 382,383,384, 440]

# import h5 data for each sample
NBL32.import_scan_data(data_path)
NBL33.import_scan_data(data_path)
TS58A.import_scan_data(data_path)
# "sample.h5data" now exists: holds h5 files

# calc factor (cts-->ampere) for XBIC channel in each h5
NBL32.get_lockin(data_path+'/a_class_electrical.csv')
NBL33.get_lockin(data_path+'/a_class_electrical.csv')
TS58A.get_lockin(data_path+'/a_class_electrical.csv')
# "sample.lockin" now exists: holds scaler factors
# these factors line up exactly with the file positions in "sample.h5data"

# import maps:
# arg1: electrical scaler channel
# arg2: element maps to extract
# arg3:  
NBL32.import_maps('ds_ic')
