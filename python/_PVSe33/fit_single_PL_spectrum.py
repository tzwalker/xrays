"""
coding: utf-8

tzwalker
Wed Feb  3 10:07:35 2021

this program i smeant to import and fit a single PL spectrum
from the Renishaw tool

it assumes you have exported the file as a .txt file
"""
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize
import numpy as np


def peak_in_range(spectra, wn, range_list, method="max", **params):
    """Find the max intensity of peak within range
       method can be max, min, or mean
    """
    cond = np.where((wn >= range_list[0]) & (wn <= range_list[1]))[0]
    spectra_cut = spectra[cond]
    return getattr(np, method)(spectra_cut, **params)


def gaussian(x, height, center, width, offset):
    return height*np.exp(-(x - center)**2/(2*width**2)) + offset


'''for single spectrum'''
IN_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\PL\spectra'
FNAME = r'\20210119 PVSe33.4_3SLAC PL - glass side test1.txt'
#FNAME = r'\20201105 PVSe33.3_4 PL Spot - Au side - boundary.txt'

spectrum = pd.read_csv(IN_PATH+FNAME, sep='\t', skiprows=1)
spectrum.columns = ["Wave #", "Intensity"]

data = spectrum.to_numpy()
energy = data[:,0]
intensity = data[:,1]
plt.plot(energy, intensity)

from baseline_algorithms import arpls
baseline_arpls = arpls(intensity, 1e5, 0.1)
intensity_arpls = intensity - baseline_arpls
plt.plot(energy, intensity_arpls)


# =============================================================================
# data_base = data[:,1] - np.min(data[:,1] , keepdims=True)
# peaks_a = peak_in_range(data_base, data[:,0], [1.37, 1.43])
# =============================================================================


# gaussian fit try 1
popt, _ = optimize.curve_fit(gaussian, energy, intensity_arpls)
plt.plot(energy, intensity_arpls)
plt.plot(energy, gaussian(energy, *popt))

# multi-gaussian fit 2
#https://stackoverflow.com/questions/54851012/fitting-data-with-multiple-gaussian-profiles-in-python
def gaussian2(x, A, x0, sig):
    return A*np.exp(-(x-x0)**2/(2*sig**2))

def multi_gaussian(x, *pars):
    offset = pars[0]
    g1 = gaussian2(x, pars[1], pars[2], pars[3])
    g2 = gaussian2(x, pars[4], pars[5], pars[6])
    return g1 + g2 + offset

# Initial guesses for the parameters to fit:
# 3 amplitudes, means and standard deviations plus a continuum offset.
guess = [8.5, 2525, 1.39, 0.013, 500, 1.37, 0.01]
popt, pcov = optimize.curve_fit(multi_gaussian, energy, intensity_arpls, guess)
plt.plot(energy, intensity_arpls, label='Data')
g1_plus_g2 = multi_gaussian(energy, *popt)
plt.plot(energy, g1_plus_g2, 'r--', label='Fit')
plt.legend()

