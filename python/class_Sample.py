# -*- coding: utf-8 -*-
"""
kineticcross
Sun Feb 16 09:50:23 2020

two files are needed for this class:
the data file (h5) containing XRF data of a desired scan
the data file (csv) containing electrical settings for all scans

can only import data from Sector 2 (for now)
"""

import h5py
import numpy as np
import pandas as pd

# =============================================================================
# # tree for IndexError exceptions:
# # object:baseexception:exception:lookuperror:indexerror
# =============================================================================

class Sample():
    def __init__(self):
        self.scans = []; self.h5data = []; self.lockin = []; self.maps = []
        self.stack = {}; self.maps_ = []
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
        for h5, factor, scannum in zip(self.h5data, self.lockin, self.scans):
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
            maps_to_array = np.array(maps_for_scan)
            name = 'scan' + str(scannum)
            setattr(self, name, maps_to_array) # useful for plotting & reference
            self.maps.append(maps_to_array) #useful w/ code before 20200402
    def apply_iios(self, user_scans, iios_array):    
        # find scan indexes
        scan_idxs = [i for i, s in enumerate(self.scans) if s in user_scans]
        for scan_idx in scan_idxs:
            scan_raw_maps = self.maps[scan_idx]
            correct_maps = scan_raw_maps.copy() # create copy to overwrite
            for ele_idx, iio in enumerate(iios_array):
                ele_idx = ele_idx+1 # skip electrical map
                # extract XRF map
                map_to_correct = scan_raw_maps[ele_idx,:,:]
                # correct XRF map
                correct_map = map_to_correct / iio
                # replace XRF map
                correct_maps[ele_idx,:,:] = correct_map
            self.maps_.append(correct_maps)