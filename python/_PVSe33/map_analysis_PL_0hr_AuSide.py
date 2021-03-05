"""
coding: utf-8

tzwalker
Wed Feb  3 09:49:31 2021

this program is used to import and process PL map data

this program uses the packages provided here:
    https://github.com/alchem0x2A/py-wdf-reader
    
Au side PL spectra showed only one PL peak

relevant data files can be found here
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
'''
this cell averages the spectra in each pixel
'''
aborted_map = 0

if aborted_map == 0:
    # for a map that was not aborted
    z = np.shape(spectra)[2]
    y = np.shape(spectra)[0]
    x = np.shape(spectra)[1]
    spectra_ravel = spectra.reshape((x*y),z)

    z_average = np.mean(spectra_ravel, axis=0)
    z_std = np.std(spectra_ravel, axis=0)
    
if aborted_map == 1:
    # for map that was aborted
    z_average = np.mean(spectra, axis=0)
    z_std = np.std(spectra, axis=0)

plt.plot(energy,z_average)


#%%
'''
this cell takes the average spectrum from a map and
performs a baseline subtraction; prepatory step for gaussian fits

this is also a useful step to check the arpls parameters and how they'll
construct a baseline
'''

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
'''


def gaussian_fit(x,*pars):
    offset = pars[0]
    A = pars[1]
    x0 = pars[2]
    sig = pars[3]
    g1 = A*np.exp(-(x-x0)**2/(2*sig**2))
    return g1 + offset

def gaussian_plot(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

# initial fit parameter guess
    # [offset, A1, xc1, width1]
guess = [0, 200, 1.50, 0.01] # for 0hr Au side spectrum
popt, pcov = optimize.curve_fit(gaussian_fit, energy, zaverage_arpls, guess)

# plot the data with the gaussian fits
plt.plot(energy, zaverage_arpls, '-', color='#1f77b4', label='0hr')
gauss1 =  gaussian_plot(energy, popt[1], popt[2], popt[3])
plt.plot(energy, gauss1, 'r--',label='peak1')
plt.xlabel('energy (eV)')
plt.ylabel('intensity (a.u.)')
plt.legend()

#%%
'''
this cell acesses a wavenumber, raman shift, or energy of interest
and plots its intensity as a funciton of x and y
'''
# specify the x-axis value you wish to plot
user_energy = 1.497
# find the value in the x-axis that is closest to the specified x-axis value
E_idx = (np.abs(energy - user_energy)).argmin()

# get relative positions of the x and y motors
map_x = reader.xpos
map_y = reader.ypos
# specificy the bounds of the area that was measured
bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
PL_map = spectra[:,:,E_idx]
plt.imshow(PL_map, extent=bounds_map)

#%%
'''
this cell subtracts background and fits gaussian
to each spectrum in each pixel

the gaussian fit parameters are stored and can be saved for boxplot analysis
or reshaping and mapping
'''

import sys
sys.path.append(r'C:\Users\triton\xrays\python')
from baseline_algorithms import arpls
from scipy import optimize

def gaussian_fit(x,*pars):
    offset = pars[0]
    A = pars[1]
    x0 = pars[2]
    sig = pars[3]
    g1 = A*np.exp(-(x-x0)**2/(2*sig**2))
    return g1 + offset

def gaussian_plot(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

# initial fit parameter guess; find from plotting background-subtraction
    # [offset, A1, xc1, width1]
guess = [0, 200, 1.50, 0.01]

# reshape spectra so they may be iterated over
aborted_map = 0
if aborted_map == 0:
    # for a map that was not aborted
    z = np.shape(spectra)[2]
    y = np.shape(spectra)[0]
    x = np.shape(spectra)[1]
    spectra_ravel = spectra.reshape((x*y),z)
if aborted_map == 1:
    spectra_ravel = spectra.copy()


# construct array to store gaussian fit parameters
    # the no. of rows (4) correspond to the number of optimization parameters
    # from the optimize.curve_fit function: offset, A, x0, sig
    # the no. of columns correspond to the number of pixels or spectra measured
pixels = np.shape(spectra_ravel)[0]
stored_gauss_params = np.zeros((pixels,4))
for pix, spectrum in enumerate(spectra_ravel):
    # construct and subtract baseline from pixel spectrum
    baseline_arpls = arpls(spectrum, 1e5, 0.01)
    spectrum_arpls = spectrum - baseline_arpls
    # fit gaussian to background-subtracted spectrum
    popt, pcov = optimize.curve_fit(gaussian_fit, energy, spectrum_arpls, guess)
    # store gaussian fit values; popt needs to be transposed
        #  since optimize.curve_fit outputs as (4,1) array
    stored_gauss_params[pix,:] = popt.T

SAVE = 0
if SAVE == 1:
    OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\PL'
    OUT_FILE = r'\gaussian fit params - 20210304 PVSe33.3_2 Au Side_PL_map0.csv'
    OUT = OUT_PATH + OUT_FILE
    np.savetxt(OUT, stored_gauss_params, delimiter=',')

#%%
'''
this cell selects a specified gaussian fit parameter
and plots it as a map
'''

# specify parameter 
    # 1: amplitude 2: energy position 3: width
fit_param = 1

# extract parameter for each pixel
relevant_data = stored_gauss_params[:,fit_param]

# reshape into map shape
x = np.shape(spectra)[1]
y = np.shape(spectra)[0]
param_map = relevant_data.reshape(y,x)

# plot parameter map
plt.imshow(param_map)

# if parameter map is amplitude, plot original map intensity at 
    # the peak user finds
# specify the x-axis value you wish to plot
user_energy = 1.497
# find the value in the x-axis that is closest to the specified x-axis value
E_idx = (np.abs(energy - user_energy)).argmin()

# get relative positions of the x and y motors
map_x = reader.xpos
map_y = reader.ypos
# specificy the bounds of the area that was measured
bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
PL_map = spectra[:,:,E_idx]
plt.figure()
plt.imshow(PL_map, extent=bounds_map)
