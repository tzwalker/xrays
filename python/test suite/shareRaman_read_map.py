"""
coding: utf-8

tzwalker
Thu Mar  4 16:41:19 2021

this program imports a .wdf file from the Renishaw WiRE software

this program requires installation of the package provided here:
    https://github.com/alchem0x2A/py-wdf-reader
    several installation options are available, but i reccommend
    installing using the Anaconda prompt

Raman spectra typically have better signal-to-noise ratios, so there is
not background subtracion performed in this program


"""

from renishawWiRE import WDFReader
import matplotlib.pyplot as plt

# input file path and file name
IN_PATH = r'Z:\Trumann\Renishaw\20210304 PVSe33'
FNAME = r'\PVSe33.4_3 Au side raman map0.wdf'

# import wdf file
filename = IN_PATH+FNAME
reader = WDFReader(filename)
reader.print_info()

# get x-axis of spectral data
    # keep in mind the units you specified for the measurement
    # here, raman shift (cm-1) was specified and would be the x-axis of the spectrum
shift = reader.xdata

# get the spectral data 
    # if .wdf file is a map, 'spectra' is 3D (y_pixel, x_pixel, intensity)
    # if .wdf file is spot, 'spectra' is 1D (intensity)
    # if .wdf file is aborted map, 'spectra' is 2D (y_pix*x_pix, intensity)
spectra = reader.spectra

# check the spectrum of the first pixel
    # this will not work if the map was aborted
first_pixel = spectra[0,0,:]
plt.plot(shift, first_pixel)

#%%
'''
often it can be intrsuctive to average over all Raman spectra in a map to
obtain the most significant peaks

this cell calculates the average Raman spectrum of a map
'''

import numpy as np

# calculate average spectrum
z = np.shape(spectra)[2]
y = np.shape(spectra)[0]
x = np.shape(spectra)[1]
spectra_ravel = spectra.reshape((x*y),z)
z_average = np.mean(spectra_ravel, axis=0)

# plot average spectrum
plt.plot(shift, z_average)

#%%
'''
this cell acesses the raman peak of interest
and plots its intensity as a funciton of x and y
'''

# specify the x-axis value you wish to plot
    # here the CdTe peaks of interest are 127,141,167,275,365cm-1
raman_shift = 141
# find the value on the x-axis that is closest to the specified x-axis value
E_idx = (np.abs(shift - raman_shift)).argmin()

# get relative positions of the x and y motors
map_x = reader.xpos
map_y = reader.ypos
# specificy the bounds of the area that was measured
bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
# extract intensity of the specified shift for all pixels
raman_map = spectra[:,:,E_idx]

# plot intensity versus x and y
plt.imshow(raman_map, extent=bounds_map)