"""
this file is meant to plot the maps we took at different energy
steps across the Cu absorption edge

these areas will be used to justify the Cu distribution is unlikely to
change during irradation up to 42min, and the integral specturm will be
included in the supplementary graph in further support
"""

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.offsetbox as offbox
from matplotlib.lines import Line2D

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

ASCII_PATH = r'C:\Users\triton\Dropbox (ASU)\2_xray\xray fitting data\2017_12_2IDD_XANES\ASCIIs'
SCANS = [423,424] + list(range(426,433))
OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\supplementary\XANES intspec - prove Cu does not move\TS58A 2017_12_2IDD'

for scan in SCANS:
    scan_str = str(scan)
    # define ascii of scan
    file = ASCII_PATH + '/combined_ASCII_2idd_0'+scan_str+'.h5.csv'
    # import ascii as dataframe
    data = pd.read_csv(file, skiprows=1)
    # dataframe keys used for shaping into map
    i = ' y pixel no'; j='x pixel no'
    # extract maps of interest; shape according to pixel no
    data_shape = data.pivot(index=i, columns=j, values=" Cu")
    # convert dataframes to numpy arrays
    data_arr = data_shape.to_numpy()

    fig, ax = plt.subplots(figsize=(5,5))
    
    im = ax.imshow(data_arr[:,:-2], cmap="Oranges_r")
    ax.axis('off')

    scalebar = 1
    if scalebar == 1:
        ob = AnchoredHScaleBar(size=50, label="5 um", loc=2, frameon=True,
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
        cbar.set_ylabel('Cu (ug/cm2)', rotation=90, va="bottom", size=12, labelpad=20)
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
    FNAME = r'\scan{s}_Cu.png'.format(s=scan_str)
    #print(OUT_PATH+FNAME)
    plt.savefig(OUT_PATH+FNAME, format='png', bbox_inches='tight', pad_inches = 0) #, dpi=300, )

