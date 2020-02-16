# -*- coding: utf-8 -*-
"""
kineticcross
Sun Feb  9 19:47:25 2020

these functions import electrical and XRF data from two types of files:
    csv file containing the lockin settings of each scan
    h5 file containing the XRF data of each scan
each sample object has data related to that sample
"""

import h5py
import pandas as pd
import numpy as np

class Sample():
    def __init__(self):
        self.scans = []; self.h5data = []; self.lockin = []; self.maps = []
        self.stack = {}
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
    def import_maps(self, eh_scaler, elements, norm_scaler, fit_access_key):
        # order of scaler channels in h5: '/MAPS/scalers'
        scaler_chs = ['SRCurrent', 'us_ic', 'ds_ic']
        # to find electrical map, set scaler index
        scaler_idx = scaler_chs.index(eh_scaler)
        # to find channel to normalize, set normalization index
        norm_idx = scaler_chs.index(norm_scaler)
        # set-up to find correct normalization scalers
        if fit_access_key == 'roi':
            fit_keys = ['/MAPS/XRF_roi', '/MAPS/XRF_roi_quant']
        elif fit_access_key == 'fit':  
            fit_keys = ['/MAPS/XRF_fits','/MAPS/XRF_fits_quant']
        # for each scan, convert and add electrical and element maps
        for h5, factor in zip(self.h5data, self.lockin):
            maps_for_scan = []
            # to find element, decode h5 element strings
            dcoded_chs = [ele_str.decode('utf-8') for ele_str in h5['/MAPS/channel_names']]
            electrical_map = h5['/MAPS/scalers'][scaler_idx]
            electrical_map = electrical_map * factor
            maps_for_scan.append(electrical_map)
            for element in elements:
                ele_idx = dcoded_chs.index(element)
                ele_map = h5[fit_keys[0]][ele_idx,:,:]
                nrmlize_map = h5['/MAPS/scalers'][norm_idx, :, :] 
                quant_map = h5[fit_keys[1]][norm_idx, 0, ele_idx]
                fit_map = ele_map / nrmlize_map / quant_map # --> fitted map
                maps_for_scan.append(fit_map)
            maps_ = np.array(maps_for_scan)
            self.maps.append(maps_)
            
            
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

# import maps:
# arg1: electrical scaler channel
# arg2: element maps to extract
# arg3: scaler channel to normalize elemental signal
# arg4: use 'fit' on fitted h5s, or 'roi' for unfitted h5s
elements = ['Cu', 'Cd_L', 'Te_L']
NBL32.import_maps('ds_ic', elements, 'us_ic', 'fit')
NBL33.import_maps('ds_ic', elements, 'us_ic', 'fit')
TS58A.import_maps('ds_ic', elements, 'us_ic', 'fit')
# "sample.maps" now exists: holds electrical and XRF for each scan
# each scan is accessed by index, e.g. "NBL32.maps[2]" --> scan 424
# to access a specific map of a given scan:
#   "NBL32.maps[2][0,:,:]" --> electrical map for scan 424
#   "NBL32.maps[2][1,:,:]" --> Cu map for scan 424

# clean up plotting functions... and learn how to import the class as a module