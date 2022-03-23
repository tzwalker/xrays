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
# columns clipped to = [" Se", " Cd_L", " Te_L", " Au_L"] #!!

# Get 80C XRF images
xrf80 = [np.array(df) for df in imgs2]
xrf80 = [arr[:,:-2] for arr in xrf80]
xrf80 = xrf80[1:6]
# columns clipped to = [" Se", " Cd_L", " Te_L", " Au_L"] #!!

# Convert 80C map to float32
xrf80_F32 = [arr.astype("float32") for arr in xrf80]

# Apply warp matrix to 80C map
aligned80 = [cv2.warpPerspective (arr, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP) for arr in xrf80_F32]

# Crop aligned area
xrf20_crop = [arr[30:190,20:] for arr in xrf20]
xrf80_crop = [arr[30:190,20:] for arr in aligned80]

#%%
"""this cell was used to replot the XRF data aligned using XBIC warp matrix"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable

fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.150):.0f}'

fig, ((ax1,ax2,ax3,ax4),(ax5,ax6,ax7,ax8)) = plt.subplots(2,4,squeeze=True,sharex=True,sharey=True)

im1 = ax1.imshow(xrf20_crop[1], vmin=0.00,vmax=15.0, origin='lower', cmap="Blues_r")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax1.set_ylabel("Y (\u03BCm)", size=8)
ax1.yaxis.set_tick_params(labelsize=8)
ax1.xaxis.set_major_locator(plt.MaxNLocator(3))
ax1.set_yticks([-40., 0., 54., 100., 147.]) # to match XBIC ticks
#ax1.yaxis.set_major_locator(plt.MaxNLocator(4))

im2 = ax2.imshow(xrf20_crop[2], vmin=0.00,vmax=15.0, origin='lower', cmap="Purples_r")
im3 = ax3.imshow(xrf20_crop[0], vmin=0.70,vmax=1.40, origin='lower', cmap="Greys_r")
im4 = ax4.imshow(xrf20_crop[3], vmin=9.00,vmax=15.0, origin='lower', cmap="copper")

ax5.imshow(xrf80_crop[1], vmin=0.00,vmax=15.0, origin='lower', cmap="Blues_r")
ax5.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax5.set_xlabel("X (\u03BCm)", size=8)
ax5.xaxis.set_tick_params(labelsize=8)
ax5.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax5.set_ylabel("Y (\u03BCm)", size=8)
ax5.yaxis.set_tick_params(labelsize=8)

ax6.imshow(xrf80_crop[2], vmin=0.00,vmax=15.0, origin='lower', cmap="Purples_r")
ax6.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax6.set_xlabel("X (\u03BCm)", size=8)
ax6.xaxis.set_tick_params(labelsize=8)

ax7.imshow(xrf80_crop[0], vmin=0.70,vmax=1.40, origin='lower', cmap="Greys_r")
ax7.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax7.set_xlabel("X (\u03BCm)", size=8)
ax7.xaxis.set_tick_params(labelsize=8)

ax8.imshow(xrf80_crop[3], vmin=9.00,vmax=15.0, origin='lower', cmap="copper")
ax8.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax8.set_xlabel("X (\u03BCm)", size=8)
ax8.xaxis.set_tick_params(labelsize=8)

for ax in fig.get_axes():
    ax.label_outer()
    
fig.tight_layout(h_pad=-8)

# Add Cd colorbar
divider = make_axes_locatable(ax1)
cax = divider.new_vertical(size='5%', pad=0.1)
fig.add_axes(cax)
cbar = fig.colorbar(im1, cax=cax, orientation='horizontal')
cbar_name = 'Cd XRF (arb. units)'
cbar.set_label(cbar_name, rotation=0, fontsize=8)
cbar.ax.locator_params(nbins=4)
cbar.ax.tick_params(labelsize=8)
cax.xaxis.set_label_position('top')
cax.xaxis.set_ticks_position('top')
# Add Te colorbar
divider = make_axes_locatable(ax2)
cax = divider.new_vertical(size='5%', pad=0.1)
fig.add_axes(cax)
cbar = fig.colorbar(im2, cax=cax, orientation='horizontal')
cbar_name = 'Te XRF (arb. units)'
cbar.set_label(cbar_name, rotation=0, fontsize=8)
cbar.ax.locator_params(nbins=4)
cbar.ax.tick_params(labelsize=8)
cax.xaxis.set_label_position('top')
cax.xaxis.set_ticks_position('top')
# Add Se colorbar
divider = make_axes_locatable(ax3)
cax = divider.new_vertical(size='5%', pad=0.1)
fig.add_axes(cax)
cbar = fig.colorbar(im3, cax=cax, orientation='horizontal')
cbar_name = 'Se XRF (arb. units)'
cbar.set_label(cbar_name, rotation=0, fontsize=8)
cbar.ax.locator_params(nbins=4)
cbar.ax.tick_params(labelsize=8)
cax.xaxis.set_label_position('top')
cax.xaxis.set_ticks_position('top')
# Add Au colorbar
divider = make_axes_locatable(ax4)
cax = divider.new_vertical(size='5%', pad=0.1)
fig.add_axes(cax)
cbar = fig.colorbar(im4, cax=cax, orientation='horizontal')
cbar_name = 'Au XRF (arb. units)'
cbar.set_label(cbar_name, rotation=0, fontsize=8)
cbar.ax.locator_params(nbins=4)
cbar.ax.tick_params(labelsize=8)
cax.xaxis.set_label_position('top')
cax.xaxis.set_ticks_position('top')

OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\0_stage design\20220322 figures_v3\figure5 materials'
FNAME = r'\fig5_XRF_from_ECC2.eps'
#print(FNAME)
#plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)

#%%
"""this cell was used to get and plot the x lineouts"""

fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
fmtr_y = ["Se (arb. unit)","Cd (arb. unit)","Te (arb. unit)","Au (arb. unit)"]
ylims = [[0.8,2.0],[3,15],[3,15],[9,15]]

fig, axes = plt.subplots(4,1,sharex=True,figsize=((3,5)))

# Plot xlines
for map1, map2, ax, unit,span in zip(xrf20_crop,xrf80_crop,axes,fmtr_y,ylims):
    # Get lines in 20C cropped area
    lineout_20x = map1[105,:]
    
    # Get lines in 80C cropped area
    lineout_80x = map2[105,:]

    ax.plot(lineout_20x, label="20\u00B0C",color='k',linewidth=0.5)
    ax.plot(lineout_80x, label="80\u00B0C",color='r',linewidth=0.5)

    ax.set_ylabel(unit, size=8)
    ax.set_ylim(span)
    ax.yaxis.set_tick_params(labelsize=8,direction="in",tick2On=True)
    
    ax.xaxis.set_tick_params(labelsize=8,direction="in",tick2On=True)
  
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.set_xlabel("X (\u03BCm)", size=8)
ax.xaxis.set_tick_params(labelsize=8,direction="in")
axes[0].legend(fontsize=8,loc=2)

OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\0_stage design\supplementary\figures'
FNAME = r'\XRF_xLineouts.png'
#print(FNAME)
plt.savefig(OUT_PATH+FNAME, format='png', dpi=300, bbox_inches='tight', pad_inches = 0)

#%%
"""this cell was used to get and plot the y lineouts"""

fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
fmtr_y = ["Se (arb. unit)","Cd (arb. unit)","Te (arb. unit)","Au (arb. unit)"]
ylims = [[0.8,2.0],[3,15],[3,15],[9,15]]

fig, axes = plt.subplots(4,1,sharex=True,figsize=((3,5)))

# Plot ylines
for map1, map2, ax, unit,span in zip(xrf20_crop,xrf80_crop,axes,fmtr_y,ylims):
    # Get lines in 20C cropped area
    lineout_20y = map1[:,200]
    
    # Get lines in 80C cropped area
    lineout_80y = map2[:,200]

    ax.plot(lineout_20y, label="20\u00B0C",color='k',linewidth=0.5)
    ax.plot(lineout_80y, label="80\u00B0C",color='r',linewidth=0.5)

    ax.set_ylabel(unit, size=8)
    ax.set_ylim(span)
    ax.yaxis.set_tick_params(labelsize=8,direction="in",tick2On=True)
    
    ax.xaxis.set_tick_params(labelsize=8,direction="in",tick2On=True)
  
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.set_xlabel("Y (\u03BCm)", size=8)
ax.xaxis.set_tick_params(labelsize=8)
axes[0].legend(fontsize=8,loc=2)

OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\0_stage design\supplementary\figures'
FNAME = r'\XRF_yLineouts.png'
#print(FNAME)
plt.savefig(OUT_PATH+FNAME, format='png', dpi=300, bbox_inches='tight', pad_inches = 0)