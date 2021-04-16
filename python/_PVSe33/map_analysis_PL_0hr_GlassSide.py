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

basic workflow:
        import spectral map
        calculate average spectrum over all spectra
        manually determine fit parameters for baseline
        subtract baseline from average spectrum
        manually determine fit parameters for gaussian fit of average spectrum
        use these fit parameters to fit spectrum of each pixel
"""

from renishawWiRE import WDFReader
import matplotlib.pyplot as plt
import numpy as np
 
IN_PATH = r'Z:\Trumann\Renishaw\20210312 PVSe33 PL glass side hiRes'
FNAME = r'\PVSe33.3_2 PL glass side map1.wdf'

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
background subtraction of average spectrum
shows user what guesses to use for gaussian fits
'''

import sys
sys.path.append(r'C:\Users\triton\xrays\python')
from baseline_algorithms import arpls


# construct and subtract baseline from average spectrum

# for glass side spectra
baseline_arpls = arpls(z_average, 1e7, 0.1)

zaverage_arpls = z_average - baseline_arpls
# check subtraction
plt.plot(energy,z_average)
plt.plot(energy,zaverage_arpls)

#%%
'''
this cell fits average spectrum of glass side
with single gaussian and plot the results
'''
def gaussian_plot(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

def single_gauss_fit(x, *pars):
    offset = pars[0]
    A = pars[1]
    x0 = pars[2]
    sig = pars[3]
    return offset + A*np.exp(-(x-x0)**2/(2*sig**2))

from scipy import optimize

# fit to double gaussian
# initial fit parameter guess
    # [offset, A1, xc1, width1]
guess = [0, 10000, 1.4, 0.01]
popt, pcov = optimize.curve_fit(single_gauss_fit, energy, zaverage_arpls, guess)

# plot the data with the gaussian fits
plt.plot(energy, zaverage_arpls, '-', color='#1f77b4', label='0hr')
gaussian_fits = gaussian_plot(energy, popt[1], popt[2], popt[3])
plt.plot(energy, gaussian_fits, 'r--', label='total_fit')
plt.xlabel('energy (eV)')
plt.ylabel('intensity (a.u.)')
plt.legend()

#%%
'''
TO PROCESS MAPS PIX-BY-PIX, spectra with one peak

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

def single_gauss_fit(x, *pars):
    offset = pars[0]
    A = pars[1]
    x0 = pars[2]
    sig = pars[3]
    return offset + A*np.exp(-(x-x0)**2/(2*sig**2))

# initial fit parameter guess; find from plotting background-subtraction
    # [offset, A1, xc1, width1]
guess = [0, 10000, 1.4, 0.01]

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
    baseline_arpls = arpls(spectrum, 1e7, 0.1)
    spectrum_arpls = spectrum - baseline_arpls
    # fit gaussian to background-subtracted spectrum
    popt, pcov = optimize.curve_fit(single_gauss_fit, energy, spectrum_arpls, guess)
    # store gaussian fit values; popt needs to be transposed
        #  since optimize.curve_fit outputs as (4,1) array
    stored_gauss_params[pix,:] = popt.T

end = time.time()
t = end-start
t_str = "%.3f" % t
message = 'time to complete: {i}s'.format(i=str(t_str))
print(message)

