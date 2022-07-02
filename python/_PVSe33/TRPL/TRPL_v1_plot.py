# -*- coding: utf-8 -*-
"""

Trumann
Wed Jun 29 16:11:06 2022

this program plots the TRPL data from PVSe33.3_2 and PVSe33.4_3

"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import ticker
import numpy as np
import tifffile
import matplotlib.ticker as mticker


#f = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\20220317_TRPL_0hr_example_0423bPL2Axis.txt.tif"
f = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\20220410_TRPL_500hr_example_0423ePL2Axis.txt.tif"
import_data = tifffile.imread(f)

total_cts1 = np.sum(import_data,axis=0)
#%%
SAVE = 0
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_TPRL'
FNAME = r'\500hr_0423e.pdf'

data = total_cts1.copy()

scalebar_color = 'white'
px = 10; dist = u"2.4\u03bcm"

cbar_txt_size = 11

unit = u'Intensity (cts/s)'

fig, ax = plt.subplots(figsize=(2.5,2.5))

im = ax.imshow(data, cmap='Greens_r', origin='lower', vmin=2000, vmax=14000)

ax.xaxis.set_ticks(np.arange(0,51,20))
ax.yaxis.set_ticks(np.arange(0,51,20))
fmtr_x = lambda x, pos: f'{(x * 0.245):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.245):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)',size=cbar_txt_size)
ax.set_ylabel('$Y$ (μm)',size=cbar_txt_size)

# format colorbar
cax1 = fig.add_axes([ax.get_position().x1+0.025,ax.get_position().y0,0.025,ax.get_position().height])
fmt = ticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))

cbar = fig.colorbar(im, cax=cax1, orientation='vertical',format=fmt)
cbar.ax.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
#cbar.locator_params(nbins=4)
cbar.ax.tick_params(labelsize=cbar_txt_size)
cbar.ax.yaxis.get_offset_text().set(size=cbar_txt_size)
cbar.ax.yaxis.set_offset_position('left')

# read these coordinates from drawn box in IMageJ: [28,36,28,36],[28,28,36,36]
    # then Image -> Stacks -> Plot Z-axis profile
    # saved the TRPL spectra within these pixels
    #"Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\0423bPL2Axis_spectrumROI_longDecay1.csv"
#ax.add_patch(Rectangle((28, 28), 8, 8, linestyle = 'solid', facecolor="none", ec='w', lw=2))

# read these coordinates from drawn box in IMageJ: [28,36,28,36],[28,28,36,36]
    # then Image -> Stacks -> Plot Z-axis profile
    # saved the TRPL spectra within these pixels
#ax.add_patch(Rectangle((26, 37), 8, 8, linestyle = 'dashed', facecolor="none", ec='w', lw=2))

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)