"""
coding: utf-8

tzwalker
Tue Feb  2 14:01:17 2021

this file contains programs that help analzye the cross section scans
2018_11_26IDC, TS118_1Ax

the good, 2D scans are
0039
0043
0046
0051 --> this one was selected because it has the least XBIC artifacts

note: run main-TS118_1A-ASCII.py before running this program!
    -for the early cross section scans 39,43,46,51, the Sample class 
    does not have methods that correspond to the scan number
    -somethign is p with how the early scan string, e.g. '0039',
    gets interpreted and stored in the Sample class; i have not fixed it
    -the maps of these scans are accessed through the '.maps' method
    which is a list

"""

# =============================================================================
# # quick idea: for unfiltered map, sum along an axis and compare to 
# # unfiltered timeseries
# 
# unfilt = TS1181A.scan195[0,:,:]
# b = np.sum(unfilt, axis=1)
# plt.plot(b)
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt

save = 1
# maps[0] --> scan0039, maps[3] --> scan0051, etc.
scan = TS1181A.maps[3][2,:,:]
column_sum = np.sum(scan, axis=0)
plt.plot(column_sum)

if save == 1:
    PATH_OUT = r'C:\Users\triton\Dropbox (ASU)\1_XBIC_decay'
    FNAME = r'\TS118_1Ax_scan0051_Cd_integrated.csv'
    np.savetxt(PATH_OUT+FNAME, column_sum, delimiter=',')
