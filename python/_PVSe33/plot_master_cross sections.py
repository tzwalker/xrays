"""
coding: utf-8

tzwalker
Wed Sep  1 08:30:39 2021

this program plots cross-section maps with different xy scales
run this program after 'main-PVSe33-ASCII-xsect'
the cross-section maps are for PVSe33

#for TS118_1A decay (2018_11_26IDC):
    plan-view inner map: 4px = 1um
    plan-view outer map: 2px = 1um

#for PVS33 
    plan-view (2020_10_26IDC): 25px = 4um
    cross-section(2021_07_2IDD): 1px = 160nm, 25px = 4um
    
#for NBL3xsect NBL33
    # XBIC: vmin=0,vmax=80, after multiplying 'data1' by 1E9
    # Cu XRF: vmin=0,vmax=30000
    # Cd XRF: vmin=0,vmax=15000

#for NBL33 xsect scan 1: 1px = 0.10um, 10px = 1.0um, 20px = 2um 
#for NBL3xsect NBL31
    for NBL31 xsect scan 8: 1px = 0.05um, 10px = 0.5um, 20px = 1um
    # XBIC: vmin=0,vmax=250, after multiplying 'data1' by 1E9,bins=3
    # Cu XRF: vmin=0,vmax=2000, bins=2
    # Cd XRF: vmin=0,vmax=15000, bins=4
    
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
import matplotlib.ticker as mticker


def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

idxs = [0,1,2,3]
# for windows 
units = ['XBIC (nA)', 'Se XRF (ug/cm2)', 'Te XRF (ug/cm2)', 'Au XRF (ug/cm2)']
# for infinite cross sections
#units = ['XBIC (nA)', 'Se XRF (cts/s)', 'Te XRF (cts/s)', 'Au XRF (cts/s)']
cmaps = ['inferno', 'Blues_r', 'Greys_r', 'YlOrBr_r']

cbar_txt_size=10

for idx in idxs:
    img = df_maps[idx]
    data = img.copy()
    data = np.array(data)
    data = data[:,:-2]
        
    MAX = data.max().max(); MIN = 0
    plt.figure()
    
    fig, ax = plt.subplots()
    
    im = ax.imshow(data, cmap=cmaps[idx])
    
    fmtr_x = lambda x, pos: f'{(x * 0.160):.0f}'
    fmtr_y = lambda x, pos: f'{(x * 0.160):.0f}'
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
    ax.set_xlabel('X (μm)')
    ax.set_ylabel('Y (μm)')
        
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%',pad=0.1) # for 072
    #cax = divider.append_axes('right', size='2%',pad=-3.5) # for 119
    #cax = divider.append_axes('right', size='5%',pad=0.1) # for 151
    # for infinite cross sections
    #fmt = mticker.ScalarFormatter(useMathText=True)
    #fmt.set_powerlimits((0, 1))
    #cb = fig.colorbar(im, cax=cax, orientation='vertical', format=fmt)
    # for windows
    cb = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar = plt.gcf().axes[-1]
    cbar.set_ylabel(units[idx], rotation=90, va="bottom", size=12, labelpad=20)
    cbar.yaxis.set_offset_position('left')
    
    aspect_ratio = 8/10
    forceAspect(ax,aspect=aspect_ratio)

