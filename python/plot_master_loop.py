"""
coding: utf-8
tzwalker
Wed May 13 15:31:19 2020
for FS3_operando: 67px = 10um
for NBL3:  33px = 5um
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
    def __init__(self, length=1, extent = 0.03, label="", loc=2, ax=None,
                 pad=0.4, borderpad=0.5, ppad = 0, sep=2, prop=None, 
                 frameon=True, linekw={}, **kwargs):
        if not ax:
            ax = plt.gca()
        trans = ax.get_xaxis_transform()
        size_bar = offbox.AuxTransformBox(trans)
        line = Line2D([0,length],[0,0], **linekw)
        size_bar.add_artist(line)
        txt = offbox.TextArea(label, minimumdescent=False, 
                              textprops=dict(color="black",size=14, fontweight='bold'))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)

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
    
scalebar = 1; cbar = 1; SAVE = 0
UNITS = r'Cu$_{K\alpha1}$ XRF (cts/s)'; COLOR = 'Oranges_r'
img_list = [NBL31.scan341[1,:,:-2], NBL32.scan422[1,:,:-2],NBL33.scan264[1,:,:-2],TS58A.scan385[1,:,:-2]]
Cu_cts_bounds = [150,1000,3000,1000]
#img_list = imgs
#delsEdit = dels1.copy()
#delsEdit[3] = delsEdit[3][:-1,:]

for img, bound in zip(img_list,Cu_cts_bounds):
    data = img.copy()
    data = data
    plt.figure()
    
    fig, ax = plt.subplots(figsize=(2.0, 2.0))

        
    im = ax.imshow(data, cmap=COLOR, vmin=0, vmax=bound)
    ax.axis('off')
    
    if scalebar == 1:
        ob = AnchoredHScaleBar(length=20, label="3μm", loc=2, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="black",linewidth=3))
        ax.add_artist(ob)
    

    #if cbar == 1:
        # create color bar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.1)

    fig.colorbar(im, cax=cax, orientation='vertical')
        #get color bar object
    cbar = plt.gcf().axes[-1]
        #format colorbar
    cbar.set_ylabel(UNITS, rotation=90, va="bottom", size=12, labelpad=20)
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
SAVE=0
if SAVE == 1:
    OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_NBL3\20200525 figures_rev3\xsect_exp\maps with colorbars'
    FNAME = r'\NBL31scan8_Cd2.eps'
    #plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)