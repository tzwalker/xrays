"""
coding: utf-8

tzwalker
Wed Feb  3 09:49:31 2021

Au side measurements taken with 50x objective, 1% laser power, 1.0s dwell

Au side measurements showed the presence of one peak

this program loads the map measurement file, 
constructs an average spectrum from the spectra of the pixels,
constructs and subtracts a baseline from the average spectrum
fits background-subtracted, average spectrum with one gaussian peak

relevant files can be found here
'Z:\Trumann\Renishaw\PVSe33 measurement overview.txt'
"""

from renishawWiRE import WDFReader
import matplotlib.pyplot as plt
import numpy as np
 
IN_PATH = r'Z:\Trumann\Renishaw\20210302 PVSe33.4_3'
FNAME = r'\Au side PL map0.wdf'

# import wdf file
filename = IN_PATH+FNAME
reader = WDFReader(filename)
reader.print_info()

### access spectral and optical image data
# get x-axis of spectral data
    # keep in mind the units you specified for the measurement
    # here the measurement was made using the eV as the x-axis
energy = reader.xdata

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
plt.plot(energy,z_average)

#%%
'''this cell takes the average spectrum from a map and
performs a baseline subtraction; prepatory step for gaussian fits'''

import sys
sys.path.append(r'C:\Users\triton\xrays\python')
from baseline_algorithms import arpls

# construct and subtract baseline from average spectrum

#for Au side spectra, 500hr
baseline_arpls = arpls(z_average, 1e7, 0.1)

zaverage_arpls = z_average - baseline_arpls
# check subtraction
plt.plot(energy,z_average)
plt.plot(energy,zaverage_arpls)

#%%
'''
this cell fits average spectrum of Au side
with single gaussian and plot the results
the amplitude guesses for these spectra will be substantially lower
than the geusses for the glass side spectra since 1% laser power was 
used for the Au side and 5% was used for the glass side 
'''
from scipy import optimize

def gaussian1(x,*pars):
    offset = pars[0]
    A = pars[1]
    x0 = pars[2]
    sig = pars[3]
    g1 = A*np.exp(-(x-x0)**2/(2*sig**2))
    return g1 + offset

def gaussian2(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

def multi_gaussian(x, *pars):
    offset = pars[0]
    g1 = gaussian2(x, pars[1], pars[2], pars[3])
    g2 = gaussian2(x, pars[4], pars[5], pars[6])
    return g1 + g2 + offset

# fit to double gaussian
# initial fit parameter guess
    # [offset, A1, xc1, width1]
guess = [0, 200, 1.50, 0.01] # for 0hr Au side spectrum
#guess = [0, 100, 1.50, 0.01] # for 500hr Au side spectrum
popt, pcov = optimize.curve_fit(gaussian1, energy, zaverage_arpls, guess)

# plot the data with the gaussian fits
plt.plot(energy, zaverage_arpls, '-', color='#1f77b4', label='500hr')
gauss1 =  gaussian2(energy, popt[1], popt[2], popt[3])
plt.plot(energy, gauss1, 'r--',label='peak1')
plt.xlabel('energy (eV)')
plt.ylabel('intensity (a.u.)')
plt.legend()

#%%
'''this cell takes an incomplete scan and chops off the last row'''

# scan 31x31 = 961
# file array (960,512)
# new array 30x31 = 930
spectra2 = spectra[:930,:]
spectra3 = spectra2.reshape(30,31,-1)

#%%
'''
this cell acesses a wavenumber, raman shift, or energy of interest
and plots its intensity as a funciton of x and y
'''
# specify the x-axis value you wish to plot
user_energy = 1.497
# find the value in the x-axis that is closest to the specified x-axis value
E_idx = (np.abs(user_energy - energy)).argmin()

# get relative positions of the x and y motors
map_x = reader.xpos
map_y = reader.ypos
# specificy the bounds of the area that was measured
bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
# extract map of a certain energy or shift
user_map = spectra3[:,:,E_idx]
plt.imshow(user_map, extent=bounds_map)

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
