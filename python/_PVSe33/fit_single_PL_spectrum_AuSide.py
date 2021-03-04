"""
coding: utf-8

tzwalker
Wed Feb  3 10:07:35 2021

this program i smeant to import and fit a single PL spectrum
from the Renishaw tool

it assumes you have exported the file as a .wdf file
"""

from renishawWiRE import WDFReader
import matplotlib.pyplot as plt
import numpy as np

'''this cell is for 0hr Au side'''
IN_PATH = r'Z:\Trumann\Renishaw\20210213 PVSe33 redo 2'
FNAME = r'\PVSe33.3_2 Au Side_PL_spot03.wdf'

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

plt.plot(energy, spectra)
plt.xlabel('Energy (eV)')
plt.ylabel('Intensity (.)')

OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\PL\spectra'
OUT_NAME = r'\20210213 PVSe33 redo 2 - PVSe33.3_2 Au Side_PL_spot03.csv'
OUT = OUT_PATH + OUT_NAME
out_data = np.vstack([energy,spectra]).T
#np.savetxt(OUT, out_data, delimiter=',')

#%%
'''this cell is for 500hr Au side'''
from renishawWiRE import WDFReader
import matplotlib.pyplot as plt
import numpy as np
 
IN_PATH = r'Z:\Trumann\Renishaw\20210302 PVSe33.4_3'
FNAME = r'\Au side PL spectrum0 - 3s - 1percent - 1accum.wdf'

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

plt.plot(energy, spectra)

#%%
'''this cell fits a baseline and subtracts it'''
# subtract baseline before fitting
from baseline_algorithms import arpls
baseline_arpls = arpls(spectra, 1e5, 0.1)
intensity_arpls = spectra - baseline_arpls
plt.plot(energy, spectra)
plt.plot(energy, intensity_arpls)

#%%
'''this cell fits a gaussian to a single peak'''

from scipy import optimize
import numpy as np

def gaussian(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

# gaussian fit try 1
popt, _ = optimize.curve_fit(gaussian, energy, intensity_arpls)
fitted_curve = gaussian(energy, *popt)

plt.plot(energy, intensity_arpls, label='Data (back. subtracted)')
plt.plot(energy, fitted_curve, 'r--',label='Gaussian Fit')
plt.xlabel('energy (eV)')
plt.ylabel('intensity (eV)')
plt.legend()



#%%
'''this cell fits two gaussians to a double peak
initial guess parameters are crucial'''


# multi-gaussian fit 2
#https://stackoverflow.com/questions/54851012/fitting-data-with-multiple-gaussian-profiles-in-python


def multi_gaussian(x, *pars):
    offset = pars[0]
    g1 = gaussian(x, pars[1], pars[2], pars[3])
    g2 = gaussian(x, pars[4], pars[5], pars[6])
    return g1 + g2 + offset

# Initial guesses for the parameters to fit:
# 3 amplitudes, means and standard deviations plus a continuum offset.
guess = [8.5, 2525, 1.39, 0.013, 500, 1.37, 0.01]
popt, pcov = optimize.curve_fit(multi_gaussian, energy, intensity_arpls, guess)
plt.plot(energy, intensity_arpls, label='Data')
g1_plus_g2 = multi_gaussian(energy, *popt)
plt.plot(energy, g1_plus_g2, 'r--', label='Fit')
plt.legend()

