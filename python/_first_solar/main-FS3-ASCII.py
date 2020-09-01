# -*- coding: utf-8 -*-
"""
tzwalker
Thu Apr  2 17:12:40 2020
coding: utf-8

BEGIN OPERANDO ANALYSES:
Sample FS3_3: 2019_06_2IDD
-abandoned h5 importing, the structure between the TW fit and BL fit
is far too different and not worth the time

ASCIIS_TW_BL have the combined data
    'us_ic' is the relevant scaler for the electrical channel
    'UC_IC' is the relevant scaler for the upstream ion chamber

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
322,323,324,325,326,327,328,329,330,331,332,333,
             337,338,339,340,341,342,343, 344, 345]

present workflow:
    "main-FS3-ASCII" --> 
    "XBIV-translate-and-deltas" --> 
    "translated analyses"
for plotting reference, pixel step was 150nm --> 20pixels = 3um, 67pix = 10um
"""

from class_ascii_Sample import Sample
ASCII_PATH = r'C:\Users\triton\FS3_2019_06_operando\ASCIIS_TW_BL'
PATH_LOCKIN = r'C:\Users\triton\FS3_2019_06_operando\ASCIIS_TW_BL\FS_plan_electrical.csv'
#ASCII_PATH =  r'C:\Users\Trumann\FS3_2019_06_operando\ASCIIS_TW_BL' 
#PATH_LOCKIN = r'C:\Users\Trumann\FS3_2019_06_operando\ASCIIS_TW_BL\FS_plan_electrical.csv'

# create sample objects
FS3 = Sample()

# define stack and scans of each sample, upstream layer first
FS3.stack = {'Au':   [19.3, 100E-7], 
                 'CdTe': [5.85, 5E-4],
                 'Se': [4.82, 100E-7],
                 'SnO2': [100E-7]}
FS3.scans = [321,325,330,337,342] #XBIC: [323,327,332,339,344] #XBIV: [321,325,330,337,342]


# channels to import from ASCII
channels = ['us_ic', 'Se', 'Cd_L', 'Te_L', 'Au_L']

FS3.import_maps(ASCII_PATH, PATH_LOCKIN, channels)

elements = [ele[0:2] for ele in channels[1:]]

#FS3.ug_to_mol(elements)
# attribute Sample.mol now exists; contains XRF maps as mol/cm2

#i want to apply a Se grading correction based off a function 
# from the cross-section integrated XRF profiles
    # the two cross-section maps from which to 
    # get integrated profiles:
        # FS2_1, 2019_03_2IDD, scan551
        # FS2_2, 2019_03_2IDD, scan661
    # 
beam_settings = {'beam_energy': 12.7, 'beam_theta':75, 'detect_theta':15}

#FS3iios = XRFcorr.get_iios(beam_settings, elements, FS3.stack, end_layer='Se')
#scans_for_correction = FS3.scans
#FS3.apply_iios(scans_for_correction, FS3iios)

# i need to modify the apply_iios definition in Sample() class
# in order to handle an Se gradient

