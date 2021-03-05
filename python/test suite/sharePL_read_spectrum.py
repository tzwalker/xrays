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
FNAME = r'\PVSe33.3_2 Au side PL spectrum0.wdf'

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
spectra = reader.spectra

# check the spectrum
plt.plot(energy, spectra)

#%%
'''
often the PL or Raman spectra can have a significant background

this cell uses the 'arpls' algorithm to subtract this background

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

# calculate baseline 
    # try different combinations of 'lam' and 'ratio'
    # it's common to get a RuntimeWarning in this step
        # RuntimeWarning: overflow encountered in exp
    # this is usually due to the 'ratio' being too small
    # usually it will not stop the fit from converging, and is not an issue
baseline_arpls = arpls(spectra, 1e7, 0.25)

# subtract baseline from data
spectra_arpls = spectra - baseline_arpls

# check subtraction
plt.plot(energy, spectra)
plt.plot(energy,spectra_arpls)

#%%
'''
this cell fits the peak of a background-subtracted PL spectrum
to a gaussian function

the amplitude, energy position, and width of the fit are in the vairable 'popt'
'''

from scipy import optimize

def gaussian_plot(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

def gaussian_fit(x,*pars):
    offset = pars[0]
    A = pars[1]
    x0 = pars[2]
    sig = pars[3]
    g1 = A*np.exp(-(x-x0)**2/(2*sig**2))
    return g1 + offset

# initial fit parameter guess
    # the starting values are critical if the user wants the fit to converge
    # recommend plotting the spectrum first, and reading the values from there
    # [offset, A1, xc1, width1]
guess = [0, 3000, 1.50, 0.01]
popt, pcov = optimize.curve_fit(gaussian_fit, energy, spectra_arpls, guess)

# plot the data with the gaussian fit
plt.plot(energy, spectra_arpls, '-', color='#1f77b4', label='data')
gauss1 =  gaussian_plot(energy, popt[1], popt[2], popt[3])
plt.plot(energy, gauss1, 'r--',label='fit')
plt.xlabel('energy (eV)')
plt.ylabel('intensity (a.u.)')
plt.legend()
