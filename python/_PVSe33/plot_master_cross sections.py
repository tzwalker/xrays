"""
coding: utf-8

tzwalker
Wed Sep  1 08:30:39 2021

this program plots cross-section maps with different xy scales
run this program after 'main-PVSe33-ASCII-xsect'
the cross-section maps are for PVSe33

#for PVS33 
    plan-view (2020_10_26IDC): 25px = 4um
    cross-section(2021_07_2IDD): 1px = 160nm, 25px = 4um
    

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
import numpy as np

SAVE = 0
idxs = [4]#,1,2,3,4]
# for windows 
#units = ['XBIC (nA)', 'Cu XRF (ug/cm2)', 'Se XRF (ug/cm2)', 'Te XRF (ug/cm2)', 'Au XRF (ug/cm2)']
# for infinite cross sections
units = ['XBIC (nA)', 'Cu XRF (ug/cm2)', 'Se XRF (cts/s)', 'Te XRF (cts/s)', 'Au XRF (cts/s)']

cmaps = ['inferno', 'Oranges_r', 'Blues_r', 'Greys_r', 'YlOrBr_r']

cbar_txt_size=11

for idx in idxs:
    img = df_maps[idx]
    data = img.copy()
    data = np.array(data)
    data = data[:,:-2]
        
    MAX = data.max().max(); MIN = 0
    
    fig, ax = plt.subplots()
    
    im = ax.imshow(data, cmap=cmaps[idx])
    # this aspect is the x width points (~101) over the y hieght points(~11), for scan 119
    ax.set_aspect(10)
    
    fmtr_x = lambda x, pos: f'{(x * 0.100):.0f}'
    fmtr_y = lambda x, pos: f'{(x * 1):.0f}'
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
    ax.set_xlabel('X (μm)')
    ax.set_ylabel('Y (μm)')
        
    divider = make_axes_locatable(ax)
    #cax = divider.append_axes('right', size='5%',pad=0.1) # for 072
    cax = divider.append_axes('right', size='2%',pad=-3.5) # for 119
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
    
    
    OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33 XRF maps'
    FNAME = r'\PVSe33.3_3x_scan0119_{s}.eps'.format(s=channels[idx])
    
    if SAVE == 1:
        plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)

