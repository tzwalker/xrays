"""
coding: utf-8

tzwalker
Wed Feb  3 10:07:35 2021

these programs are used as a testbed for fitting PL spectra from
    the Renishaw tool
the programs use either the wdf file or a text file output
"""
import pandas as pd
import matplotlib.pyplot as plt
from astropy import modeling
from scipy.stats import norm
from scipy import optimize
import numpy as np


def peak_in_range(spectra, wn, range_list, method="max", **params):
    """Find the max intensity of peak within range
       method can be max, min, or mean
    """
    cond = np.where((wn >= range_list[0]) & (wn <= range_list[1]))[0]
    spectra_cut = spectra[cond]
    return getattr(np, method)(spectra_cut, **params)



def gaussian(x, y0, amplitude, mean, stddev):
    return y0 + amplitude * np.exp(-((x - mean) / 4 / stddev)**2)


'''for single spectrum'''
IN_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\PL'
FNAME = r'\20210119 PVSe33.4_3SLAC PL - glass side test1.txt'

spectrum = pd.read_csv(IN_PATH+FNAME, sep='\t', skiprows=1)
spectrum.columns = ["Wave #", "Intensity"]

data = spectrum.to_numpy()
energy = data[:,0]
intensity = data[:,1]
#plt.plot(intensity)

share = data[::20]
plt.plot(share[:,1])

# ALS approach
from scipy import sparse
from scipy.sparse.linalg import spsolve
def baseline_als(y, lam, p, niter=10):
    L = len(y)
    D = sparse.csc_matrix(np.diff(np.eye(L), 2))
    w = np.ones(L)
    for i in range(niter):
      W = sparse.spdiags(w, 0, L, L)
      Z = W + lam * D.dot(D.transpose())
      z = spsolve(Z, w*y)
      w = p * (y > z) + (1-p) * (y < z)
    return z

baseline = baseline_als(share[:,1], 1E6, 0.001)
baseline_subtracted = share[:,1] - baseline
plt.plot(baseline_subtracted)



# rubberband approach
from scipy.spatial import ConvexHull
def rubberband(x, y):
    # Find the convex hull
    v = ConvexHull(share).vertices
    # Rotate convex hull vertices until they start from the lowest one
    v = np.roll(v, v.argmax())
    # Leave only the ascending part
    v = v[:v.argmax()]
    # Create baseline using linear interpolation between vertices
    return np.interp(x, x[v], y[v])

baseline_rubber = rubberband(share[:,0], share[:,1])
intensity_rubber = share[:,1] - baseline_rubber
plt.plot(intensity_rubber)

# peakutils approach
import peakutils
baseline_peakutils = peakutils.baseline(share[:,1])
intensity_peakutils = share[:,1] - baseline_peakutils
plt.plot(intensity_peakutils)

# =============================================================================
# intensity_adjusted = intensity[125:500]
# zero_intensity = intensity - np.min(intensity , keepdims=True)
# intensity[501:] = intensity_adjusted - baseline
# plt.plot(zero_intensity)
# =============================================================================

# =============================================================================
# data_base = data[:,1] - np.min(data[:,1] , keepdims=True)
# peaks_a = peak_in_range(data_base, data[:,0], [1.37, 1.43])
# =============================================================================

# =============================================================================
# # gaussian fit try 1
# popt, _ = optimize.curve_fit(gaussian, data[:,0], data[:,1])
# plt.plot(data[:,0], data[:,1])
# plt.plot(data[:,0], gaussian(data[:,0], *popt))
# 
# # gaussian fit try 2
# mean,std=norm.fit(data[:,1])
# px_fit = norm.pdf(data[:,0], mean, std)
# plt.plot(data[:,0], data[:,1])
# plt.plot(data[:,0], px_fit)
# 
# # gaussian fit try 3
# fitter = modeling.fitting.LevMarLSQFitter()
# # depending on the data you need to give some initial values
# model = modeling.models.Gaussian1D()   
# fitted_model = fitter(model, data[:,0], data[:,1])
# plt.plot(data[:,0], data[:,1])
# plt.plot(data[:,0], fitted_model(data[:,0]))
# =============================================================================
