# -*- coding: utf-8 -*-
"""

Trumann
Tue Jun  7 09:03:06 2022

this is meant to plot the EBSD images with the FIB marks and damage masked
    these aritfacts show up as green in RGB: [0,255,0]
    
both the 0hr and 500hr were exported using this program

"""

from skimage import io
import matplotlib.pyplot as plt
import numpy as np

PATH_EBSD = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD\500hr_right_map.tif"

# import EBSD tiff
# (x,y,color_value)
EBSD = io.imread(PATH_EBSD)

# try to mask pixels that are only green (not allpixels that have a 255 green value)
img = EBSD.copy()
#index_pos = np.where((img[:,:,0]==0) & (img[:,:,1]==255) & (img[:,:,2]==0))
#img[img[:, :, 1] == 255, 1] = 0 # close

# threshold of 255 gets rid of bright blue, relax the threshold
mask = (img != [0,254,0]).all(-1) 
img *= mask[...,None]

import matplotlib.ticker as mticker

SAVE = 0

cbar_txt_size = 11

img = np.flipud(img) # flip data for display purposes

fig, ax = plt.subplots(figsize=(2.5,2.5))

im = ax.imshow(img,origin='lower')

fmtr_x = lambda x, pos: f'{(x * 0.100):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.100):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)',size=cbar_txt_size)
ax.set_ylabel('$Y$ (μm)',size=cbar_txt_size)

if SAVE == 1:
        OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_EBSD'
        FNAME = r'\500hr_EBSD.pdf'
        plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)