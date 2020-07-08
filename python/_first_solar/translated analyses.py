"""
coding: utf-8

tzwalker
Tue Jul  7 17:05:57 2020

this program is meant for analyses of the aligned
XBIV scans produced using 
'_first_solar/XBIC-XBIV-translate-and-deltas.py'

before serious correlations are preformed, the XRF data should be
corrected for absorption
"""

# first try to import some arrays
PATH_IN = r'C:\Users\triton\Dropbox (ASU)\1_FS_operando\XBIC_XBIV aligned image csvs'
SCAN = 'scan325'
CHANNEL = 'Te'

from numpy import genfromtxt
FNAME = r'\FS3_{scn}_{chn}.csv'.format(scn=SCAN, chn=CHANNEL)
my_data = genfromtxt(PATH_IN+FNAME, delimiter=',')