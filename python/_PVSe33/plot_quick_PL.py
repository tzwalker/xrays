"""
coding: utf-8

tzwalker
Fri Jan 29 19:11:30 2021

this program is meant to process the .txt PL and Raman data 
    from the Renishaw software
    
"""
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def gaussian(x, y0, amplitude, mean, stddev):
    return y0 + amplitude * np.exp(-((x - mean) / 4 / stddev)**2)

def baseline(y, deg=None, max_it=None, tol=None):
    """
    Computes the baseline of a given data.

    Iteratively performs a polynomial fitting in the data to detect its
    baseline. At every iteration, the fitting weights on the regions with
    peaks are reduced to identify the baseline only.

    Parameters
    ----------
    y : ndarray
        Data to detect the baseline.
    deg : int (default: 3)
        Degree of the polynomial that will estimate the data baseline. A low
        degree may fail to detect all the baseline present, while a high
        degree may make the data too oscillatory, especially at the edges.
    max_it : int (default: 100)
        Maximum number of iterations to perform.
    tol : float (default: 1e-3)
        Tolerance to use when comparing the difference between the current
        fit coefficients and the ones from the last iteration. The iteration
    procedure will stop when the difference between them is lower than
    *tol*.

    Returns
    -------
    ndarray
    Array with the baseline amplitude for every original point in *y*
    """
    import math
    import scipy.linalg as LA


    # for not repeating ourselves in `envelope`
    if deg is None: deg = 3
    if max_it is None: max_it = 100
    if tol is None: tol = 1e-3

    order = deg + 1
    coeffs = np.ones(order)

    # try to avoid numerical issues
    cond = math.pow(y.max(), 1. / order)
    x = np.linspace(0., cond, y.size)
    base = y.copy()

    vander = np.vander(x, order)
    vander_pinv = LA.pinv2(vander)

    for _ in range(max_it):
        coeffs_new = np.dot(vander_pinv, y)

        if LA.norm(coeffs_new - coeffs) / LA.norm(coeffs) < tol:
            break

        coeffs = coeffs_new
        base = np.dot(vander, coeffs)
        y = np.minimum(y, base)

    return base

import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy import optimize
import matplotlib.pyplot as plt
from astropy import modeling

IN_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\PL'
FNAME = r'\20210119 PVSe33.4_3SLAC PL MAP - Au side test2.txt'

data = pd.read_csv(IN_PATH+FNAME, sep='\t', skiprows=1)
data.columns = ["X", "Y", "Wave #", "Intensity"]

# create dictionary where each pixel is an entry
# from StackOverflow solution:
    # https://stackoverflow.com/questions/65969561/how-do-i-convert-mapped-data-to-dictionary-where-each-xy-coordinate-contains-a/65969669#65969669
map_dict = data.set_index(['X', 'Y']).agg(list, 1).groupby(level=(0,1)).agg(list).transform(np.array).to_dict()

new_dict = {}
for pixel in map_dict:
    px_spec = map_dict[pixel]
    px_spec_avg = moving_average(px_spec[:,1], 5)
    amp = np.max(px_spec_avg)
    new_dict[pixel] = amp
# try baseline subtraction (from Brad's Renishaw-Reniawesome)
base = baseline(px_spec[:,1], 4)
plt.plot(base)
base_sub = px_spec[:,1]-base
plt.plot(base_sub)

# gaussian fit try 1
popt, _ = optimize.curve_fit(gaussian, px_spec[:,0], px_spec[:,1])
plt.plot(px_spec[:,0], px_spec[:,1])
plt.plot(px_spec[:,0], gaussian(px_spec[:,0], *popt))

# gaussian fit try 2
mean,std=norm.fit(px_spec[:,1])
px_fit = norm.pdf(px_spec[:,0], mean, std)
plt.plot(px_spec[:,0], px_spec[:,1])
plt.plot(px_spec[:,0], px_fit)

# gaussian fit try 3
fitter = modeling.fitting.LevMarLSQFitter()
model = modeling.models.Gaussian1D()   # depending on the data you need to give some initial values
fitted_model = fitter(model, px_spec[:,0], px_spec[:,1])
plt.plot(px_spec[:,0], px_spec[:,1])
plt.plot(px_spec[:,0], fitted_model(px_spec[:,0]))

#pixel_spectrum_arr_5avg = moving_average(pixel_spectrum_arr[:,1], 5)

# copy dictionary key
# set value of copy dictionary key to max amplitude
# store this key-value pair in new dictionary

#print(np.shape(pixel_spectrum))
    

# =============================================================================
# '''for spectra of different pixels of PL map'''
# # isolate data of pixel with index, 'n'
#     # i looked in the txt file and found the index where X changed
# n = 20
# row_idxLo = 511*n+n
# row_idxHi = 511*(n+1)+n
# data_pixel01 = data.iloc[row_idxLo:row_idxHi]
# 
# # extract spectrum
# data_pixel01_spectrum = data_pixel01[data_pixel01.columns[-2:]]
# 
# import matplotlib.pyplot as plt
# plt.plot(data_pixel01_spectrum["Wave #"], data_pixel01_spectrum["Intensity"])
# 
# =============================================================================
#%%
'''for single spectrum'''
import pandas as pd
import matplotlib.pyplot as plt

IN_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\PL'
FNAME = r'\20210119 PVSe33.4_3SLAC PL - glass side test1.txt'

data = pd.read_csv(IN_PATH+FNAME, sep='\t', skiprows=1)
data.columns = ["Wave #", "Intensity"]

plt.plot(data["Wave #"], data["Intensity"])