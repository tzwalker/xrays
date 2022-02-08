"""
coding: utf-8
Trumann
Tue Feb  8 08:44:02 2022

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


def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

SAVE = 1
idxs = [0,1,2,3,4]

# for infinite cross sections
units = ['XBIC (nA)', 'Cu XRF (cts/s)', 'Se XRF (cts/s)', 'Te XRF (cts/s)', 'Au XRF (cts/s)']

cmaps = ['inferno', 'Oranges_r', 'Blues_r', 'Greys_r', 'YlOrBr_r']

cbar_txt_size=10

for idx in idxs:
    img = df_maps[idx]
    data = img.copy()
    data = np.array(data)
    data = data[:,:-2]
        
    MAX = data.max().max(); MIN = 0
    plt.figure()
    
    fig, ax = plt.subplots(figsize=(1.35,1.35))
    
    im = ax.imshow(data, cmap=cmaps[idx])
    
    fmtr_x = lambda x, pos: f'{(x * 0.160):.0f}'
    fmtr_y = lambda x, pos: f'{(x * 0.160):.0f}'
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
    ax.set_xlabel('X (μm)')
    ax.set_ylabel('Y (μm)')
        
    divider = make_axes_locatable(ax)


    cax = divider.append_axes('right', size='5%',pad=0.1) # for 151
    
    if idx > 0:
        fmt = mticker.ScalarFormatter(useMathText=True)
        fmt.set_powerlimits((0, 1))
        cb = fig.colorbar(im, cax=cax, orientation='vertical', format=fmt)
    else:
        cb = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar = plt.gcf().axes[-1]
    cbar.set_ylabel(units[idx], rotation=90, va="bottom", size=12, labelpad=20)
    cbar.yaxis.set_offset_position('left')
    
    #aspect_ratio = 1
    #forceAspect(ax,aspect=aspect_ratio)
    OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33 XRF maps'
    FNAME = r'\PVSe33.4_2x_scan0151_{s}.eps'.format(s=channels[idx])
    
    if SAVE == 1:
        plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)