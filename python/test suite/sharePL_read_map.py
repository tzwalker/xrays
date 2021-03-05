"""
coding: utf-8

tzwalker
Thu Mar  4 16:41:19 2021

this program imports a .wdf file from the Renishaw WiRE software

this program requires installation of the package provided here:
    https://github.com/alchem0x2A/py-wdf-reader
    several installation options are available, but i reccommend
    installing using the Anaconda prompt

this program requires the 'arpls' module from here:
    https://irfpy.irf.se/projects/ica/_modules/irfpy/ica/baseline.html
    this link has many useful backgorund subtraction algorithims
    the 'arpls' algorithim stands for 
    Asymmetrically Reweighted Penalized Least Squares smoothing
        Sung-June Baek, Aaron Park, Young-Jin Ahna and Jaebum Choo,
        Analyst, 2015, 140, 250 (2015)
    'arpls' was found to be suitable for most spectra


"""

from renishawWiRE import WDFReader
import matplotlib.pyplot as plt

# input file path and file name
IN_PATH = r'Z:\Trumann\Renishaw\20210304 PVSe33'
FNAME = r'\PVSe33.3_2 Glass side PL map0.wdf'

# import wdf file
filename = IN_PATH+FNAME
reader = WDFReader(filename)
reader.print_info()

# get x-axis of spectral data
    # keep in mind the units you specified for the measurement
    # here, energy (eV) was specified and would be the x-axis of the spectrum
energy = reader.xdata

# get the spectral data 
    # if .wdf file is a map, 'spectra' is 3D (y_pixel, x_pixel, intensity)
    # if .wdf file is spot, 'spectra' is 1D (intensity)
    # if .wdf file is aborted map, 'spectra' is 2D (y_pix*x_pix, intensity)
spectra = reader.spectra

# check the spectrum of the first pixel
    # this will not work if the map was aborted
first_pixel = spectra[0,0,:]
plt.plot(energy, first_pixel)

#%%
'''
often the PL or Raman spectra can have a significant background

this cell uses the 'arpls' algorithm to subtract this background

in the case of a map, the average spectrum of the map is calculated here
and then the background subraction is performed
    in princple, the backgorund subtraction could be done per pixel,
    but this is in development (as of 20210304)

the user will need to try different combinations of 'lam' and 'ratio' to get
the best result for a set of spectra
    'lam' should be veried logorithmically (e.g. 1E4-1E7)
    'ratio' should be varied logorithmically (e.g. 0.001-0.1)
'''

import numpy as np
from scipy.sparse.linalg import spsolve
from scipy import sparse
from scipy.linalg import cholesky

def arpls(y, lam=1e4, ratio=0.05, itermax=100):
    N = len(y)
#  D = sparse.csc_matrix(np.diff(np.eye(N), 2))
    D = sparse.eye(N, format='csc')
    D = D[1:] - D[:-1]  # numpy.diff( ,2) does not work with sparse matrix. This is a workaround.
    D = D[1:] - D[:-1]

    H = lam * D.T * D
    w = np.ones(N)
    for i in range(itermax):
        W = sparse.diags(w, 0, shape=(N, N))
        WH = sparse.csc_matrix(W + H)
        C = sparse.csc_matrix(cholesky(WH.todense()))
        z = spsolve(C, spsolve(C.T, w * y))
        d = y - z
        dn = d[d < 0]
        m = np.mean(dn)
        s = np.std(dn)
        wt = 1. / (1 + np.exp(2 * (d - (2 * s - m)) / s))
        if np.linalg.norm(w - wt) / np.linalg.norm(w) < ratio:
            break
        w = wt
    return z

# calculate average spectrum from the map
z = np.shape(spectra)[2]
y = np.shape(spectra)[0]
x = np.shape(spectra)[1]
spectra_ravel = spectra.reshape((x*y),z)
z_average = np.mean(spectra_ravel, axis=0)

# check average spectrum
plt.plot(energy,z_average)

# calculate baseline 
    # try different combinations of 'lam' and 'ratio'
    # it's common to get a RuntimeWarning in this step
        # RuntimeWarning: overflow encountered in exp
    # this is usually due to the 'ratio' being too small
    # usually it will not stop the fit from converging, and is not an issue
baseline_arpls = arpls(z_average, 1e5, 0.01)

# subtract baseline from data
spectra_arpls = z_average - baseline_arpls

# check subtraction
plt.plot(energy, z_average)
plt.plot(energy,spectra_arpls)

#%%
'''
this cell fits the average, background-subtracted PL spectrum of a map
to a gaussian function

for the example provided, two peaks appear in the average, background-subtracted
spectrum

this cell fits two gaussian functions
    be sure to set the initial guesses for each peak

the amplitude, energy position, and width of each fit are in 'popt'
'''

from scipy import optimize

def gaussian_plot(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

def multi_gaussian_fit(x, *pars):
    offset = pars[0]
    A1 = pars[1];    A2 = pars[4]
    x01 = pars[2];   x02 = pars[5]
    sig1 = pars[3];  sig2 = pars[6]
    
    g1 = A1*np.exp(-(x-x01)**2/(2*sig1**2))
    g2 = A2*np.exp(-(x-x02)**2/(2*sig2**2))
    return g1 + g2 + offset

# initial fit parameter guess
    # the starting values are critical if the user wants the fit to converge
    # recommend plotting the spectrum first, and reading the values from there
    # [offset, A1, xc1, width1, A2, xc2, width2]
guess = [0, 300, 1.388, 0.009, 175, 1.371, 0.018]
popt, pcov = optimize.curve_fit(multi_gaussian_fit, energy, spectra_arpls, guess)

# plot the data with the gaussian fit
plt.plot(energy, spectra_arpls, '-', color='#1f77b4', label='data')
# plot one gaussian peak
gauss1 =  gaussian_plot(energy, popt[1], popt[2], popt[3])
plt.plot(energy, gauss1, 'g-.',label='fit1')
# plot another gaussian peak
gauss2 =  gaussian_plot(energy, popt[4], popt[5], popt[6])
plt.plot(energy, gauss2, 'm-.',label='fit2')
# plot total fit
gaussian_fits = multi_gaussian_fit(energy, *popt)
plt.plot(energy, gaussian_fits, 'r--', label='total fit')

plt.legend()
