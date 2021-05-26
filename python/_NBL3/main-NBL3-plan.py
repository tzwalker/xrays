# -*- coding: utf-8 -*-
"""
kineticcross
Sun Feb  9 19:47:25 2020

these functions import electrical and XRF data from two types of files:
    csv file containing the lockin settings of each scan
    h5 file containing the XRF data of each scan
each sample object has data related to that sample

workflow for XBIC v XBIV alignment and correlations
    "main-NBL3-plan" --> "XBIC-XBIV-translate-and-deltas.py" --> 
    "XBIC-XBIV-scatter-hex-fit.py"
workflow for grain core v boundary analyses:
    "main-NBL3-plan" --> "masked-data-save-arrays-to-csv.py" --> 
    "masked-data-construct-violin-df.py"
    
note that the Sample class (classh5_Sample.py) for these samples was changed
at line 75
this is done to avoid the
quantification units of ug/cm2; the quantification doesn't mean anything
because of the vanishing transmittance of Cu, te, and Cd XRF in these layers'
"""

from classh5_Sample import Sample
#from absorb_correct import get_iios

path = 1
if path == 0:
    data_path =  r'C:\Users\Trumann\data_NBL3\all_H5s'
elif path == 1:
    data_path = r'C:\Users\triton\NBL3_data\plan_view'
elif path == 2:
    data_path = '/home/kineticcross/Desktop/data'
    
# create sample objects
NBL31 = Sample(); NBL32 = Sample(); NBL33 = Sample(); TS58A = Sample()

# define stack and scans of each sample
NBL31.stack = {'Mo':   [10.2, 500E-7], 
                 'ZnTe': [6.34, 375E-7], 
                 'Cu':   [8.96, 0.5E-7], 
                 'CdTe': [5.85, 10.85E-4], 
                 'CdS':  [4.82, 80E-7], 
                 'SnO2': [100E-7]}
NBL31.scans = [335,336,337, 338,339,340, 341,342,343,344, 517,519]

NBL32.stack = {'Mo':   [10.2, 500E-7], 
                 'ZnTe': [6.34, 375E-7], 
                 'Cu':   [8.96, 2.5E-7], 
                 'CdTe': [5.85, 10.85E-4], 
                 'CdS':  [4.82, 80E-7], 
                 'SnO2': [100E-7]}
NBL32.scans =  [416,417,418, 419,420,421, 422,423,424,426, 538,550,575,551]

NBL33.stack = {'Mo':   [10.2, 500E-7], 
                 'ZnTe': [6.34, 375E-7], 
                 'Cu':   [8.96, 10E-7], 
                 'CdTe': [5.85, 10.85E-4], 
                 'CdS':  [4.82, 80E-7], 
                 'SnO2': [100E-7]}
NBL33.scans =  [258,259,260, 261,262,263, 264,265,266,267,  491,472,475]

TS58A.stack = {'Mo':   [10.2, 500E-7], 
                 'ZnTe': [6.34, 375E-7], 
                 'Cu':   [8.96, 2.5E-7], 
                 'CdTe': [5.85, 10.85E-4], 
                 'CdS':  [4.82, 80E-7], 
                 'SnO2': [100E-7]}
TS58A.scans =  [378,379,380, 382,383,384, 385,386,387,388, 439,408,427,440]

# import h5 data for each sample
NBL31.import_scan_data(data_path)
NBL32.import_scan_data(data_path)
NBL33.import_scan_data(data_path)
TS58A.import_scan_data(data_path)
# "sample.h5data" now exists: holds h5 files

# calc factor (cts-->ampere) for XBIC channel in each h5
NBL31.get_lockin(data_path+'/a_class_electrical.csv')
NBL32.get_lockin(data_path+'/a_class_electrical.csv')
NBL33.get_lockin(data_path+'/a_class_electrical.csv')
TS58A.get_lockin(data_path+'/a_class_electrical.csv')
# "sample.lockin" now exists: holds scaler factors

