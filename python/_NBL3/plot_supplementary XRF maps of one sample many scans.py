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

OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\NBL3 XRF maps'



scalebar_color = "white"
cbar_txt_size = 9

data = NBL32.maps[6:8]
idx = [6,7] # CHANGE idx TO MATCH WHAT IS IN sample.maps[] on line before

ele = ['Cu','Cd','Te','Zn','Mo']
colors = ['Oranges_r', 'Greys_r', 'Blues_r','Greens_r','Purples_r']

for maps,i in zip(data,idx):
    #data = FS3.scan344[1,:,:] #i NBL33.scan261[0,:,:]
    data1 = maps[[1,2,3,4,5],:,:-2]
    for Map,color, E in zip(data1,colors, ele):
        plt.figure()
        
        fig, ax = plt.subplots(figsize=(2,2))
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
            
        im = ax.imshow(Map, cmap=color, vmax = 1500)
        ax.axis('off')
        
        scalebar = 1
        if scalebar == 1:
            ob = AnchoredHScaleBar(size=20, label="3um", loc=4, frameon=False,
                                   pad=0.5, borderpad=1, sep=4, 
                                   linekw=dict(color=scalebar_color))
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
            cbar.set_ylabel(E+' XRF (cts/s)', rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
                # change number of tick labels on colorbar
            #cbar.locator_params(nbins=4)
                #change colorbar tick label sizes
            cbar.tick_params(labelsize=cbar_txt_size)
                # change scale label, e.g. 1e-8
            #cbar.set_title('1e4', size=11,loc='left')
                #change color bar scale label size, e.g. 1e-8
            cbar.yaxis.get_offset_text().set(size=cbar_txt_size)
                #change color bar scale label position   
            cbar.yaxis.set_offset_position('left')

        
        FNAME = r'\NBL32scan{s}_{e}.eps'.format(s=str(NBL32.scans[i]),e=E) # CHANGE SAMPLE
        print(FNAME)
        #plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)


