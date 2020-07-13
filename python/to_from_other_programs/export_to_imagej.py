"""
tzwalker
Sat Nov  2 17:35:04 2019
coding: utf-8

Export image of map of interest

"""

import matplotlib.pyplot as plt  
import numpy as np

def export_to_ImgJ_planview(path, shaped_data, color, name, 
                             scan,dpi, save):
    fig, ax = plt.subplots()
    #plt.figure(frameon=False)
    x_dim = shaped_data.shape[1] ; y_dim = shaped_data.shape[0]
    fig.set_size_inches(x_dim/dpi, y_dim/dpi)    
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.imshow(shaped_data, cmap=color)
    if save == 1:
        fname = r'\scan{s}_{ele}.png'.format(s=scan,ele=name)
        directory= path+fname
        plt.savefig(directory, dpi=dpi)
    else: pass
    return

# =============================================================================
# PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\for_imagej'
# 
# SAMPLE= NBL33; SCAN = 4; CHAN = 0
# MAP_OUT = SAMPLE.maps[SCAN][CHAN,:,:-2]
# scanstr = str(SAMPLE.scans[SCAN])
# NAMES = ['XBIV', 'Cu', 'Cd', 'Te', 'Mo', 'Zn']
# CMAPS = ['inferno', 'Oranges_r', 'Blues_r', 'Greens_r', 'Reds_r', 'Greys_r']
# # export to imagej #
# export_to_ImgJ_planview(PATH, MAP_OUT, CMAPS[CHAN], NAMES[CHAN],
#                          scan=scanstr,dpi=96, save=1)
# =============================================================================

# save FS3 operando XBIV vs. Temp
# this code will show axes in spyder, but the exported image
# will have no axes in the image
# and will ahve the same pixels as the original array
# i.e. this code WORKS despite what is shown in the spyder plot window
#SCAN = 'scan321'
PATH = r'C:\Users\triton\Dropbox (ASU)\1_FS_operando\for_imageJ\Se'
FNAME = r'\scan321_XBIV.txt'
PATH_OUT = PATH + FNAME
ARR_OUT = imgs[0] #getattr(NBL33,SCAN)[3,:,:-2]
DPI=96

fig, ax = plt.subplots()
XDIM = ARR_OUT.shape[1] ; YDIM = ARR_OUT.shape[0]
fig.set_size_inches(XDIM/DPI, YDIM/DPI)    
ax = fig.add_axes([0, 0, 1, 1])

ax.imshow(ARR_OUT, cmap='inferno')
ax.set_axis_off()
#plt.savefig(PATH_OUT, dpi=DPI)

np.savetxt(PATH_OUT, ARR_OUT)


