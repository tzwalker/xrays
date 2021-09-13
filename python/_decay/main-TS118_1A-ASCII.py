"""
coding: utf-8

tzwalker
Wed May 27 18:25:55 2020

analyses for XBIC decay data

plan view maps: 195-200
    -these scans were not merged and were directly exported using MAPS
    -the Sample class was written for merged csvs
    -the following was done to the files to accomodate Sample class import:
        -filenames were changed from "h5.csv" to "h5_mda.csv"
        -1sr row of csv deleted; contained
        "ascii information for file: combined_ASCII_26idbSOFT_0195.h5.csv"
    -the lockin XBIC channel header: 'ds_ic'
    
xsect maps: 39,51
    -these were merged from mda and h5 csv outputs
    -the lockin XBIC channel header: '26idc:3820:scaler1_cts2.B'
    -the direct XBIC channel header: '26idc:3820:scaler1_cts2.C' (double check)
    
"""

from class_ascii_Sample import Sample
ASCII_PATH =  r'C:\Users\triton\XBIC_decay\TS118A_1A_2018_11_26IDC' 
PATH_LOCKIN = r'C:\Users\triton\Dropbox (ASU)\2_XBIC_decay\decay_electrical.csv'

# create sample objects
TS1181A = Sample()

# define stack and scans of each sample
TS1181A.stack = {'Au':   [19.3, 100E-7], 
                 'CdTe': [5.85, 5E-4],
                 'Se': [4.82, 100E-7],
                 'SnO2': [100E-7]}
TS1181A.scans = [195,196,197,198,199,200] #[39, 43, 46, 51]


# channels to import from ASCII, for plan-view
channels = ['ds_ic', 'Cu', 'Cd_L', 'Te_L', 'Au_M']
# for cross-section
#channels = ['26idc:3820:scaler1_cts2.B', 'Cu', 'Cd_L', 'Te_L', 'Au_M']


TS1181A.import_maps(ASCII_PATH, PATH_LOCKIN, channels, sector=26)

elements = [ele[0:2] for ele in channels[1:]]

#FS3.ug_to_mol(elements)
# attribute Sample.mol now exists; contains XRF maps as mol/cm2

# =============================================================================
# beam_settings = {'beam_energy': 12.7, 'beam_theta':75, 'detect_theta':15}
# 
# FS3iios = XRFcorr.get_iios(beam_settings, elements, FS3.stack, end_layer='Se')
# scans_for_correction = FS3.scans
# FS3.apply_iios(scans_for_correction, FS3iios)
# =============================================================================
