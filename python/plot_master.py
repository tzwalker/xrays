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

#for i in imgs:
#data = FS3.scan344[1,:,:]#i#NBL33.scan261[0,:,:]
data1 = data.copy()
data1=data1
plt.figure()

fig, ax = plt.subplots(figsize=(5,5))
# cmaps: 
    #RdYlGn #inferno #Greys_r #viridis #Oranges_r #Blues_r
#for NBL3xsect
    # XBIC: vmin=
    # Cu XRF: vmin=0,vmax=4 after dividing 'data1' by 10000
#for FS3
    # Se XRF: vmin=0.5,vmax=1.5
    # XBIC: vmin=5.6E-8,vmax=8.6E-8 
    
im = ax.imshow(data1, cmap='Blues_r')#, vmin=0,vmax=4)
ax.axis('off')

scalebar = 0
if scalebar == 1:
    ob = AnchoredHScaleBar(size=67, label="10 um", loc=4, frameon=True,
                           pad=0.5, borderpad=1, sep=4, 
                           linekw=dict(color="black"))
    ax.add_artist(ob)

cbar = 1
if cbar == 1:
    # create color bar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.1)
    fig.colorbar(im, cax=cax, orientation='vertical',format='%.0f')
    #get color bar object
    cbar = plt.gcf().axes[-1]
    #format colorbar
    cbar.set_ylabel('XRF (cts/s)', rotation=90, va="bottom", size=11, labelpad=15)
    #change colorbar tick label sizes
    cbar.tick_params(labelsize=11)
    # scale label, e.g. 1e-8
    #cbar.set_title('1e4', size=11,loc='left')
    #change color bar scale label size, e.g. 1e-8
    cbar.yaxis.get_offset_text().set(size=11)
    #change color bar scale label position   
    cbar.yaxis.set_offset_position('left')

OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_NBL3\20200525 figures_rev3\xsect_exp\maps with colorbars'
FNAME = r'\NBL33scan1_Cd.eps'
plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)


