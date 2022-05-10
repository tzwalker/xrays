"""

Trumann
Tue May 10 15:22:46 2022

for TS118_1A decay (2018_11_26IDC):
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
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker

SAVE = 1
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_XBIC_decay\supplementary\figures\S6 materials'
FNAME = r'\TS118_1Ax_scan051_Au.eps'

#unit = 'XBIC (arb. unit)'; colormap='inferno'
#unit = 'Cu ($\mu$g/cm$^2$)'; colormap = 'Oranges_r'
#unit = 'Cd ($\mu$g/cm$^2$)'; colormap = 'Blues_r'
unit = 'Au ($\mu$g/cm$^2$)'; colormap = 'YlOrBr_r'

img = data_shape[4]

cbar_txt_size = 11

cbar_scale_control = 0; MIN = 0; MAX = 250

fig, ax = plt.subplots(figsize=(5,3))

fmtr_x = lambda x, pos: f'{(x * 0.100):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.400):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)')
ax.set_ylabel('$Y$ (μm)')

im = ax.imshow(img, cmap=colormap, origin='lower')

divider = make_axes_locatable(ax)
# create color bar
cax = divider.append_axes('right', size='5%', pad=-0.75)
fmt = mticker.ScalarFormatter(useMathText=True)
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

ax.set_aspect(4)

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)