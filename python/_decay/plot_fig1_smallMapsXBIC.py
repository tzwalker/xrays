"""
coding: utf-8

tzwalker
Sat Sep 11 10:35:30 2021

2022 04 19
this program was used to get the smaller maps in figure 1 of paper
data from scans 195 and 196 2018_11_26IDC


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

        size_bar.add_artist(line)

        txt = offbox.TextArea(label, textprops=dict(color=scalebar_color,weight='bold',size=cbar_txt_size))
        self.vpac = offbox.VPacker(children=[size_bar,txt], align="center", pad=ppad, sep=sep)
        
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)


SAVE = 1
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_XBIC_decay\figures v1\figure1 materials'
FNAME = r'\TS118_1A_scan195_XBIC_v2.eps'

scalebar_color = 'white'

# SET SCALE BAR
px = 12; dist = u'3\u00B5m'

cbar_txt_size = 11

cbar_scale_control = 0; MAX = 250; MIN = 0

unit = 'XBIC (nA)'; colormap='inferno'

# filter image
img0 = TS1181A.scan195[0,:,:] 
data0 = img0.copy()
data0 = data0 * 1e9

plt.figure()
fig, ax = plt.subplots(figsize=(2.5,2.5))

im = ax.imshow(data0,cmap=colormap)

ax.axis('off')
ob = AnchoredHScaleBar(size=px, label=dist, loc=4, frameon=False,
                       pad=0.1, borderpad=0.5, sep=4, 
                       linekw=dict(color=scalebar_color))
ax.add_artist(ob)

# plot crosshairs at specific positions
# scan 195 indices
#plt.scatter([14,16,31], [18,32,20], marker='+', s=50, color='white')

# create color bar
divider = make_axes_locatable(ax)    

cax = divider.append_axes('right', size='5%', pad=0.1)
fmt = ticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cb = fig.colorbar(im, cax=cax, orientation='vertical',format=fmt)
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
    

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)

#%%
SAVE = 1
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_XBIC_decay\figures v1\figure1 materials'
FNAME = r'\TS118_1A_scan196_XBIC_v2.eps'

# filter image
img1 = TS1181A.scan196[0,:,:] 
data1 = img1.copy()
data1 = data1 * 1e9


plt.figure()
fig, ax = plt.subplots(figsize=(2.5,2.5))

im = ax.imshow(data1,cmap=colormap)

ax.axis('off')
ob = AnchoredHScaleBar(size=px, label=dist, loc=4, frameon=False,
                       pad=0.1, borderpad=0.5, sep=4, 
                       linekw=dict(color=scalebar_color))
ax.add_artist(ob)

# plot crosshairs at specific positions
# scan 196 indices
#plt.scatter([27,5,10], [16,4,24], marker='x', s=50, color='white')

# create color bar
divider = make_axes_locatable(ax)    

cax = divider.append_axes('right', size='5%', pad=0.1)
fmt = ticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cb = fig.colorbar(im, cax=cax, orientation='vertical',format=fmt)
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
    

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)