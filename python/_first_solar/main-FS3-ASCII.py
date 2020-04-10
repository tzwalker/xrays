# -*- coding: utf-8 -*-
"""
tzwalker
Thu Apr  2 17:12:40 2020
coding: utf-8

BEGIN OPERANDO ANALYSES:
Sample FS3_3: 2019_06_2IDD
-abandoned h5 importing, the structure between the TW fit and BL fit
is far too different and not worth the time

--> use ASCII csvs for these data

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
from class_ascii_Sample import Sample

SYS_PATH = r'C:\Users\Trumann\Desktop\FS_data\FS3_2019_06_2IDD'
XRF_ASCII = SYS_PATH + r'\BL_fit_202002\output'
XBICV_ASCII = SYS_PATH + r'\TW_fit_201907\output'

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


