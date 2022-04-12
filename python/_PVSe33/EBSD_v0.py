# -*- coding: utf-8 -*-
"""

Trumann
Wed Apr  6 08:58:33 2022

this program opens EBSD csvs from Helio Moutinho (NREL)

data were taken from email 20220405 
    R=(001)
    G=(101)
    B=(111)
    
and copied to Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tifffile

PATH_0hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD\PVSe33.3_2_rightFIB.csv"
PATH_500hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD\PVSe33.4_3_rightFIB.csv"

# import data
no_stress = pd.read_csv(PATH_0hr, skiprows=[1])

# unpack RGB values for inverted pole figure (IPF) coloring column
IPF = no_stress['IPF Coloring'].str.split(' ',expand=True)
IPF = IPF.rename(columns={0:"R",1:"G",2:"B"})

# attach unpacked RGB values
no_stress1 = pd.concat([no_stress,IPF], axis='columns')

# shape reds, greens, and blues
cr = no_stress1.pivot(index="Y",columns="X", values="R")
cg = no_stress1.pivot(index="Y",columns="X", values="G")
cb = no_stress1.pivot(index="Y",columns="X", values="B")

# convert to numpy arrays
cR = cr.to_numpy(dtype='int')
cG = cg.to_numpy(dtype='int')
cB = cb.to_numpy(dtype='int')

# merge channels
rgb = np.dstack((cR,cG,cB))  # stacks 3 h x w arrays -> h x w x 3

# transform image to match orientation of ToFSIMS
mirror1 = np.fliplr(rgb) # flips along vertical axis
mirror2 = np.flipud(mirror1) # flip along horizontal axis

# plot data
fig, ax = plt.subplots()
ax.imshow(mirror2)

# save reconstructed, transformed data cube (rgb image)
PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD\0hr_right_map.tif"
tifffile.imsave(PATH_OUT, mirror2, bigtiff=True)


#%%
# try to mask absolute green (0 255 0), (101) to avoid displaying FIB marks
color_frame = rgb.copy()

# get approximate indices of FIB marks [rows,columns,green_channel]
FIB_indices = np.where(color_frame[:75,:65,1] == 255)
color_frame[FIB_indices] = 0

#plt.imshow(color_frame)

