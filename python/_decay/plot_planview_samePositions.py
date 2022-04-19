"""
coding: utf-8

tzwalker
Sat Sep 11 10:35:30 2021

this program was copied from "plot_XANESvPosition_cross sections.py"

it was a test plotting of XBIC map positions

this program plots plan-view maps of TS118_1A - 2018_11_26IDC - scans195,196,197
and overlays a scatter plot at specific pixel indices
https://stackoverflow.com/questions/29155324/how-can-i-color-specific-pixels-in-matplotlib-imshow

the indices are the scatter plot data

run this program after 'main-TS118_1A-ASCII'

# cmaps: 
    #RdYlGn 
    #inferno 
    #Greys_r
    #Blues_r
    #viridis
    #Oranges_r
    #YlOrBr_r
    
"""

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np


def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

 
units = 'XBIC (nA)'
cmaps = 'inferno'

cbar_txt_size=10


img = TS1181A.scan197[0,:,:]
data = img.copy()
data = np.array(data)
data = data[:,:-2] * 1e9
    
fig, ax = plt.subplots()

im = ax.imshow(data, cmap=cmaps)

# scan 195 indices
plt.scatter([14,16,31], [18,32,20], color='white', marker='+', s=20)

# scan 196 indices
#plt.scatter([9,10,12,14,15], [35,35,35,35,35], color='red', s=10)

ax.set_xlabel('X (pix)')
ax.set_ylabel('Y (pix)')
    
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%',pad=0.1)
# for windows
cb = fig.colorbar(im, cax=cax, orientation='vertical')
cbar = plt.gcf().axes[-1]
cbar.set_ylabel(units, rotation=90, va="bottom", size=12, labelpad=20)
cbar.yaxis.set_offset_position('left')
    

