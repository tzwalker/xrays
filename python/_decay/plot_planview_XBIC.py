"""
coding: utf-8
tzwalker
Wed May 13 15:31:19 2020

for TS118_1A decay (2018_11_26IDC):
    plan-view inner map: 4px = 1um; figsize=2.5,2.5
    plan-view outer map: 2px = 1um; figsize=3.4,5.65
    xsect scan0051: 
            x - 10um/101pts = 1px = 0.100um
            y - 40px/101pts = 1px = 0.400um


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
import matplotlib.offsetbox as offbox
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.lines import Line2D
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


SAVE = 1
OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\2_XBIC_decay\figures v1'
FNAME = r'\TS118_1A_scan197_XBIC.eps'

scalebar = 1
scalebar_color = 'black'
# SET SCALE BAR
px = 12; dist = '3um' # CHANGE
px = 20; dist = '10um'

draw_cbar = 1
cbar_txt_size = 10
top_cbar = 0
side_cbar=1

cbar_scale_control = 0; MAX = 250; MIN = 0
normalize = 0
sci_notation = 1

unit = 'XBIC (nA)'; colormap='inferno'

img = TS1181A.scan197[0,:,:] # CHANGE
data = img.copy()
data = data * 1e9


plt.figure()
#fig, ax = plt.subplots(figsize=(2.5,2.5)) # CHANGE
fig, ax = plt.subplots(figsize=(3.4,5.65))


if cbar_scale_control == 1:
    if normalize == 1:
        #data = data*1e8
        data = (data - data.min()) / (data.max() - data.min())
    im = ax.imshow(data, cmap=colormap, vmax=MAX, vmin=MIN)
else: 
    if normalize == 1:
        #data = data*1e8
        data = (data - data.min()) / (data.max() - data.min())
    im = ax.imshow(data, cmap=colormap)

if scalebar == 1:
    ax.axis('off')
    ob = AnchoredHScaleBar(size=px, label=dist, loc=4, frameon=False,
                           pad=0.1, borderpad=0.5, sep=4, 
                           linekw=dict(color=scalebar_color))
    ax.add_artist(ob)

# plot crosshairs at specific positions # CHANGE
# scan 195 indices
#plt.scatter([14,16,31], [18,32,20], marker='+', s=50, color='white')

# scan 196 indices
#plt.scatter([27,5,10], [16,4,24], marker='x', s=50, color='white')

# scan 197 indices
plt.scatter([27,28,35], [69,76,70], marker='+', s=50, color='white')
plt.scatter([33,22,25], [28,22,32], marker='x', s=50, color='white')

if draw_cbar == 1:
    divider = make_axes_locatable(ax)
    
    if side_cbar == 1:
        # create color bar
        cax = divider.append_axes('right', size='5%', pad=0.1)
        if sci_notation == 1:
            fmt = ticker.ScalarFormatter(useMathText=True)
            fmt.set_powerlimits((0, 0))
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
            #change color bar scale label size, e.g. 1e-8
        cbar.yaxis.get_offset_text().set(size=cbar_txt_size)
            #change color bar scale label position   
        cbar.yaxis.set_offset_position('left')
    
    if top_cbar == 1:
        cax = divider.new_vertical(size='5%', pad=0.25)
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
        cbar = plt.gcf().axes[-1]
        cbar.yaxis.set_offset_position('left')
        

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)