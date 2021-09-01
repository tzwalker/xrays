"""
coding: utf-8
tzwalker
Wed May 13 15:31:19 2020
for FS3_operando: 67px = 10um
for NBL3:  20px = 3um
for NBL33 xsect scan 1: 1px = 0.10um, 10px = 1.0um, 20px = 2um 
for NBL31 xsect scan 8: 1px = 0.05um, 10px = 0.5um, 20px = 1um
for stage pattern
    overview: 30px = 20um
    tiny features: 10px = 1um
    Au4: 10px = 1um
    line: 1px = 50nm
for TS118_1A decay (2018_11_26IDC):
    plan-view inner map: 4px = 1um
    plan-view outer map: 2px = 1um
for PVS33 (2020_10_26IDC)
    plan-view: 25px = 4um
    
# cmaps: 
    #RdYlGn 
    #inferno 
    #Greys_r
    #Blues_r
    #viridis
    #Oranges_r
    #YlOrBr_r
#for NBL3xsect NBL33
    # XBIC: vmin=0,vmax=80, after multiplying 'data1' by 1E9
    # Cu XRF: vmin=0,vmax=30000
    # Cd XRF: vmin=0,vmax=15000
#for NBL3xsect NBL31
    # XBIC: vmin=0,vmax=250, after multiplying 'data1' by 1E9,bins=3
    # Cu XRF: vmin=0,vmax=2000, bins=2
    # Cd XRF: vmin=0,vmax=15000, bins=4
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
                              textprops=dict(color=scalebar_color,weight='bold'))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)
SAVE = 0
OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_XBIC_decay\figures v0'
FNAME = r'\TS118scan196_XBIC2.eps'

scalebar = 1; scalebar_color='white'
draw_cbar = 1; sci_notation = 1; cbar_txt_size=10
img = map_dfs[0]
data = img.copy()
data = data

# =============================================================================
# unit = 'XBIC (A)'
# MAX = data.max().max(); MIN = data.min().min()
# colormap = 'inferno'
# =============================================================================

# =============================================================================
# unit = 'Cu XRF (cts/s)'
# MAX = 20000; MIN = 0
# colormap = 'Oranges_r'
# =============================================================================


unit = 'XBIC (A)'
colormap = 'inferno'


MAX = data.max().max(); MIN = 0
plt.figure()

fig, ax = plt.subplots(figsize=(3,1.7))
ax.set_aspect('equal')
    
im = ax.imshow(data, cmap=colormap, vmax=MAX, vmin=MIN)
ax.axis('off')

if scalebar == 1:
    ob = AnchoredHScaleBar(size=20, label="2 um", loc=4, frameon=False,
                           pad=0.1, borderpad=0.1, sep=4, 
                           linekw=dict(color=scalebar_color))
    ax.add_artist(ob)

if draw_cbar == 1:
        # create color bar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.1)
    if sci_notation == 1:
        fmt = ticker.ScalarFormatter(useMathText=True)
        fmt.set_powerlimits((0, 1))
        cb = fig.colorbar(im, cax=cax, orientation='vertical',format=fmt)
    else:
        cb = fig.colorbar(im, cax=cax, orientation='vertical')#,format='.1f')
        #get color bar object
    cbar = plt.gcf().axes[-1]
        #format colorbar
    cbar.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
        # change number of tick labels on colorbar
    #cbar.locator_params(nbins=4)
        #change colorbar tick label sizes
    cbar.tick_params(labelsize=cbar_txt_size)
        # change scale label, e.g. 1e-8
    #cbar.set_title(r'$\times$10$^{-9}$', size=11,loc='left')
        #change color bar scale label size, e.g. 1e-8
    cbar.yaxis.get_offset_text().set(size=cbar_txt_size)
        #change color bar scale label position   
    cbar.yaxis.set_offset_position('left')

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)