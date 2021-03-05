"""
coding: utf-8

tzwalker
Thu Feb  4 10:47:19 2021

this program is used to import and process Raman map data

this program uses the packages provided here:
    https://github.com/alchem0x2A/py-wdf-reader

Raman CdTe peaks of interest are 127,141,167,275,365cm-1
 
relevant data files can be found here
'Z:\Trumann\Renishaw\PVSe33 measurement overview.txt'
"""

from renishawWiRE import WDFReader
import matplotlib.pyplot as plt
import numpy as np
 
IN_PATH = r'Z:\Trumann\Renishaw\20210213 PVSe33 redo 2'
FNAME = r'\PVSe33.3_2 Au Side_raman_map0.wdf'

# import wdf file
filename = IN_PATH+FNAME
reader = WDFReader(filename)
reader.print_info()

# get x-axis of spectral data
    # keep in mind the units you specified for the measurement
    # here the measurement was made using shift (cm-1) as the x-axis
shift = reader.xdata

# get the spectral data from the map; has form (y_pixel, x_pixel, intensity)
spectra = reader.spectra

#%%
'''this cell averages the spectra in each pixel'''
z = np.shape(spectra)[2]
y = np.shape(spectra)[0]
x = np.shape(spectra)[1]
spectra_ravel = spectra.reshape((x*y),z)

z_average = np.mean(spectra_ravel, axis=0)
z_std = np.std(spectra_ravel, axis=0)
plt.plot(shift, z_average)

#%%
'''
this cell acesses a wavenumber, raman shift, or energy of interest
and plots its intensity as a funciton of x and y
'''
# specify the x-axis value you wish to plot
    # here the CdTe peaks of interest are 127,141,167,275,365cm-1
raman_shift = 141
# find the value in the x-axis that is closest to the specified x-axis value
E_idx = (np.abs(shift - raman_shift)).argmin()

# get relative positions of the x and y motors
map_x = reader.xpos
map_y = reader.ypos
# specificy the bounds of the area that was measured
bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
raman_map = spectra[:,:,E_idx]
plt.imshow(raman_map, extent=bounds_map)

#%%
'''
this cell takes the ratio between two peak intesities at each pixel
and plots that ratio as a function of x and y
'''
# raman_peak 1 (primary peak)
raman_shift1 = 141
E_idx1 = (np.abs(shift - raman_shift1)).argmin()
# rmaman_peak 2 (other peak of interest)
raman_shift2 = 275
E_idx2 = (np.abs(shift - raman_shift2)).argmin()

# maps of peak intensities
raman_map1 = spectra[:,:,E_idx1]
raman_map2 = spectra[:,:,E_idx2]

ratio_map = raman_map2/raman_map1

# get relative positions of the x and y motors
map_x = reader.xpos
map_y = reader.ypos
# specificy the bounds of the area that was measured
bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
plt.imshow(ratio_map, extent=bounds_map)
