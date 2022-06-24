# -*- coding: utf-8 -*-
"""

Trumann
Fri Jun 24 09:53:18 2022

this program is meant to plot the KAM data

"""

import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def match_tof_orientation(dataframe):
    mirror1 = np.fliplr(dataframe)
    mirror2 = np.flipud(mirror1)
    mirror2 = np.nan_to_num(mirror2)    
    return mirror2

PATH_0hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD\Image 2_PVSe33.3_2_No stress Specimen 1 FIB marks on the right Map Data 4-KAM.csv"
PATH_500hr = r"C:/Users/Trumann/Dropbox (ASU)/1_PVSe33 ex-situ/DATA/EBSD/Image 5_PVSe33.4_3_Stressed Specimen 1 Site 2_FIB marks on right Map Data 2-KAM.csv"

# import data - 0hr
no_stress = pd.read_csv(PATH_0hr, skiprows=[1])
kam0 = no_stress.pivot(index="Y",columns="X", values="Kernel Average Misorientation")
# orient image same way as EBSD tif and ToF-SIMS map
kam0 = match_tof_orientation(kam0)

# import data - 500hr
stress = pd.read_csv(PATH_500hr, skiprows=[1])
kam500 = stress.pivot(index="Y",columns="X", values="Kernel Average Misorientation")
kam500 = match_tof_orientation(kam500)

# check
plt.figure()
plt.imshow(kam0, vmax = 1)
plt.axis("off")

plt.figure()
plt.imshow(kam500, vmax = 1)
plt.axis("off")
#%%
SAVE = 1

img = np.flipud(kam500) # flip data for display purposes

cbar_txt_size = 11

fig, ax = plt.subplots(figsize=(2.5,2.5))

im = ax.imshow(img, vmax = 1.25, origin='lower',cmap='bone')

fmtr_x = lambda x, pos: f'{(x * 0.100):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.100):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)',size=cbar_txt_size)
ax.set_ylabel('$Y$ (μm)',size=cbar_txt_size)

# format and add colorbar
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))

cax1 = fig.add_axes([ax.get_position().x1+0.025,ax.get_position().y0,0.025,ax.get_position().height])
cbar = fig.colorbar(im, cax=cax1, format=fmt)
cbar.ax.set_ylabel(u'Kernel Avgerage \n Misorientation (\u00b0)', rotation=90, 
                   va="bottom", size=cbar_txt_size, labelpad=30)
cbar.ax.yaxis.set_offset_position('left')

if SAVE == 1:
        OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_EBSD'
        FNAME = r'\500hr_KAM.pdf'
        plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)