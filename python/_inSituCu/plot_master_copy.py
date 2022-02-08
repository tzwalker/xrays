"""
coding: utf-8

tzwalker
Fri Aug 27 09:27:09 2021

this program is meant to plot extra cross section maps of NBL31 and NBL33

these maps all had different scan parameters, and a single scale bar is not adequate

this program plots the maps with their axes in um
    see great advice in these links:
        https://stackoverflow.com/questions/66927234/change-from-pixel-to-micron-when-using-matplotlib-plt-imshow
        https://stackoverflow.com/questions/25119193/matplotlib-pyplot-axes-formatter
        

be sure to run first section in the code "main-NBL3-xsect.py" before
running this program
"""


import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker

def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

idxs = [0,1,2]
units = ['XBIC (A)', 'Cu XRF (cts/s)', 'Cd XRF (cts/s)']
cmaps = ['inferno', 'Greys_r', 'Blues_r']

for idx in idxs:
    
    img = map_dfs[idx]
    
    data = img.copy()
    
    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap=cmaps[idx])
    ax.invert_xaxis()
    
    fmtr_x = lambda x, pos: f'{(x * 0.050):.0f}'
    fmtr_y = lambda x, pos: f'{(x * 0.150):.0f}'
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
    ax.set_xlabel('X (μm)')
    ax.set_ylabel('Y (μm)')
    
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%',pad=0.1)
    cb = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar = plt.gcf().axes[-1]
    cbar.set_ylabel(units[idx], rotation=90, va="bottom", size=12, labelpad=20)
    
    xsize = int(META_DATA['x_size'].values) #pixel
    ysize = int(META_DATA['y_size'].values) #pixel
    
    if xsize < ysize:
        aspect_ratio = xsize / ysize
    else:
        aspect_ratio = ysize / xsize
    forceAspect(ax,aspect=aspect_ratio)

