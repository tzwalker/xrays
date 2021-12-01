"""
coding: utf-8

tzwalker
Wed Dec  1 09:53:22 2021

this is an attempt at importing and plotting AFM data

csv from "Z:\Trumann\AFM\test_AFM_export.csv"

data from "Z:\Trumann\Tutorial Videos\20211201 how to export a set of individual XANES - PVSe33 xsect.mp4"

"""

import pandas as pd

# specify path to file
file = r"C:\Users\triton\Desktop\test_AFM_export.csv"

# import data
data = pd.read_csv(file, delimiter=';', header=None)

# rename columns for convenience
column_names = ["x_um", "y_um", "z_m"]
data.columns = column_names

# shape the data according to x and y
AFM_map = data.pivot(index = "x_um", columns = "y_um", values = "z_m")

# convert Z from meter to micrometer
    # meter is the default unit exported by the NanoSurf software
AFM_map_nm = AFM_map.copy() * 1e6

#%%
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable

# construct plot object
fig, ax = plt.subplots()

# plot data with same color as NanoSurf software, and no labels
im = ax.imshow(AFM_map_nm, cmap='afmhot', origin = 'lower')

# format the X and Y axis labels
    # be sure to indicate the step size
    # in this example, the step size is 0.150 micron
fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.150):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('X (μm)')
ax.set_ylabel('Y (μm)')

# add colorscale bar
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%',pad=0.1)
cb = fig.colorbar(im, cax=cax, orientation='vertical')
cbar = plt.gcf().axes[-1]
cbar.set_ylabel("height (um)", rotation=90, va="bottom", size=12, labelpad=20)