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
plt.plot(share[:,1], 'k', label='original')

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
plt.plot(baseline_subtracted, 'r', label='als')

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
#plt.plot(intensity_rubber, 'b', label='rubberband')

# peakutils approach
import peakutils
baseline_peakutils = peakutils.baseline(share[:,1])
intensity_peakutils = share[:,1] - baseline_peakutils
plt.plot(intensity_peakutils, 'g', label='peakutils')

# arpls approach
from scipy.linalg import cholesky
def arpls(y, lam=1e4, ratio=0.05, itermax=100):
    r"""
    Baseline correction using asymmetrically
    reweighted penalized least squares smoothing
    Sung-June Baek, Aaron Park, Young-Jin Ahna and Jaebum Choo,
    Analyst, 2015, 140, 250 (2015)
    Inputs:
        y:
            input data (i.e. chromatogram of spectrum)
        lam:
            parameter that can be adjusted by user. The larger lambda is,
            the smoother the resulting background, z
        ratio:
            wheighting deviations: 0 < ratio < 1, smaller values allow less negative values
        itermax:
            number of iterations to perform
    Output:
        the fitted background vector
    """
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

baseline = baseline_als(share[:,1], 1E6, 0.001)
baseline_subtracted = share[:,1] - baseline
plt.plot(baseline_subtracted, 'r', label='als')

baseline_arpls = arpls(share[:,1], 1e5, 0.1)
intensity_arpls = share[:,1] - baseline_arpls
plt.plot(intensity_arpls, label='arpls')

plt.legend()