# import maps:
# arg1: electrical scaler channel
# arg2: element maps to extract
# arg3: scaler channel to normalize elemental signal
# arg4: use 'fit' on fitted h5s, or 'roi' for unfitted h5s
elements = ['Cu', 'Cd_L', 'Te_L', 'Mo_L']
NBL31.import_maps('ds_ic', elements, 'us_ic', 'fit')
NBL32.import_maps('ds_ic', elements, 'us_ic', 'fit')
NBL33.import_maps('ds_ic', elements, 'us_ic', 'fit')
TS58A.import_maps('ds_ic', elements, 'us_ic', 'fit')
# "sample.maps" now exists: holds electrical and XRF for each scan
# each scan is accessed by index, e.g. "NBL32.maps[2]" --> scan 424
# to access a specific map of a given scan:
#   "NBL32.maps[2][0,:,:]" --> electrical map for scan 424
#   "NBL32.maps[2][1,:,:]" --> Cu map for scan 424

# =============================================================================
# # enter beamtime settings
# # in apply_iios():
# # arg3: sample stack
# # arg4: layer at which to cease correction
# 
# beam_settings = {'beam_energy': 12.7, 'beam_theta':75, 'detect_theta':15}
# ### NBL32 ###
# iios2019 = get_iios(beam_settings, elements, NBL32.stack, end_layer='CdTe')
# scans_for_correction = [422,423,424, 419,420,421]
# #NBL32.apply_iios(scans_for_correction, iios2019)
# ### NBL33 ###
# iios2019 = get_iios(beam_settings, elements, NBL33.stack, end_layer='CdTe')
# scans_for_correction = [261,262,263, 264,265,266]
# #NBL33.apply_iios(scans_for_correction, iios2019)
# ### TS58A ###
# iios2019 = get_iios(beam_settings, elements, TS58A.stack, end_layer='CdTe')
# scans_for_correction = [385,386,387, 382,383,384]
# #TS58A.apply_iios(scans_for_correction, iios2019)
# 
# beam_settings = {'beam_energy': 8.99, 'beam_theta':90, 'detect_theta':43}
# ### NBL32 ###
# iios2017 = get_iios(beam_settings, elements, NBL32.stack, end_layer='CdTe')
# scans_for_correction = [550,538,575,551]
# #NBL32.apply_iios(scans_for_correction, iios2017)
# ### NBL33 ###
# iios2017 = get_iios(beam_settings, elements, NBL33.stack, end_layer='CdTe')
# scans_for_correction = [472,475,491]
# #NBL33.apply_iios(scans_for_correction, iios2017)
# ### TS58A ###
# iios2017 = get_iios(beam_settings, elements, TS58A.stack, end_layer='CdTe')
# scans_for_correction = [439,427,408,440]
# #TS58A.apply_iios(scans_for_correction, iios2017)
# 
# # "sample.maps_" now exists: holds electrical and corrected XRF of select scans
# # scan accessed by index in "scans_for_correction", NOT original scan list
# # e.g. "NBL32.maps_[4]" --> scan 419, "NBL32.maps[4]" --> scan 538)
# =============================================================================


# =============================================================================
# import numpy as np
# import matplotlib.pyplot as plt
# # max-min stretch 
# def normalize(array):
#     data_norm = (array - array.min()) / (array.max() - array.min())
#     return data_norm
# 
# # save XBIC array for Fiji processing and main_xrf figure
# OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20200525 figures_rev3\main_xrf'
# FILE = r'\NBL3_scan341_XBIC.csv'
# arr = NBL31.scan341[0,:,:-2]
# arr = normalize(arr)
# np.savetxt(OUT_PATH+FILE,arr,delimiter=',')
# 
# OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20200525 figures_rev3\main_xrf'
# FILE = r'\NBL32_scan422_bksubXBIC.csv'
# arr = NBL32.scan422[0,:,:-2]
# arr = normalize(arr)
# np.savetxt(OUT_PATH+FILE,arr1,delimiter=',')
# 
# OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20200525 figures_rev3\main_xrf'
# FILE = r'\NBL33_scan264_XBIC.csv'
# arr = NBL33.scan264[0,:,:-2]
# arr = normalize(arr)
# np.savetxt(OUT_PATH+FILE,arr,delimiter=',')
# 
# OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20200525 figures_rev3\main_xrf'
# FILE = r'\TS58A_scan386_XBIC.csv'
# arr = TS58A.scan386[0,:,:-2]
# arr = normalize(arr)
# np.savetxt(OUT_PATH+FILE,arr,delimiter=',')
# =============================================================================
