"""
coding: utf-8

tzwalker
Wed Feb  3 09:49:31 2021

Au side measurements showed the presence of one peak

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
 
IN_PATH = r'Z:\Trumann\Renishaw\20210304 PVSe33'
FNAME = r'\PVSe33.4_3 Au side PL map0.wdf'

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
from scipy.stats import iqr
from sklearn.preprocessing import normalize
aborted_map = 1

if aborted_map == 0:
    # for a map that was not aborted
    z = np.shape(spectra)[2]
    y = np.shape(spectra)[0]
    x = np.shape(spectra)[1]
    spectra_ravel = spectra.reshape((x*y),z)

    # stats of spectra without normalizing
    z_average = np.mean(spectra_ravel, axis=0)
    z_std = np.std(spectra_ravel, axis=0)
    q = iqr(spectra_ravel, axis=0, rng=(25 ,75))
    
    # stats of spectra with normalizing; this was done to see
        # if i could get rid of some error bar artifacts in origin
    spectra_norm = normalize(spectra_ravel, axis=1, norm='max')
    norm_avg = np.mean(spectra_norm, axis=0)
    
    norm_q = iqr(spectra_norm, axis=0, rng=(25,75))
    x = np.vstack((norm_avg,norm_q)).T
    
if aborted_map == 1:
    # stats of spectra without normalizing
    z_average = np.mean(spectra, axis=0)
    z_std = np.std(spectra, axis=0)
    q = iqr(spectra, axis=0, rng=(25 ,75))
    
    # stats of spectra with normalizing; this was done to see
        # if i could get rid of some error bar artifacts in origin
    spectra_norm = normalize(spectra, axis=1, norm='max')
    norm_avg = np.mean(spectra_norm, axis=0)
    
    norm_q = iqr(spectra_norm, axis=0, rng=(25,75))
    x = np.vstack((norm_avg,norm_q)).T


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
aborted_map = 1
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

end = time.time()
t = end-start
t_str = "%.3f" % t
message = 'time to complete: {i}s'.format(i=str(t_str))
print(message)

SAVE = 1
if SAVE == 1:
    OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\PL'
    OUT_FILE = r'\gaussian fit params - 20210304 PVSe33.4_3 Au Side_PL_map0.csv'
    OUT = OUT_PATH + OUT_FILE
    np.savetxt(OUT, stored_gauss_params, delimiter=',')