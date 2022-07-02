# -*- coding: utf-8 -*-
"""

Trumann
Thu Jun 30 08:48:48 2022

this program fits the average TRPL from a 3D datacuibe
and tries to construct the TRPL lifetime histograms shared by Darius

most of the program tried to replicate what Darius is calling the
'integrated spectra' over a map

side note: total counts along the time axis doesn't really match anything
Darius has sent; it's probably not meaningful

"""

import numpy as np
import tifffile
import matplotlib.pyplot as plt


f0 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\20220317_TRPL_0hr_example_0423bPL2Axis.txt.tif"
f1 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\20220410_TRPL_500hr_example_0423ePL2Axis.txt.tif"

data0 = tifffile.imread(f0)
data1 = tifffile.imread(f1)

# calibration for x-axis see email 20220412
time = np.arange(0,262.1,0.1)

avg0 = np.mean(data0,axis=(1,2))
avg1 = np.mean(data1,axis=(1,2))

#%%
'''this cell plots average counts; color scheme matches 20210427 slide 6'''
fig, ax = plt.subplots(figsize=(4,4))

# plot 0hr average spectrum
ax.plot(time, avg0, label = '0423b_avg',color='r',linewidth=0.5)
# plot 0hr average spectrum
ax.plot(time, avg1, label = '0423e_avg',color = '#9C097E',linewidth=0.5)

# adjust axis to match
# C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\20210427 PVSe33 TRPL.pptx\slide 6
# the 500hr curve does not match what is in the slide; double check averaging
# is what this program is doing
ax.set_xlim([0,80])
ax.set_xlabel('Time (ns)')

ax.set_ylim([0.03,700])
ax.set_yscale('log')
ax.set_ylabel('Average Intensity (.)')

ax.legend()

#%%
'''check averaging is doing what i think'''
# TPRL map at 500th time step
a = data0[500,:,:]

# average of all the points in this slice
# does this match the 500th index in the avg0 array? -> YES
b = np.mean(a)

# averaging is doing what i think: 
    # takes average intensity over the 50 x 50 pixel area for each time step
#%%
'''this cell fits the average curve for the 0hr maps'''
from scipy.optimize import curve_fit

def double_exp(t, y0, A1, tau1, A2, tau2):
    return y0 + A1 * np.exp(-t / tau1) + A2 * np.exp(-t / tau2)

# Here you give the initial parameters for a,b,c which Python then iterates over
# to find the best fit
popt, pcov = curve_fit(double_exp, time, avg0, p0=(600, 1.5, 300, 14))

print(popt) # This contains your three best fit parameters
