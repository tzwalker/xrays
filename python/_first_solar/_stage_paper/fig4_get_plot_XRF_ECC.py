# -*- coding: utf-8 -*-
"""

Trumann
Tue Mar 22 10:38:07 2022

run first cell in "opencv_ECC_register.py" before this program

this program plots the registration results for the stage paper

i want to add a figure that shows the XBIC registration lineouts to the
main manuscript

and the lineouts of the XRF channels in the supporting information

these cells are for plotting XRF data at two temperatures
normalized to the US_IC
    the XRF data were fit by Barry Lai
    
"""

import cv2
import numpy as np
import pandas as pd

im1_path = r'Z:\Trumann\Fitted_Sychrotron_Data\2019_06_2IDD_FS3_operando\BL_fit_202002\output\combined_ASCII_2idd_0323.h5.csv'
im2_path = r'Z:\Trumann\Fitted_Sychrotron_Data\2019_06_2IDD_FS3_operando\BL_fit_202002\output\combined_ASCII_2idd_0339.h5.csv'
im1_data = pd.read_csv(im1_path, skiprows=1)
im2_data = pd.read_csv(im2_path, skiprows=1)

# Read images of interest
columns = [" US_IC", " Se", " Cd_L", " Te_L", " Au_L"]

i = ' y pixel no'
j = 'x pixel no'
imgs1 = [im1_data.pivot(index=i, columns=j, values=c) for c in columns]
imgs2 = [im2_data.pivot(index=i, columns=j, values=c) for c in columns]


# Get 20C XRF images
xrf20 = [np.array(df) for df in imgs1]
xrf20 = [arr[:,:-2] for arr in xrf20]
xrf20 = xrf20[1:6]

# Get 80C XRF images
xrf80 = [np.array(df) for df in imgs2]
xrf80 = [arr[:,:-2] for arr in xrf80]
xrf80 = xrf80[1:6]

# Convert 80C map to float32
xrf80_F32 = [arr.astype("float32") for arr in xrf80]

# Apply warp matrix to 80C map
aligned80 = [cv2.warpPerspective (arr, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP) for arr in xrf80_F32]

# Crop aligned area
xrf20_crop = [arr[30:190,20:] for arr in xrf20]
xrf80_crop = [arr[30:190,20:] for arr in aligned80]

#%%
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.150):.0f}'

fig, ((ax1,ax2,ax3,ax4),(ax5,ax6,ax7,ax8)) = plt.subplots(2,4,squeeze=True,)

ax1.imshow(xrf20_crop[1], vmin=0.00,vmax=15.0, origin='lower', cmap="Blues_r")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))

ax2.imshow(xrf20_crop[2], vmin=0.00,vmax=15.0, origin='lower', cmap="Purples_r")
ax3.imshow(xrf20_crop[0], vmin=0.70,vmax=1.40, origin='lower', cmap="Greys_r")
ax4.imshow(xrf20_crop[3], vmin=9.00,vmax=15.0, origin='lower', cmap="copper")

ax5.imshow(xrf80_crop[1], vmin=0.00,vmax=15.0, origin='lower', cmap="Blues_r")
ax5.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax5.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax6.imshow(xrf80_crop[2], vmin=0.00,vmax=15.0, origin='lower', cmap="Purples_r")
ax6.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax7.imshow(xrf80_crop[0], vmin=0.70,vmax=1.40, origin='lower', cmap="Greys_r")
ax7.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax8.imshow(xrf80_crop[3], vmin=9.00,vmax=15.0, origin='lower', cmap="copper")
ax8.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))

for ax in fig.get_axes():
    ax.label_outer()
    
fig.tight_layout(h_pad=-10)
#%%
plt.figure()
plt.imshow(xrf20_crop[3])
plt.figure()
plt.imshow(xrf80_crop[3])

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