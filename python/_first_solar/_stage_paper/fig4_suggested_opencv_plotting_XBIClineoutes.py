# -*- coding: utf-8 -*-
"""

Trumann
Tue Mar 22 10:38:07 2022

run first cell in "opencv_ECC_register.py" before this program

this program plots the registration results for the stage paper

i want to add a figure that shows the XBIC registration lineouts to the
main manuscript

and the lineouts of the XRF channels in the supporting information

"""

import cv2
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Normalize XBIC to upstream_ion chamber
xbic = np.array(imgs1[1])
us_ic = np.array(imgs1[0])
xbic20 = xbic[:,:-2] / us_ic[:,:-2]

xbic = np.array(imgs2[1])
us_ic = np.array(imgs2[0])
xbic80 = xbic[:,:-2] / us_ic[:,:-2]

# Convert 80C map to float32
im2_F32 = xbic80.astype("float32")

# Apply warp matrix to 80C map
im2_aligned = cv2.warpPerspective (im2_F32, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

# Crop aligned area
xbic20_crop = xbic20[30:190,20:]
xbic80_crop = im2_aligned[30:190,20:]

# Get lines in 20C cropped area
lineout_20x = xbic20_crop[105,:]
lineout_20y = xbic20_crop[:,200]

x = np.array(list(range(0,len(lineout_20x))))
y = np.array(list(range(0,len(lineout_20y))))

# Get lines in 80C cropped area
lineout_80x = xbic80_crop[105,:]
lineout_80y = xbic80_crop[:,200]

x1 = np.array(list(range(0,len(lineout_80x))))
y1 = np.array(list(range(0,len(lineout_80y))))
#%%

# From C:\Users\Trumann\xrays\python\_NBL3\XBIC-XBIV-scatter-hex-fit.py
# setup histograms in margins #

# Plot 20C lineouts
fig = plt.figure(constrained_layout=True)

grid = GridSpec(3, 3, figure=fig)
main_ax = fig.add_subplot(grid[1:,:2])
hline = fig.add_subplot(grid[0, :-1], xticklabels=[], xticks=[])
vline = fig.add_subplot(grid[1:, -1], yticklabels=[], yticks=[])

# plot 
im = main_ax.imshow(xbic20_crop, cmap='afmhot', aspect='auto', vmin=1.6,vmax=2.2)
main_ax.axhline(y=105, linestyle='--', linewidth=0.5, color='w')
main_ax.axvline(x=200, linestyle='--', linewidth=0.5, color='w')

fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.150):.0f}'
main_ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
main_ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
main_ax.invert_yaxis()
main_ax.set_xlabel("X (um)")
main_ax.set_ylabel("Y (um)")
cbar = fig.colorbar(im)
cbar.set_label("XBIC (arb. unit)")

hline.plot(x,lineout_20x, linewidth=1, color='black')
hline.set_ylim([1.6,2.2])
hline.set_xlim([0,279])
hline.set_ylabel("XBIC (arb. unit)")

vline.plot(lineout_20y,y, linewidth=1, color='black')
vline.set_xlim([1.6,2.2])
vline.set_ylim([0,160])
vline.set_xlabel("XBIC (arb. unit)")

# Plot 80C lineouts
fig = plt.figure(constrained_layout=True)

grid = GridSpec(3, 3, figure=fig)
main_ax = fig.add_subplot(grid[1:,:2])
hline = fig.add_subplot(grid[0, :-1], xticklabels=[], xticks=[])
vline = fig.add_subplot(grid[1:, -1], yticklabels=[], yticks=[])

im = main_ax.imshow(xbic80_crop, cmap='afmhot', aspect='auto', vmin=1.6,vmax=2.2)
main_ax.axhline(y=105, linestyle='--', linewidth=0.5, color='r')
main_ax.axvline(x=200, linestyle='--', linewidth=0.5, color='r')

fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.150):.0f}'
main_ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
main_ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
main_ax.invert_yaxis()
main_ax.set_xlabel("X (um)")
main_ax.set_ylabel("Y (um)")
cbar = fig.colorbar(im)
cbar.set_label("XBIC (arb. unit)")

hline.plot(x,lineout_20x, linewidth=1, color='black',label="20C")
hline.set_ylim([1.6,2.2])
hline.set_xlim([0,279])
hline.set_ylabel("XBIC (arb. unit)")

hline.plot(x,lineout_80x, linewidth=1, color='red',label="80C")
hline.set_ylim([1.6,2.2])
hline.set_xlim([0,279])
hline.set_ylabel("XBIC (arb. unit)")
hline.legend()

vline.plot(lineout_20y,y, linewidth=1, color='black',label="20C")
vline.set_xlim([1.6,2.2])
vline.set_ylim([0,160])
vline.set_xlabel("XBIC (arb. unit)")

vline.plot(lineout_80y,y1, linewidth=1, color='red',label="80C")
vline.set_xlim([1.6,2.2])
vline.set_ylim([0,160])
vline.set_xlabel("XBIC (arb. unit)")
vline.legend()