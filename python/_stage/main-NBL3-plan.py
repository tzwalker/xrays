"""
coding: utf-8

tzwalker
Thu Dec  3 10:21:04 2020

this is meant to process the scans of the Au 1234 pattern
used to quantify the oeprando stage resolution

there is no XBIC data for this scan, so the 'Sample'
class has been edited to include a 'import_XRFmaps' method
    the method is basically the same as 'import_maps',
    but excludes the operations that extrical electrical maps
"""

from classh5_Sample import Sample
        

DATA_PATH =  r'Z:\Trumann\Fitted_Sychrotron_Data\2019_06_2IDD_stage\img.dat'

# create sample objects
Au4 = Sample()

# define stack and scans of each sample
#Au4.stack = {'Au':   [10.2, 100E-7], 'Si': [2.33,200E-6]}
Au4.scans = [243,244]

# import h5 data for each sample
Au4.import_scan_data(DATA_PATH)
# "sample.h5data" now exists: holds h5 files

elements = ['Au_L', 'Si']
Au4.import_XRFmaps(elements, 'us_ic', 'fit')

# plot the "Au 4" at 25 and 100C to show where linescans were taken
