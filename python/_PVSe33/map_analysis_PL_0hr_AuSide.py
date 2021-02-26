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
 
IN_PATH = r'Z:\Trumann\Renishaw\20210213 PVSe33 redo 2'
FNAME = r'\PVSe33.3_2 Au Side_PL_map0.wdf'

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
'''this cell takes the average spectrum from a map and checks
performs a baseline subtraction; prepatory step for gaussian fits'''

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

import sys
sys.path.append(r'C:\Users\triton\xrays\python')
from baseline_algorithms import arpls
from scipy import optimize

# construct and subtract baseline from average spectrum

#for Au side spectra, 0hr
baseline_arpls = arpls(z_average, 1e5, 0.01)

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

# fit to double gaussian
# initial fit parameter guess
    # [offset, A1, xc1, width1]
guess = [0, 200, 1.50, 0.01] # for 0hr Au side spectrum
popt, pcov = optimize.curve_fit(gaussian1, energy, zaverage_arpls, guess)

# plot the data with the gaussian fits
plt.plot(energy, zaverage_arpls, '-', color='#1f77b4', label='0hr')
gauss1 =  gaussian2(energy, popt[1], popt[2], popt[3])
plt.plot(energy, gauss1, 'r--',label='peak1')
plt.xlabel('energy (eV)')
plt.ylabel('intensity (a.u.)')
plt.legend()
