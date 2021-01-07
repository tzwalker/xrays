"""
coding: utf-8

tzwalker
Wed Jan  6 20:23:51 2021

this program is intended to make the base XBIC, Cu XRF, and Te XRF images

it overlays the Cu on the Te XRF, and plots the color bars above the image

the Cu response is quite noisy after masking and will be Gaussian filtered
before overlaying

the XBIC responses should be normalized (max-min stretch) to facilitate
comparison

# change font of labels
#plt.rcParams["font.family"] = "arial"

# experiment with color scales of NBL33 and TS58A

# apply gaussian filter to Cu images before overlaying

# max-min strech XBIC before plotting each
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.axes_grid1 import make_axes_locatable


xbic = NBL31.scan341[0,:,:-2]
Cu = NBL31.scan341[1,:,:-2]
Te = NBL31.scan341[3,:,:-2]

Cu1 = Cu.copy()
Cu1[Cu1<0.15]=np.nan
Te1 = Te.copy()
#Te1[Te1<10]=np.nan

fig,axs = plt.subplots()
axs.axis('off')

pltTe = axs.imshow(Te1, cmap='bone',
                   vmin=5,vmax=30,
                   alpha=1)

pltCu = axs.imshow(Cu1, cmap='Oranges_r',
                   vmin=0.15,vmax=0.30,
                   alpha=0.75)


divider = make_axes_locatable(axs)

cax = divider.new_vertical(size='5%', pad=0.5)
fig.add_axes(cax)
fig.colorbar(pltTe, cax=cax, orientation='horizontal', label='Te (ug/cm2)')

cax1 = divider.new_vertical(size='5%', pad=0)
fig.add_axes(cax1)
fig.colorbar(pltCu, cax=cax1, orientation='horizontal', label='Cu (ug/cm2)')
cax1.xaxis.set_label_position('top')
cax1.xaxis.set_ticks_position('top')


#cbCu = plt.colorbar(pltCu)
#cbTe = plt.colorbar(pltTe)
#from mpl_toolkits.axes_grid1.inset_locator import inset_axes
#axins1 = inset_axes(axs,width="100%",  # width = 50% of parent_bbox width height="5%",  # height : 5%,loc='upper center')
#axins1.xaxis.set_ticks_position("top")
#fig.colorbar(pltTe, ax=axs, orientation="horizontal",location='bottom')


# position of colorbar
# where arg is [left, bottom, width, height]
#cax = fig.add_axes([0.15, .87, 0.35, 0.03])
#fig.colorbar(surf, orientation='horizontal', cax=cax)



#%%
xbic = NBL32.scan422[0,:,:-2]
Cu = NBL32.scan422[1,:,:-2]
Te = NBL32.scan422[3,:,:-2]

Cu1 = Cu.copy()
Cu1[Cu1<0.75]=np.nan
Te1 = Te.copy()
#Te1[Te1<10]=np.nan

fig,axs = plt.subplots()
axs.axis('off')

pltTe = axs.imshow(Te1, cmap='bone',
                   vmin=0,vmax=30,
                   alpha=1)

pltCu = axs.imshow(Cu1, cmap='Oranges_r',
                   vmin=0.5,vmax=2,
                   alpha=0.75)


divider = make_axes_locatable(axs)

cax = divider.new_vertical(size='5%', pad=0.5)
fig.add_axes(cax)
fig.colorbar(pltTe, cax=cax, orientation='horizontal', label='Te (ug/cm2)')

cax1 = divider.new_vertical(size='5%', pad=0)
fig.add_axes(cax1)
fig.colorbar(pltCu, cax=cax1, orientation='horizontal', label='Cu (ug/cm2)')
cax1.xaxis.set_label_position('top')
cax1.xaxis.set_ticks_position('top')


