"""
coding: utf-8
Trumann
Mon Feb  7 16:53:50 2022

this program gets one of the maps during the in-situ measurement
2021_11_2IDD

for now it is intended only to plot things for DoE

standford: 50uA/V
lockin output: 500 V/V

scaler_factor = (stanford*1E-9) / (2e5*lockin)

"""

from class_ascii_Sample import Sample

ASCII_PATH =  r'C:\Users\Trumann\Dropbox (ASU)\2_insitu_Cu_cross_section\output' 
#PATH_LOCKIN = r'C:\Users\Trumann\FS3_2019_06_operando\ASCIIS_TW_BL\FS_plan_electrical.csv'

# create sample objects
Cu1b4c = Sample()

# define stack and scans of each sample, upstream layer first
Cu1b4c.stack = {'Au':   [19.3, 100E-7], 
                 'CdTe': [5.85, 5E-4],
                 'Se': [4.82, 100E-7],
                 'SnO2': [100E-7]}
#Cu1b4c.scans = [238,366]
Cu1b4c.scans = [238,254,271,285,298,317,341,353,366,524]

# channels to import from ASCII
channels = [' us_ic', ' ds_ic', ' Cu', ' Se_L', ' Cd_L', ' Te_L', ' Au_M']

# uncomment this line to import maps with XBIC converted to ampere
# this requires XBIC channel ('us_ic') to be in first position of 'channels' list
#Cu1b4c.import_maps(ASCII_PATH, PATH_LOCKIN, channels)

# uncomment this line to import maps without XBIC converted to ampere
Cu1b4c.import_maps_no_XBIC_conversion(ASCII_PATH, channels)

