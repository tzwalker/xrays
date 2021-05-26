"""
coding: utf-8

tzwalker
Wed May 19 11:56:31 2021

plots 3d projection of xrf or xbic data

before running this program, the maps were blurred using a separate program
    gaussian filter (sigma=1)

"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
import numpy as np
from scipy.ndimage.filters import gaussian_filter

def cm2inch(*tupl):
    inch = 2.54
    if type(tupl[0]) == tuple:
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

MAP_TYPE = 3
xrf_data = NBL33.scan264[MAP_TYPE,:,:-2]
xrf_data_plot = xrf_data.copy()
xrf_data_plot = xrf_data_plot.T
 
if MAP_TYPE == 0:
    data1 = xrf_data_plot.copy()
    data1 = data1*1e8
    colors = 'inferno'
    units = 'X-ray Beam Induced Current (nA)'
    lower_limit = 0.25
    upper_limit = 1

if MAP_TYPE == 1:
    data1 = xrf_data_plot.copy()
    data1 = gaussian_filter(data1, sigma=1)
    colors = 'Oranges_r'
    units = 'Cu XRF (cts/s)'
    lower_limit = 1000
    upper_limit = 4000
    
if MAP_TYPE == 3:
    data1 = xrf_data_plot.copy()
    data1 = gaussian_filter(data1, sigma=1)
    colors = 'bone'
    units = 'Te XRF (cts/s)'
    lower_limit = 0
    upper_limit = 1500

left_right = 25
up_down = 75
label_sizes = 14
SAVE = 1
OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\Cu in CdTe - publication materials'
FNAME = r'\graphical_abstract2_NBL33_scan264_Te.eps'

# Create figure and add axis
fig = plt.figure(figsize=(8,5))
ax = plt.subplot(111, projection='3d')

# Remove gray panes and axis grid
ax.xaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('white')
ax.yaxis.pane.fill = False
ax.yaxis.pane.set_edgecolor('white')
ax.zaxis.pane.fill = False
ax.zaxis.pane.set_edgecolor('white')
ax.grid(False)
# Remove z-axis
ax.w_zaxis.line.set_lw(0.)
ax.set_zticks([])

# Create meshgrid
    # minus 2 in x if not transposed
    # plus2 in x if transposed
    # change 2nd arg in linspace() to um bounds of map
X = np.linspace(0, 15, len(data1)+2)
Y = np.linspace(0, 15, len(data1))
X, Y = np.meshgrid(X, Y)


# Plot surface
surf = ax.plot_surface(X=X, Y=Y, Z=data1, cmap=colors, vmin=lower_limit, vmax=upper_limit, antialiased=False, linewidth=0)

# Adjust plot view
ax.view_init(elev=up_down, azim=left_right)
ax.dist=11

# Add colorbar
# position of colorbar
    # arg is [left, bottom, width, height]
cax = fig.add_axes([0.275, 0.85, 0.5, 0.03])
if MAP_TYPE == 0:
    fmt = mpl.ticker.ScalarFormatter(useMathText=True)
    fmt.set_powerlimits((1, 0))
    cb = fig.colorbar(surf, cax=cax, orientation='horizontal', format=fmt)
else:
    cb = fig.colorbar(surf, cax=cax, orientation='horizontal')
#move cbar ticks to top of cbar
cax.xaxis.set_label_position('top')
cax.xaxis.set_ticks_position('top')
#set cbar title label size
cb.set_label(units, fontsize=label_sizes, labelpad=10)
#set cbar tick label sizes
cb.ax.tick_params(labelsize=label_sizes)


# Set tick marks
ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(3.0))
ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(3.0))
# Set axis labels
ax.set_xlabel(r'$\mathregular{\mu}$m', labelpad=20, size=label_sizes)
ax.set_ylabel(r'$\mathregular{\mu}$m', labelpad=20, size=label_sizes)
#set xy tick label sizes
ax.tick_params(labelsize=label_sizes)
# Set z-limit
ax.set_zlim(lower_limit, upper_limit)

if SAVE == 1:
 plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)