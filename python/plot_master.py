"""
coding: utf-8

tzwalker
Wed May 13 15:31:19 2020

for FS3_operando: 67px = 10um
for NBL3:  33px = 5um or... 50px =5um (for older scans 2017_2018)
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

img = NBL32.scan422[1,:,:-2]
data = img.copy()
data = data
plt.figure()

fig, ax = plt.subplots(figsize=(5,5))
# cmaps: 
    #RdYlGn 
    #inferno 
    #Greys_r
    #Blues_r
    #viridis #Oranges_r 
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
    
im = ax.imshow(data, cmap='Oranges_r')
ax.axis('off')

scalebar = 1
if scalebar == 1:
    ob = AnchoredHScaleBar(size=33, label="5 um", loc=2, frameon=True,
                           pad=0.5, borderpad=1, sep=4, 
                           linekw=dict(color="black"))
    ax.add_artist(ob)

cbar = 1
if cbar == 1:
        # create color bar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.1)
    fig.colorbar(im, cax=cax, orientation='vertical')#,format='%.0f')
        #get color bar object
    cbar = plt.gcf().axes[-1]
        #format colorbar
    cbar.set_ylabel('Concentration (ug/cm2)', rotation=90, va="bottom", size=12, labelpad=20)
        # change number of tick labels on colorbar
    #cbar.locator_params(nbins=4)
        #change colorbar tick label sizes
    cbar.tick_params(labelsize=12)
        # change scale label, e.g. 1e-8
    #cbar.set_title('1e4', size=11,loc='left')
        #change color bar scale label size, e.g. 1e-8
    cbar.yaxis.get_offset_text().set(size=12)
        #change color bar scale label position   
    cbar.yaxis.set_offset_position('left')

OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20200525 figures_rev3\main_xrf\vector graphics'
FNAME = r'\NBL32scan422_Cu.eps'
plt.savefig(OUT_PATH+FNAME, format='eps', bbox_inches='tight', pad_inches = 0) #, dpi=300, )


