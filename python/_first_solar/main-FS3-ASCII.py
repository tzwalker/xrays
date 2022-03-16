# -*- coding: utf-8 -*-
"""
tzwalker
Thu Apr  2 17:12:40 2020
coding: utf-8

BEGIN OPERANDO ANALYSES:
Sample FS3_3: 2019_06_2IDD
-abandoned h5 importing, the structure between the TW fit and BL fit
is far too different and not worth the time

instead the ASCIIs were exported from TW fit and BL fit and combined
    workflow:
        1. 'ASCII old-main.py'
        2. 'ASCII-merge.py'
        3. 'ASCII-reduce.py'

after (3), ASCIIS_TW_BL have the combined data
    'us_ic' is the relevant scaler for the electrical channel
    'US_IC' is the relevant scaler for the upstream ion chamber

the relevant scans are given below
    XBIC
    20C: scan0323
    40C: scan0327
    60C: scan0332
    80C: scan0339
    100C: scan344
    
    XBIV
    20C: scan0321
    40C: scan0325
    60C: scan0330
    80C: scan0337
    100C: scan0342
    [322,323,324,325,326,327,328,329,330,331,332,333,
                 337,338,339,340,341,342,343, 344, 345]

workflow to align XBIC and XBIV maps:
    1. 'main-FS3-ASCII'
    2. '...-translate-and-deltas'
    3. '...-translated analyses'

after (3), the aligned maps were saved as 2D csvs  in
    r'Dropbox (ASU)\2_FS_operando\XBIC aligned image csvs'
    and 'XBIC aligned image csvs'
for plotting reference, pixel step was 150nm --> 20pixels = 3um, 67pix = 10um

"""

from class_ascii_Sample import Sample
#ASCII_PATH = r'C:\Users\triton\FS3_2019_06_operando\ASCIIS_TW_BL\ug_per_cm2_XRF'
#PATH_LOCKIN = r'C:\Users\triton\FS3_2019_06_operando\ASCIIS_TW_BL\FS_plan_electrical.csv'
ASCII_PATH =  r'C:\Users\Trumann\FS3_2019_06_operando\ASCIIS_TW_BL' 
PATH_LOCKIN = r'C:\Users\Trumann\FS3_2019_06_operando\ASCIIS_TW_BL\FS_plan_electrical.csv'

# create sample objects
FS3 = Sample()

# define stack and scans of each sample, upstream layer first
FS3.stack = {'Au':   [19.3, 100E-7], 
                 'CdTe': [5.85, 5E-4],
                 'Se': [4.82, 100E-7],
                 'SnO2': [100E-7]}
FS3.scans = [323,327,332,339,344] #XBIC: [323,327,332,339,344] #XBIV: [321,325,330,337,342]


# channels to import from ASCII
channels = ['US_IC','us_ic', 'Se', 'Cd_L', 'Te_L', 'Au_L']

# uncomment this line to import maps with XBIC converted to ampere
# this requires XBIC channel ('us_ic') to be in first position of 'channels' list
#FS3.import_maps(ASCII_PATH, PATH_LOCKIN, channels)

# uncomment this line to import maps without XBIC converted to ampere
FS3.import_maps_no_XBIC_conversion(ASCII_PATH, channels)

#%%
'''
current maps

this cell was used to normalize the XBIC maps to the 
upstream ion chamber
to do this, use Sample class method 'import_maps_no_XBIC_conversion' above
	this keeps XBIC in cts/s

only run this cell if XBIC scans [323,327,...] are imported 
at the beginning of this program

it's important to normalize the XBIC channel ('us_ic') cts/s 
to upstream ion chamber ('US_IC') cts/s 
since the incident flux can change over the time of the experiment (up to 40hrs)
	especially during fill/unfill

normalization needs to be done before converting into ampere
	
'''

# normalize the xbic channel to the us_ic channel
xboc_norms = []
for scan in FS3.maps:
    us_ic = scan[0,:,:-2]
    xbic = scan[1,:,:-2]
    xbic_norm = xbic / us_ic
    xboc_norms.append(xbic_norm)

# turn maps in to vectors
import numpy as np
xbic_norms_ravel = [np.ravel(xbic_norm) for xbic_norm in xboc_norms]

# remove bad row in 100C map
xbic_norms_ravel[4] = np.delete(aligned_crop[4], 38, axis=1)

# turn list of vectors to nupmy array
xbic_norms_array = np.array(xbic_norms_ravel).T

OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\2_FS_operando\histogram arrays from python'
FNAME = r'\arrays_for_hist_normalizedXBICvTemp.csv'
np.savetxt(OUT_PATH+FNAME, xbic_norms_array, delimiter=",")

#%%
'''
voltage maps 

this cell was used to normalize the XBIV maps to the 
upstream ion chamber; to do this, the XBIV channel
was kept in cts/s, hence the use of the Sample class method
'import_maps_no_XBIC_conversion'

only run this cell if the XBIV scans are imported 
at the beginning of this program
'''
# it's important to normalize the XBIC channel 'us_ic' cts/s to the
# upstream ion chamber 'US_IC' cts/s before converting into ampere
    # the measurements took place over many hours and the incident beam
    # flux can easily change during that time (especially during fill/unfill)

FS3.import_maps_no_XBIC_conversion(ASCII_PATH, channels)

# normalize the xbic channel to the us_ic channel
xboc_norms = []
for scan in FS3.maps:
    us_ic = scan[0,:,:-2]
    xbic = scan[1,:,:-2]
    xbic_norm = xbic / us_ic
    xboc_norms.append(xbic_norm)

# turn maps in to vectors
import numpy as np
xbic_norms_ravel = [np.ravel(xbic_norm) for xbic_norm in xboc_norms]

# turn list of vectors to nupmy array
xbic_norms_array = np.array(xbic_norms_ravel).T

OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\2_FS_operando\histogram arrays from python'
FNAME = r'\arrays_for_hist_normalizedXBIVvTemp.csv'
np.savetxt(OUT_PATH+FNAME, xbic_norms_array, delimiter=",")

#%%
'''
this cell is backup in case i want to do an XRF absorption correction 
for the FS3 sample measured in the new operando stage 2019_06_2IDD
'''


#elements = [ele[0:2] for ele in channels[1:]]

#FS3.ug_to_mol(elements)
# attribute Sample.mol now exists; contains XRF maps as mol/cm2

#i want to apply a Se grading correction based off a function 
# from the cross-section integrated XRF profiles
    # the two cross-section maps from which to 
    # get integrated profiles:
        # FS2_1, 2019_03_2IDD, scan551
        # FS2_2, 2019_03_2IDD, scan661
    # 
#beam_settings = {'beam_energy': 12.7, 'beam_theta':75, 'detect_theta':15}

#FS3iios = XRFcorr.get_iios(beam_settings, elements, FS3.stack, end_layer='Se')
#scans_for_correction = FS3.scans
#FS3.apply_iios(scans_for_correction, FS3iios)

# i need to modify the apply_iios definition in Sample() class
# in order to handle an Se gradient

