# -*- coding: utf-8 -*-
"""
tzwalker
Thu Apr  2 17:12:40 2020
coding: utf-8

BEGIN OPERANDO ANALYSES:
Sample FS3_3: 2019_06_2IDD

XBIC
20C: scan0323
40C: scan0327
60C: scan0332
80C: scan0344
100C: scan344

XBIV
20C: scan0321
40C: scan0325
60C: scan0330
80C: scan0337
100C: scan0342

"""

#from class_FS3Sample import Sample
#import class_absorb_correct as XRFcorr

# -*- coding: utf-8 -*-
"""
this sample class was created for scans of sample FS3 2019_06_2IDD
because the scaler data was stored haphazardly at the beam
--> the XBIC data is found in one H5 file (fitted by T Walker)
and the XRF data is found in another h5 file (fitted by B Lai)

the class does not store the h5 data because two of each h5 would
take too much memory space;
instead, each h5 is treated separately, 
and the pertinent data is extracted:
    XBIC from an H5 file in one path
    merge with XRF from H5 in different path
here h5s and the lockin data are NOT stored as an atribute of the class
and are erased from memory once the program imports the maps of each scan 
"""

import h5py
import numpy as np
import pandas as pd

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
        self.scans = []; self.maps = []
        self.stack = {}; self.maps_ = []

    def import_maps(self, path_xbic, eh_scaler, lockin_file, path_xrf, elements, xrfnorm_scaler, fit_access_key):
        # order of scaler channels in OLD h5: '/MAPS/scalers' TW_fit
        scaler_chs = ['SRCurrent', 'us_ic', 'ds_ic']
        # to find electrical map, set scaler index
        scaler_idx = scaler_chs.index(eh_scaler)
        # store scan data
        maps_for_scan = []
        for scan in self.scans:
            scan_str = str(scan)
            # get electrical factor for xbic h5
            factor = get_lockin(scan, lockin_file)
            # get electrical map
            xbic_fname = path_xbic+'/2idd_0'+scan_str+'.h5'
            xbic_h5 = h5py.File(xbic_fname, 'r')
            electrical_map = xbic_h5['/MAPS/scalers'][scaler_idx]
            # apply scale factor
            electrical_map = electrical_map * factor
            maps_for_scan.append(electrical_map)
            
            # setup XRF import
            # order of scaler channels in NEW h5: '/MAPS/scalers' BL_fit
            scaler_chs = ['ds_ic', 'SRCurrent', 'us_ic']
            xrf_fname = path_xrf+'/2idd_0'+scan_str+'.h5'
            xrf_h5 = h5py.File(xrf_fname, 'r')
            # normalize xrf according to this channel, set normalization index
            norm_idx = scaler_chs.index(xrfnorm_scaler)
            # set-up to find correct normalization scalers
            if fit_access_key == 'roi':
                fit_keys = ['/MAPS/XRF_roi', '/MAPS/XRF_roi_quant']
            elif fit_access_key == 'fit':  
                fit_keys = ['/MAPS/XRF_fits','/MAPS/XRF_fits_quant']
            # to find element, decode h5 element strings
            dcoded_chs = [ele_str.decode('utf-8') for ele_str in xrf_h5['/MAPS/channel_names']]
            for element in elements:
                ele_idx = dcoded_chs.index(element)
                ele_map = xrf_h5[fit_keys[0]][ele_idx,:,:]
                nrmlize_map = xrf_h5['/MAPS/scalers'][norm_idx, :, :] 
                quant_map = xrf_h5[fit_keys[1]][norm_idx, 0, ele_idx]
                fit_map = ele_map / nrmlize_map / quant_map # --> fitted map
                maps_for_scan.append(fit_map)
            maps_to_array = np.array(maps_for_scan)
            name = 'scan' + scan_str
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



path = 1
if path == 0:
    PATH_XBIC =  r'C:\Users\Trumann\FS3_2019_06_2IDD_stage\TW_fit_201906'
    PATH_XRF = r'C:\Users\Trumann\FS3_2019_06_2IDD_stage\BL_fit_202002'
    PATH_LOCKIN = r'C:\Users\Trumann\xrays\python\_first_solar'
elif path == 1:
    PATH_XBIC =  r'C:\Users\triton\FS_operando\TW_fit_201907'
    PATH_XRF = r'C:\Users\triton\FS_operando\BL_fit_202002'
    PATH_LOCKIN = r'C:\Users\triton\FS_operando'
elif path == 2:
    data_path = '/home/kineticcross/Desktop/data'
    
# create sample objects
FS3 = Sample()

# define stack and scans of each sample
FS3.stack = {'Au':   [19.3, 100E-7], 
                 'CdTe': [5.85, 5E-4],
                 'Se_grad': [4.82, 500E-7],
                 'SnO2': [100E-7]}
FS3.scans = [321,322,323,324,325,326,327,328,329,330,331,332,333,
             337,338,339,340,341,342,343, 344, 345]


# import h5 data for each sample
# think about splitting the XBIC import and the XRF import
lockin_file = PATH_LOCKIN+r'\a_class_electrical.csv'
elements = ['Se', 'Cd_L', 'Te_L', 'Au_L']

FS3.import_maps(PATH_XBIC, 'us_ic', lockin_file, PATH_XRF, elements, 'us_ic', 'fit')
# "sample.eh_maps" now exists: destined to merge with xrf maps

# =============================================================================
# 
# # calc factor (cts-->ampere) for XBIC channel in each h5
# FS3.get_lockin(data_path+'/a_class_electrical.csv')
# # "sample.lockin" now exists: holds scaler factors
# 
# # import maps:
# # arg1: electrical scaler channel
# # arg2: element maps to extract
# # arg3: scaler channel to normalize elemental signal
# # arg4: use 'fit' on fitted h5s, or 'roi' for unfitted h5s
# elements = ['Se', 'Cd_L', 'Te_L', 'Cu']
# FS3.import_maps('us_ic', elements, 'us_ic', 'fit')
# # "sample.maps" now exists: holds electrical and XRF for each scan
# # each scan can be accessed by index, e.g. 
# #   "NBL32.maps[2]" --> scan 424
# #   "NBL32.maps[2][0,:,:]" --> electrical map for scan 424
# #   "NBL32.maps[2][1,:,:]" --> Cu map for scan 424
# # OR by scan number, e.g. "NBL32.scan424[0,:,:-2]" --> electrical map for 424
# 
# # enter beamtime settings
# # in apply_iios():
# # arg3: sample stack
# # arg4: layer at which to cease correction
# 
# beam_settings = {'beam_energy': 12.7, 'beam_theta':75, 'detect_theta':15}
# 
# FS3iios = XRFcorr.get_iios(beam_settings, elements, FS3.stack, end_layer='Se_grad')
# scans_for_correction = FS3.scans
# FS3.apply_iios(scans_for_correction, FS3iios)
# 
# # i need to modify the apply_iios definition in Sample() class
# # in order to handle an Se gradient
# 
# # "sample.maps_" now exists: holds electrical and corrected XRF of select scans
# # scan accessed by index in "scans_for_correction", NOT original scan list
# # e.g. "NBL32.maps_[4]" --> scan 419, "NBL32.maps[4]" --> scan 538)
# =============================================================================


