"""
coding: utf-8

tzwalker
Wed May 13 15:31:19 2020
"""

'''adds scalebar to matplotlib images'''
import matplotlib.pyplot as plt
import matplotlib.offsetbox as offbox
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
        vline1 = Line2D([0,0],[-extent/2.,extent/2.], **linekw)
        vline2 = Line2D([size,size],[-extent/2.,extent/2.], **linekw)
        size_bar.add_artist(line)
        size_bar.add_artist(vline1)
        size_bar.add_artist(vline2)
        txt = offbox.TextArea(label, minimumdescent=False, 
                              textprops=dict(color="black"))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)

for i in imgs:
    data = i*1000#NBL33.scan261[0,:,:]
    data1 = data.copy()
    
    plt.figure()
    
    fig, ax = plt.subplots()
    im = ax.imshow(data1, cmap='inferno') #RdYlGn #inferno
    ax.axis('off')
    
    ob = AnchoredHScaleBar(size=67, label="10 um", loc=4, frameon=True,
                           pad=0.5, borderpad=1, sep=4, 
                           linekw=dict(color="black"))
    ax.add_artist(ob)
    
    cbar = 1
    if cbar == 1:
        # create color bar
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.1)
        fig.colorbar(im, cax=cax, orientation='vertical',format='%.2g')
        #get color bar object
        cbar = plt.gcf().axes[-1]
        #format colorbar
        cbar.set_ylabel('XBIV (mV)', rotation=90, va="bottom", size=11, labelpad=15)
        #change colorbar tick label sizes
        cbar.tick_params(labelsize=11)   
        #change color bar scale label size, e.g. 1e-8
        cbar.yaxis.get_offset_text().set(size=11)
        #change color bar scale label position   
        cbar.yaxis.set_offset_position('left')

OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_XBIC_decay\figures v0'
FNAME = r'\TS1181A_scan195_XBIC.eps'
#plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300)


