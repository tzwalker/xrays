"""
coding: utf-8

tzwalker
Tue Mar 23 16:39:59 2021

this program contains code snippets that aid in plotting PL and Raman
data from a wdf file

"""

def get_map_of_bin(user_input, map_of_spectra):
    # find the value in the x-axis that is closest to the specified x-axis value
    E_idx = (np.abs(bins - user_input)).argmin()
    # extract bin from the spectral map
    map_of_bin = map_of_spectra[:,:,E_idx]
    return map_of_bin


# example file import
from renishawWiRE import WDFReader
import matplotlib.pyplot as plt
import numpy as np
 
IN_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\Raman'
FNAME = r'\20210203 PVSe33 redo - PVSe334_3 - Au Side map 1.wdf'

# import wdf file
filename = IN_PATH+FNAME
reader = WDFReader(filename)
reader.print_info()

# get x-axis of spectral data
    # keep in mind the units you specified for the measurement
    # here the measurement was made using shift (cm-1) as the x-axis
bins = reader.xdata

# get the spectral data from the map; has form (y_pixel, x_pixel, intensity)
spectra = reader.spectra

#%%
# specify the x-axis value you wish to plot
    # here the CdTe peaks of interest are 127,141,167,275,365cm-1
raman_shift = 141
map_of_bin = get_map_of_bin(raman_shift, spectra)

#%%
'''this cell takes an incomplete scan and chops off the last row'''
# maybe insert a if statement here that checks if the map is complete
    # if reader.capacity == reader.count: chop off last row
# scan 31x31 = 961
# file array (960,512)
# new array 30x31 = 930
spectra2 = spectra[:930,:]
spectra3 = spectra2.reshape(30,31,-1)
#%%
'''
this cell takes the ratio between two peak intesities at each pixel
and plots that ratio as a function of x and y
'''

# raman_peak 1 (primary peak)
raman_shift1 = 141
raman_shift2 = 275
map_of_bin1 = get_map_of_bin(raman_shift1, spectra)
map_of_bin2 = get_map_of_bin(raman_shift2, spectra)

ratio_map = map_of_bin2/map_of_bin1

# get relative positions of the x and y motors
map_x = reader.xpos
map_y = reader.ypos
# specificy the bounds of the area that was measured
bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
plt.imshow(ratio_map, extent=bounds_map)

#%%
'''
this cell isolates a peak based on user-defined shift
and plots the spectrum around this peak
'''

def get_peak_bounds(shift_array, lower, upper):
    idx_low = np.abs(shift_array - lower).argmin()
    idx_hi = np.abs(shift_array - upper).argmin()
    return idx_low,idx_hi

low, high = get_peak_bounds(shift, 50,200)

peak_shift = shift[high:low]
peak_i = spectra[10,24,high:low]
plt.plot(peak_shift, peak_i)

#%%
'''
this cell selects a specified gaussian fit parameter
and plots it as a map
'''

# specify parameter 
    # 1: amplitude1, 2: energy position1, 3: width1
    # 4: amplitude2, 5: energy position2, 6: width2
fit_param = 1

# extract parameter for each pixel
    # note if array isn't loaded, then you will have to import the file
relevant_data = stored_gauss_params[:,fit_param]

# reshape into map shape
x = np.shape(spectra)[1]
y = np.shape(spectra)[0]
param_map = relevant_data.reshape(y,x)

# in case column is offset
roll_map = 1
if roll_map == 1:
    roll = np.roll(param_map, -1, axis=1)
# plot parameter map
plt.imshow(roll)

#%%
'''
this cell fits average spectrum of glass side
with double gaussian and plot the results
'''
def gaussian_plot(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

def single_gauss_fit(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

def multi_gaussian_fit(x, *pars):
    offset = pars[0]
    g1 = single_gauss_fit(x, pars[1], pars[2], pars[3])
    g2 = single_gauss_fit(x, pars[4], pars[5], pars[6])
    return g1 + g2 + offset

from scipy import optimize

# fit to double gaussian
# initial fit parameter guess
    # [offset, A1, xc1, width1, A2, xc2, width2]
guess = [0, 10000, 1.4, 0.01, 2000, 1.37, 0.01]  # for 0hr glass side spectrum
popt, pcov = optimize.curve_fit(multi_gaussian_fit, energy, zaverage_arpls, guess)

# plot the data with the gaussian fits
plt.plot(energy, zaverage_arpls, '-', color='#1f77b4', label='0hr')
gauss1 =  gaussian_plot(energy, popt[1], popt[2], popt[3])
plt.plot(energy, gauss1, 'g-.',label='peak1')
gauss2 =  gaussian_plot(energy, popt[4], popt[5], popt[6])
plt.plot(energy, gauss2, 'm-.', label='peak2')
gaussian_fits = multi_gaussian_fit(energy, *popt)
plt.plot(energy, gaussian_fits, 'r--', label='total_fit')
plt.xlabel('energy (eV)')
plt.ylabel('intensity (a.u.)')
plt.legend()

#%%
'''
TO PROCESS MAPS PIX-BY-PIX, spectra with two peaks

this cell subtracts background and fits gaussian
to each spectrum in each pixel

the gaussian fit parameters are stored and can be saved for boxplot analysis
or reshaping and mapping
'''

import time
start = time.time()

import sys
sys.path.append(r'C:\Users\triton\xrays\python')
from baseline_algorithms import arpls
from scipy import optimize


def gaussian_plot(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

def single_gauss_fit(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

def multi_gaussian_fit(x, *pars):
    offset = pars[0]
    g1 = single_gauss_fit(x, pars[1], pars[2], pars[3])
    g2 = single_gauss_fit(x, pars[4], pars[5], pars[6])
    return g1 + g2 + offset

# initial fit parameter guess; find from plotting background-subtraction
    # [offset, A1, xc1, width1, A2, xc2, width2]
guess = [0, 750, 1.388, 0.01, 250, 1.371, 0.01] 

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
stored_gauss_params = np.zeros((pixels,7))
for pix, spectrum in enumerate(spectra_ravel):
    # construct and subtract baseline from pixel spectrum
    baseline_arpls = arpls(spectrum, 1e6, 0.01)
    spectrum_arpls = spectrum - baseline_arpls
    # fit gaussian to background-subtracted spectrum
    popt, pcov = optimize.curve_fit(multi_gaussian_fit, energy, spectrum_arpls, guess)
    # store gaussian fit values; popt needs to be transposed
        #  since optimize.curve_fit outputs as (4,1) array
    stored_gauss_params[pix,:] = popt.T

end = time.time()
t = end-start
t_str = "%.3f" % t
message = 'time to complete: {i}s'.format(i=str(t_str))
print(message)
#%%
SAVE = 0
if SAVE == 1:
    OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\PL'
    OUT_FILE = r'\gaussian fit params - 20210312 PVSe33.3_2 glass side PL map1.wdf.csv'
    OUT = OUT_PATH + OUT_FILE
    np.savetxt(OUT, stored_gauss_params, delimiter=',')