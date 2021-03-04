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
 
IN_PATH = r'Z:\Trumann\Renishaw\20210301 PVSe33 PL glass side'
FNAME = r'\PVSe33.3_2 map0.wdf'

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
'''this cell averages the spectra in each pixel when the
scan gets hung up in on the last few points and must be aborted'''

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
def gaussian2(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

def multi_gaussian(x, *pars):
    offset = pars[0]
    g1 = gaussian2(x, pars[1], pars[2], pars[3])
    g2 = gaussian2(x, pars[4], pars[5], pars[6])
    return g1 + g2 + offset

from scipy import optimize

# fit to double gaussian
# initial fit parameter guess
    # [offset, A1, xc1, width1, A2, xc2, width2]
guess = [0, 300, 1.388, 0.009, 175, 1.371, 0.018] # for 0hr glass side spectrum
popt, pcov = optimize.curve_fit(multi_gaussian, energy, zaverage_arpls, guess)

# plot the data with the gaussian fits
plt.plot(energy, zaverage_arpls, '-', color='#1f77b4', label='0hr')
gauss1 =  gaussian2(energy, popt[1], popt[2], popt[3])
plt.plot(energy, gauss1, 'g-.',label='peak1')
gauss2 =  gaussian2(energy, popt[4], popt[5], popt[6])
plt.plot(energy, gauss2, 'm-.', label='peak2')
gaussian_fits = multi_gaussian(energy, *popt)
plt.plot(energy, gaussian_fits, 'r--', label='total_fit')
plt.xlabel('energy (eV)')
plt.ylabel('intensity (a.u.)')
plt.legend()

#%%
'''
this cell acesses a wavenumber, raman shift, or energy of interest
and plots its intensity as a funciton of x and y

here the energy was recorded after running the Gaussian fits,
there is no need to run the fits before running this cell
however, do run the first cell in this file

in this case, the scan froze toward the end, and was aborted prematurely
most of the data points were saved, but the last row in the map incomplete 
the data need to be clipped, then reshaped into the map

this map
IN_PATH = r'Z:\Trumann\Renishaw\20210224 PL glass side'
FNAME = r'\PVSe33.3_2 test map.wdf'
showed degradation similar to XBIC degradation; the second PL peak
is probably due to laser damage
'''
# clip spectra, remove last row of 101x101map --> 101x100 spectra --> 10100 rows
spectra2 = spectra[:10100,:]
# reshape clipped spectra
spectra2_map = spectra2.reshape(100,101,-1)

# specify the x-axis value you wish to plot
    # this value is taken from the Gaussian fit above
PL_energy = 1.384
# find the value in the x-axis that is closest to the specified x-axis value
E_idx = (np.abs(energy - PL_energy)).argmin()

# get relative positions of the x and y motors
map_x = reader.xpos
map_y = reader.ypos
# specificy the bounds of the area that was measured
bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
raman_map = spectra2_map[:,:,E_idx]
plt.imshow(raman_map, extent=bounds_map)

#%%
'''
this cell acesses a wavenumber, raman shift, or energy of interest
and plots its intensity as a funciton of x and y

here the energy was recorded after running the Gaussian fits,
there is no need to run the fits before running this cell
however, do run the first cell in this file
'''

# specify the x-axis value you wish to plot
    # this value is taken from the Gaussian fit above
PL_energy = 0.55#1.392
# find the value in the x-axis that is closest to the specified x-axis value
E_idx = (np.abs(energy - PL_energy)).argmin()

# get relative positions of the x and y motors
map_x = reader.xpos
map_y = reader.ypos
# specify the bounds of the area that was measured
bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
raman_map = spectra[:,:,E_idx]
raman_map_shift = np.roll(raman_map, -1)
#plt.imshow(raman_map, extent=bounds_map)
#plt.figure()
plt.imshow(raman_map_shift, extent=bounds_map)