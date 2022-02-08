"""
coding: utf-8
Trumann
Tue Feb  8 11:47:49 2022
"""

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np


def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

SAVE = 1
idxs = [0,1,2]
idx = 1
# for windows 
# units = ['XBIC (nA)', 'Se XRF (ug/cm2)', 'Te XRF (ug/cm2)', 'Au XRF (ug/cm2)']
# for infinite cross sections
units = ['XBIC (nA)', 'Cu XRF (cts/s)', 'Cd XRF (cts/s)']
cmaps = ['inferno', 'Oranges_r', 'Greys_r']

cbar_txt_size=10

# import list from 'main-PVSe33-ASCII-xsect.py'
img = df_maps[idx]
data = img.copy()
data = np.array(data)
data = data[:,:-2]
    
MAX = data.max().max(); MIN = 0
plt.figure()

fig, ax = plt.subplots(figsize=(3,3))

im = ax.imshow(data, cmap=cmaps[idx])

# scan 1212 indices
x_coord = [15,19,23,27,31,35,39,42,46,50]
y_coord = 10* [48]
plt.scatter(x_coord, y_coord, color='black', s=3)

# scan 1210 indices
#plt.scatter([9,10,12,14,15], [35,35,35,35,35], color='red', s=10)

ax.set_xlabel('X (pix)')
ax.set_ylabel('Y (pix)')
    
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='10%',pad=0.1) # for 072

# for infinite cross sections
#fmt = mticker.ScalarFormatter(useMathText=True)
#fmt.set_powerlimits((0, 1))
#cb = fig.colorbar(im, cax=cax, orientation='vertical', format=fmt)
# for windows
cb = fig.colorbar(im, cax=cax, orientation='vertical')
cbar = plt.gcf().axes[-1]
cbar.set_ylabel(units[idx], rotation=90, va="bottom", size=12, labelpad=20)
cbar.yaxis.set_offset_position('left')

OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_XANESvP_Cu'
FNAME = r'\PVSe33.4_2x_scan1212_{s}_XANESpositions.eps'.format(s=channels[idx])

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)