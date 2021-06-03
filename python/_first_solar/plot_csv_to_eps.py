"""
coding: utf-8

tzwalker
Wed Jun  2 11:46:47 2021

this program is for plotting FS3 2019_06_2IDD data for the stage paper

for FS3_operando:
    67px = 10um
for stage pattern
    overview: 30px = 20um
    tiny features: 10px = 1um
    Au4: 10px = 1um
    line: 1px = 50nm
    
# cmaps: 
    #RdYlGn 
    #inferno 
    #Greys_r
    #Blues_r
    #viridis
    #Oranges_r
    #YlOrBr_r

#for FS3
    # Se XRF: vmin=0.5,vmax=1.5
    # XBIC: vmin=5.6E-8,vmax=8.6E-8 
"""
import matplotlib.pyplot as plt
import matplotlib.offsetbox as offbox
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import ticker
'''adds scalebar to matplotlib images'''
class AnchoredHScaleBar(offbox.AnchoredOffsetbox):
    """ size: length of bar in pixels
        extent : height of bar ends in axes units """
    def __init__(self, size=1, extent = 0.03, label="", loc=2, ax=None,
                 pad=0.4, borderpad=0.5, ppad = 0, sep=2, prop=None, 
                 frameon=True, linekw={}, **kwargs):
        if not ax:
            ax = plt.gca()
        trans = ax.get_xaxis_transform()
        size_bar = offbox.AuxTransformBox(trans)
        line = Line2D([0,size],[0,0], **linekw)
        #vline1 = Line2D([0,0],[-extent/2.,extent/2.], **linekw)
        #vline2 = Line2D([size,size],[-extent/2.,extent/2.], **linekw)
        size_bar.add_artist(line)
        #size_bar.add_artist(vline1)
        #size_bar.add_artist(vline2)
        txt = offbox.TextArea(label, minimumdescent=False, 
                              textprops=dict(color=scalebar_color,weight='bold', size=cbar_txt_size))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)
import numpy as np

# specificy path to csvs
PATH_IN = r'C:\Users\triton\Dropbox (ASU)\2_FS_operando\XBIC aligned image csvs'
# XBIC scans
scans = [323,327,332,339,344]
# XBIV scans
#scans = [321,325,330,337,342]
scans1 = [str(s) for s in scans]

T_list = ['20C', '40C', '60C', '80C', '100C']

channel = 'Se'

# import aligned XBIC maps
imgs = []
for S in scans1:
    FNAME = r'\FS3_scan{SCN}_{CHAN}.csv'.format(SCN=S, CHAN=channel)
    IMG = np.genfromtxt(PATH_IN+FNAME, delimiter=',')
    imgs.append(IMG)
    
SAVE = 1

### PLOT SETTINGS
scalebar = 1
scalebar_color = 'white'
px = 67; dist = u"10\u03bcm"

draw_cbar = 1
cbar_txt_size = 8
top_cbar = 1
side_cbar=0

cbar_scale_control = 1; MIN = 0; MAX = 1.5
normalize = 0
standardized = 0
sci_notation = 0

#unit = u'XBIC (arb. units)'; colormap = 'inferno';
unit = u'Se (\u03bcg/cm$^{2}$)'; colormap = 'viridis';


for i, data0 in enumerate(imgs):
    data = data0.copy()
    
    if normalize == 1:
        #data = data*1e8
        data_norm = data / data.max()
    if standardized == 1:
        mean = np.mean(data)
        std = np.std(data)
        data_stand = (data - mean) / std
    
    
    plt.figure()
    fig, ax = plt.subplots(figsize=(2.5,1.5))
    
    if normalize == 0:
        if cbar_scale_control == 0: 
            im = ax.imshow(data, cmap=colormap)
        if cbar_scale_control == 1:
            im = ax.imshow(data, cmap=colormap, vmax=MAX, vmin=MIN)
    
    if normalize == 1:
        if cbar_scale_control == 0:
            im = ax.imshow(data_norm, cmap=colormap)
        if cbar_scale_control == 1:
            im = ax.imshow(data_norm, cmap=colormap, vmax=MAX, vmin=MIN)
    if standardized == 1:
        if cbar_scale_control == 0:
            im = ax.imshow(data_stand, cmap=colormap)
        if cbar_scale_control == 1:
            im = ax.imshow(data_stand, cmap=colormap, vmax=MAX, vmin=MIN)
    
    ax.axis('off')
    
    if scalebar == 1:
        ob = AnchoredHScaleBar(size=px, label=dist, loc=4, frameon=False,
                               pad=0.25, borderpad=0.25, sep=4, 
                               linekw=dict(color=scalebar_color))
        ax.add_artist(ob)
    
    if draw_cbar == 1:
        divider = make_axes_locatable(ax)
        if side_cbar == 1:
            # create color bar
            cax = divider.append_axes('right', size='5%', pad=0.1)
            if sci_notation == 1:
                fmt = ticker.ScalarFormatter(useMathText=True)
                fmt.set_powerlimits((1, 0))
                cb = fig.colorbar(im, cax=cax, orientation='vertical',format=fmt)
            else:
                cb = fig.colorbar(im, cax=cax, orientation='vertical')#,format='.1f')
                #get color bar object
            cbar = plt.gcf().axes[-1]
                #format colorbar
            cbar.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
                # change number of tick labels on colorbar
            cbar.locator_params(nbins=4)
                #change colorbar tick label sizes
            cbar.tick_params(labelsize=cbar_txt_size)
                #change color bar scale label size, e.g. 1e-8
            cbar.yaxis.get_offset_text().set(size=cbar_txt_size)
                #change color bar scale label position   
            cbar.yaxis.set_offset_position('left')
        if top_cbar == 1:
            cax = divider.new_vertical(size='5%', pad=0.1)
            fig.add_axes(cax)
            if sci_notation == 1:
                fmt = ticker.ScalarFormatter(useMathText=True)
                fmt.set_powerlimits((0, 0))
                cb = fig.colorbar(im, cax=cax, orientation='horizontal',format=fmt)
            else:
                cb = fig.colorbar(im, cax=cax, orientation='horizontal')
            # change cbar label font sizes
            cb.set_label(unit, fontsize=cbar_txt_size)
            cb.ax.tick_params(labelsize=cbar_txt_size)
            #move cbar ticks to top of cbar
            cax.xaxis.set_label_position('top')
            cax.xaxis.set_ticks_position('top')
            #change number of tick labels on cbar
            #cbar = plt.gcf().axes[-1]
            #cbar.locator_params(nbins=10)

    if SAVE == 1:
        OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\0_stage design\20210527 figures_v1\figure4 materials'
        FNAME = r'\FS3_{TEMP}_scan{SCAN}_{CHAN}.eps'.format(TEMP=T_list[i], SCAN=scans1[i], CHAN=channel)
        #print(FNAME)
        plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)