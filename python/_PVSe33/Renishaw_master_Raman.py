# -*- coding: utf-8 -*-
"""

Trumann
Tue Jun 28 12:23:58 2022

this program plot Raman peak instensity from the Renishaw wdf file

the peak intensity at each xy location is plotted

"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from renishawWiRE import WDFReader
import numpy as np
 
#FILE = r"Z:\Trumann\Renishaw\20210213 PVSe33 redo 2\PVSe33.3_2 Au Side_raman_map0.wdf"
FILE = r"Z:\Trumann\Renishaw\20210304 PVSe33\PVSe33.4_3 Au side raman map0.wdf"

# import wdf file
reader = WDFReader(FILE)
reader.print_info()

# get x-axis of spectral data
    # keep in mind the units you specified for the measurement
    # here the measurement was made using shift (cm-1) as the x-axis
shift = reader.xdata

# get the spectral data from the map; has form (y_pixel, x_pixel, intensity)
spectra = reader.spectra


# specify the x-axis value you wish to plot
    # here the CdTe peaks of interest are 127,141,167,275,365cm-1
user_shift = 141

# find the value in the x-axis that is closest to the specified x-axis value
E_idx = (np.abs(shift - user_shift)).argmin()

# get the intensity at this wavenumber as a function of x and y
user_map = spectra[:,:,E_idx]

#%%
SAVE = 1
unit = 'Intensity (cts/s)'

img = user_map[:-1,:].copy()

cbar_txt_size = 11

fig, ax = plt.subplots(figsize=(2.5,2.5))

im = ax.imshow(img, cmap='Greys_r', vmin = 100, vmax=500, origin='lower')

fmtr_x = lambda x, pos: f'{(x * 1.0):.0f}'
fmtr_y = lambda x, pos: f'{(x * 1.0):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)',size=cbar_txt_size)
ax.set_ylabel('$Y$ (μm)',size=cbar_txt_size)

# format and add colorbar
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))

cax1 = fig.add_axes([ax.get_position().x1+0.025,ax.get_position().y0,0.025,ax.get_position().height])
cbar = fig.colorbar(im, cax=cax1)#, format=fmt)
cbar.ax.set_ylabel(unit, rotation=90, 
                   va="bottom", size=cbar_txt_size, labelpad=15)
cbar.ax.yaxis.set_offset_position('left')

if SAVE == 1:
        OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_renishaw'
        FNAME = r'\500hr_Au_Raman141cm-1.pdf'
        plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)