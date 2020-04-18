# -*- coding: utf-8 -*-
"""
this sample class was created for scans of sample FS3 2019_06_2IDD
because the scaler data was stored haphazardly at the beam
--> the XBIC data is found in one H5 file (fitted by T Walker)
and the XRF data is found in another h5 file (fitted by B Lai)

-the XBIC data from TW and XRF data from XRF
were exported independently using MAPS
-"merge FS3 data.py" was used to merge these csvs into one file
for each scan; the intention: avoid importing scans from
separate directories

"""

import numpy as np
import pandas as pd
import xraylib as xl

def get_lockin(scan, data_path):
    data = pd.read_csv(data_path)
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
    return scaler_factor

class Sample():
    def __init__(self):
        self.scans = []; self.scans=[]; self.maps = [];
    def import_maps(self, path_ascii, path_lockin, CH):
        # store scan data
        for scan in self.scans:
            scan_str = str(scan)
            # define ascii of scan
            file = path_ascii + '/combined_ASCII_2idd_0'+scan_str+'.h5.csv'
            # import ascii as dataframe
            data = pd.read_csv(file)
            # dataframe keys used for shaping into map
            i = 'y pixel no'; j='x pixel no'
            # extract maps of interest; shape according to pixel no
            data_shape = [data.pivot(index=i, columns=j, values=c) for c in CH]
            # convert dataframes to numpy arrays
            data_arr = [df.to_numpy() for df in data_shape]
            # prepare electrical map for cts to ampere
            electrical_map = data_arr[0]
            # get electrical factor for xbic
            factor = get_lockin(scan, path_lockin)
            # convert electrical: cts to ampere
            data_arr[0] = electrical_map*factor
            # stack numpy arrays (into 3D)
            data_stack = np.array(data_arr)
            # store stacked numpy arrays
            name = 'scan' + scan_str
            setattr(self, name, data_stack) # useful for plotting & reference
            self.maps.append(data_stack) #useful w/ code before 20200402
    
    def ug_to_mol(self, elements):
        XRF_maps = [scan[-1:,:,:-2] for scan in self.maps]
        z_list = [xl.SymbolToAtomicNumber(e) for e in elements]
        factors = [(1/1E6) * (1/xl.AtomicWeight(z)) for z in z_list]
        XRF_mol = [factors[:, None, None] * XRF_map for XRF_map in XRF_maps]
        setattr(self.maps, 'mol', XRF_mol)
        return
    
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