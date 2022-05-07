# -*- coding: utf-8 -*-
"""

Trumann
Thu Mar 31 14:06:04 2022

this program is meant to test plot TPRL maps Darius as already analyzed

data were sent from Eric 20220317

see Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts


"""

'''this cell is for the 0hr sample PVSe33.3_2'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# these files were given by Eric/Darius (email 20220317)
f = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\0423bPL2Axis_taverage.txt'
f1 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\0423bPL2Axis_tau1.txt"
f2 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\0423bPL2Axis_tau2.txt"
f3 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\0423bPL2Axis_ratio.txt"

# this file was exported using ImageJ
# see videos "Z:\Trumann\Tutorial Videos\20220331..."
f4 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\SUM_0423bPL2Axis.txt-1.txt"

t_avg = np.loadtxt(f)
tau1 = np.loadtxt(f1)
tau2 = np.loadtxt(f2)
A1_over_A2 = np.loadtxt(f3)
total_cts = np.loadtxt(f4)

fig, ax = plt.subplots()
im = ax.imshow(total_cts)
fig.colorbar(im)
# read these coordinates from drawn box in IMageJ: [28,36,28,36],[28,28,36,36]
    # then Image -> Stacks -> Plot Z-axis profile
    # saved the TRPL spectra within these pixels
    #"Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\0423bPL2Axis_spectrumROI_longDecay1.csv"
ax.add_patch(Rectangle((28, 28), 8, 8, linestyle = 'dashed', facecolor="none", ec='w', lw=1))

# read these coordinates from drawn box in IMageJ: [28,36,28,36],[28,28,36,36]
    # then Image -> Stacks -> Plot Z-axis profile
    # saved the TRPL spectra within these pixels
ax.add_patch(Rectangle((26, 37), 8, 8, linestyle = 'dashed', facecolor="none", ec='w', lw=1))

#%%
'''this cell loads the tiff images / from the datacubes'''

import tifffile

f = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\20220317_TRPL_0hr_example_0423bPL2Axis.txt.tif"

import_data = tifffile.imread(f)

total_cts1 = np.sum(data,axis=0)

