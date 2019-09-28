'''
created: Fri Aug 16 14:49:13 2019
author: Trumann
'''
import z_plot_supplement as PLT

samp = NBL3_2
scan = 0
axis_label_sizes = 16

# use this function to plot normal-unit, corrected elemental maps
    # -1:XBIC, 0:Cu, 1:Cd, 2:Te, etc...
    # integer matches index of element in 'elements' you want to plot
PLT.plot_nice_2Dmap(samp, scan, axis_label_sizes, 'elXBIC', 0) 

# use this function to plot standardized maps
# useful for electrical channel, but can plot XRF as well
sample = NBL3_2
scan = 0
channel = 0
data = 'c_stand_arrs'
    # adds nan columns
    # 0:XBIC, 1:Cu, 2:Cd (match to index of 'elements' list)
PLT.from_stand_to_stand_map(sample, scan, data, channel)


