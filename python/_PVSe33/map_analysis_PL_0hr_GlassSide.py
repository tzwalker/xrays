"""
coding: utf-8

tzwalker
Wed Feb  3 09:49:31 2021

glass side measurements taken with 5x objective, 5% laser power, 0.25s dwell

glass side measurements showed the presence of two peaks

this program loads the map measurement file, 
constructs an average spectrum from the spectra of the pixels,
constructs and subtracts a baseline from the average spectrum
fits background-subtracted, average spectrum with two gaussian peaks

relevant files can be found here
'Z:\Trumann\Renishaw\PVSe33 measurement overview.txt'

"""

from renishawWiRE import WDFReader
import matplotlib.pyplot as plt
import numpy as np
 
IN_PATH = r'Z:\Trumann\Renishaw\20210304 PVSe33'
FNAME = r'\PVSe33.3_2 Glass side PL map0.wdf'

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

'''this cell averages the spectra in each pixel'''
z = np.shape(spectra)[2]
y = np.shape(spectra)[0]
x = np.shape(spectra)[1]
spectra_ravel = spectra.reshape((x*y),z)

z_average = np.mean(spectra_ravel, axis=0)
z_std = np.std(spectra_ravel, axis=0)
plt.plot(energy,z_average)

#%%
'''this cell averages the spectra in each pixel'''

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
'''this cell takes the average spectrum from a map and checks
performs a baseline subtraction; prepatory step for gaussian fits'''

import sys
sys.path.append(r'C:\Users\triton\xrays\python')
from baseline_algorithms import arpls


# construct and subtract baseline from average spectrum

# for glass side spectra
baseline_arpls = arpls(z_average, 1e6, 0.01)

zaverage_arpls = z_average - baseline_arpls
# check subtraction
plt.plot(energy,z_average)
plt.plot(energy,zaverage_arpls)
#%%
'''this cell fits average spectrum of glass side
with double gaussian and plot the results'''
def gaussian_plot(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

# =============================================================================
# def single_gauss_fit(x, A, x0, sig):
#     return A*np.exp(-(x-x0)**2/(2*sig**2))
# =============================================================================

def multi_gaussian_fit(x, *pars):
    offset = pars[0]
    g1 = single_gauss_fit(x, pars[1], pars[2], pars[3])
    g2 = single_gauss_fit(x, pars[4], pars[5], pars[6])
    return g1 + g2 + offset

from scipy import optimize

# fit to double gaussian
# initial fit parameter guess
    # [offset, A1, xc1, width1, A2, xc2, width2]
guess = [0, 750, 1.388, 0.01, 250, 1.371, 0.01]  # for 0hr glass side spectrum
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
this cell acesses a wavenumber, raman shift, or energy of interest
and plots its intensity as a funciton of x and y

if the map was aborted, then some shaping things needs to happen
'''

aborted_map=0
# specify the x-axis value you wish to plot
    # this value is taken from the Gaussian fit above
PL_energy = 1.384
if aborted_map == 1:
    # clip spectra, remove last row of 101x101map --> 101x100 spectra --> 10100 rows
    spectra2 = spectra[:10100,:]
    # reshape clipped spectra
    spectra2_map = spectra2.reshape(100,101,-1)

    # find the value in the x-axis that is closest to the specified x-axis value
    E_idx = (np.abs(energy - PL_energy)).argmin()
    # get relative positions of the x and y motors
    map_x = reader.xpos
    map_y = reader.ypos
    # specificy the bounds of the area that was measured
    bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
    raman_map = spectra2_map[:,:,E_idx]
    plt.imshow(raman_map, extent=bounds_map)
else:
    E_idx = (np.abs(energy - PL_energy)).argmin()
    # get relative positions of the x and y motors
    map_x = reader.xpos
    map_y = reader.ypos
    # specificy the bounds of the area that was measured
    bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
    raman_map = spectra[:,:,E_idx]
    plt.imshow(raman_map, extent=bounds_map)


#%%
'''
TO PROCESS MAPS PIX-BY-PIX

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
SAVE = 1
if SAVE == 1:
    OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\PL'
    OUT_FILE = r'\gaussian fit params - 20210304 PVSe33.3_2 Glass side PL map0.wdf.csv'
    OUT = OUT_PATH + OUT_FILE
    np.savetxt(OUT, stored_gauss_params, delimiter=',')
#%%
'''
this cell selects a specified gaussian fit parameter
and plots it as a map
'''

# specify parameter 
    # 1: amplitude1, 2: energy position1, 3: width1
    # 4: amplitude2, 5: energy position2, 6: width2
fit_param = 4

# extract parameter for each pixel
    # note if array isn't loaded, then you will have to import the file
relevant_data = stored_gauss_params[:,fit_param]

# reshape into map shape
x = np.shape(spectra)[1]
y = np.shape(spectra)[0]
param_map = relevant_data.reshape(y,x)

# plot parameter map
plt.imshow(param_map)
