'''
created: Fri Aug 16 14:49:13 2019
author: Trumann

this file plots the original data with or without correct;
    original nans of the h5 file
    vmin and max of cbar calculated from data
useful for element plots!
'''
import z_plot_supplement as plt_supp

samp = NBL3_3
scan = 0
axis_label_sizes = 16

# use this function to plot normal-unit, corrected elemental maps
    # -1:XBIC, 0:Cu, 1:Cd, 2:Te, etc...
#plt_supp.plot_nice_2Dmap(samp, scan, axis_label_sizes, 'elXBIC_corr', 0) 

sample = TS58A
scan = 0
channel = 0
data = 'c_stand_arrs'
# use this functino to plot standardized electrical maps
    # adds nan columns
    # 0:XBIC, 1:Cu, 2:Cd (match to index of 'elements' list)
#plt_supp.from_stand_to_stand_map(sample, scan, data, channel)