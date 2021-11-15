# -*- coding: utf-8 -*-
"""
tzwalker
Sat Nov  13 17:12:40 2021
coding: utf-8

this program imports the data from one fit

i just need the XRF normalized to the US_IC
for the stage paper

everything is hard coded, including the alignment of the XRF maps between
the two scans; i have the translation coordinates from the SIFT alignment
in 'XBIC-translate'

use the other directory (ug_per_cm2_XRF) for aligning all the data

for plotting reference, pixel step was 

20pixels = 3um
67pix = 10um

"""
import sys
sys.path.append(r'C:\Users\triton\xrays\python\_first_solar')

from class_ascii_Sample import Sample

ASCII_PATH = r'C:\Users\triton\FS3_2019_06_operando\BL_fit_202002\output'

# create sample objects
FS3 = Sample()

# define stack and scans of each sample, upstream layer first
FS3.stack = {'Au':   [19.3, 100E-7], 
                 'CdTe': [5.85, 5E-4],
                 'Se': [4.82, 100E-7],
                 'SnO2': [100E-7]}
FS3.scans = [323,339]


# channels to import from ASCII
channels = [' US_IC', ' Se', ' Cd_L', ' Te_L', ' Au_L']


# uncomment this line to import maps without XBIC converted to ampere
FS3.stage_paper_XRF(ASCII_PATH, channels)

#%%

'''this cell is from XBIC-translate-and-deltas.py'''

from skimage.transform import SimilarityTransform, warp
import numpy as np

### start with map with largest offset
img2 = FS3.scan339
SHFT2 = SimilarityTransform(translation=(-11, -8))
# shift (translate) all imported channels
shifted_channels2 = []
for i, channel in enumerate(channels):
    IMG2_SHIFT = warp(img2[i,:,:-2], SHFT2)
    shifted_channels2.append(IMG2_SHIFT)
# store shifted channels
shifted_channels2 = np.array(shifted_channels2)

### make mask that defines area to crop
mask = IMG2_SHIFT!=0
mask = mask.astype(int)

### mask the map used as alignemnt reference
img0 = FS3.scan323
shifted_channels0 = []
for i, channel in enumerate(channels):
    # mask the translated maps
    IMG0_MSK = img0[i,:,:-2]*mask
    shifted_channels0.append(IMG0_MSK)
shifted_channels0 = np.array(shifted_channels0) 

### store aligned and masked images
aligned = [shifted_channels0,
           shifted_channels2]

### remove zeros according to indices of map with largest offsets
# in the XBIC images, the last 100C map is cut off both above and below, 
    # from row indices 19:176
aligned_crop = [arr[:,8:,11:] for arr in aligned]

#%%
'''
this cell is for plotting the XRF data normalized to the US_IC
the US_IC and XRF came from the same fitted data file fit by BLai


Cd range - vmin=0.00,vmax=15.0
Te range - vmin=0.00,vmax=15.0
Se range - vmin=0.70,vmax=1.50

'''
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker

# specify index of scan, cmap, and fname
# 0 is scan323, 1 is scan339
idx = 1

channel = 4

T_list = ['20C','80C']
scans1 = [323,339]

img = aligned_crop[idx][channel,:,:]

fig, ax = plt.subplots(figsize=(1.8,3.6))

im = ax.imshow(img, cmap = 'copper', origin='lower',vmin=9,vmax=15.0)

# format tick labels (convert to um)
fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.150):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))

# plot some arbitrary points at same locations
plt.scatter([50,200,75], [120,60,25], facecolors='none', edgecolors='black', marker='o', s=10)


ax.set_xlabel("X (um)", size=8)
ax.xaxis.set_tick_params(labelsize=8)

ax.set_ylabel("Y (um)", size=8)
ax.yaxis.set_tick_params(labelsize=8)

divider = make_axes_locatable(ax)

cax = divider.new_vertical(size='5%', pad=0.1)
fig.add_axes(cax)
cbar = fig.colorbar(im, cax=cax, orientation='horizontal')
cbar.set_label('Au XRF Intensity (arb. units)', rotation=0, fontsize=8)
cbar.ax.locator_params(nbins=4)
cbar.ax.tick_params(labelsize=8)
cax.xaxis.set_label_position('top')
cax.xaxis.set_ticks_position('top')



OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\0_stage design\20211114 figures_v2\figure4 materials'
FNAME = r'\FS3_{TEMP}_scan{SCAN}_{CHAN}.eps'.format(TEMP=T_list[idx], SCAN=scans1[idx], CHAN=channels[channel])
print(FNAME)
#plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)

