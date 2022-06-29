"""
coding: utf-8

tzwalker
Thu Feb  4 10:47:19 2021

this program is used to import and process Raman map data

this program uses the packages provided here:
    https://github.com/alchem0x2A/py-wdf-reader

Raman CdTe peaks of interest are 127,141,167,275,365cm-1
 
relevant data files can be found here
'Z:\Trumann\Renishaw\PVSe33 measurement overview.txt'
"""

from renishawWiRE import WDFReader
import numpy as np
 
IN_PATH = r'Z:\Trumann\Renishaw\20210213 PVSe33 redo 2'
FNAME = r'\PVSe33.3_2 Au Side_raman_map0.wdf'

# import wdf file
filename = IN_PATH+FNAME
reader = WDFReader(filename)
reader.print_info()

# get x-axis of spectral data
    # keep in mind the units you specified for the measurement
    # here the measurement was made using shift (cm-1) as the x-axis
shift = reader.xdata

# get the spectral data from the map; has form (y_pixel, x_pixel, intensity)
spectra = reader.spectra

#%%
'''this cell averages the spectra in each pixel, among other things'''
from scipy.stats import iqr
from sklearn.preprocessing import normalize

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
norm_std = np.std(spectra_norm, axis=0)
norm_q = iqr(spectra_norm, axis=0, rng=(25,75))

x = np.vstack((norm_avg,norm_std,norm_q)).T

#%%
'''
this cell takes the raman map
finds bin closest to the wavenumber shift specified by the user
records and stores intensity
'''
# reshape spectra out of map form for convenience
z = np.shape(spectra)[2]
y = np.shape(spectra)[0]
x = np.shape(spectra)[1]
spectra_ravel = spectra.reshape((x*y),z)

# specify the x-axis value you wish to plot
    # here the CdTe peaks of interest are 127,141,167,275,365cm-1
user_shift = 141

# find the value in the x-axis that is closest to the specified x-axis value
E_idx = (np.abs(shift - user_shift)).argmin()

user_intensities = spectra_ravel[:,E_idx]


OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\Raman'
OUT_FILE = r'141 peak intensities - 20210213 PVSe33.3_2 Au side_raman_map0.csv'
OUT = OUT_PATH + OUT_FILE
#np.savetxt(OUT, user_intensities, delimiter=',')
