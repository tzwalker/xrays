"""
coding: utf-8

tzwalker
Tue Jul  7 17:05:57 2020

this program is meant for analyses of the aligned
XBIV scans produced using 
'_first_solar/XBIC-XBIV-translate-and-deltas.py'

before serious correlations are preformed, the XRF data should be
corrected for absorption
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

"""
from numpy import genfromtxt
import matplotlib.pyplot as plt
# first try to import some arrays
PATH_IN = r'C:\Users\triton\Dropbox (ASU)\1_FS_operando\XBIC_XBIV aligned image csvs'

### "auto-retrieve" aligned image
# =============================================================================
# SCAN = 'scan325'
# CHANNEL = 'Te'
# FNAME = r'\FS3_{scn}_{chn}.csv'.format(scn=SCAN, chn=CHANNEL)
# img0 = genfromtxt(PATH_IN+FNAME, delimiter=',')
# =============================================================================
scans = [321,325,330,337,342]
scans1 = [str(s) for s in scans]
imgs = []
for s in scans1:
    FNAME = r'\FS3_scan{SCN}_XBIV.csv'.format(SCN=s)
    img0 = genfromtxt(PATH_IN+FNAME, delimiter=',')
    imgs.append(img0)

dels = [x - y for x, y in zip(imgs[1:], imgs[0:])]

for d in dels:
    plt.figure()
    plt.imshow(d, cmap='RdYlGn')
