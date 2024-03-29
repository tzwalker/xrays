# -*- coding: utf-8 -*-
"""

Trumann
Fri Jun  3 17:27:30 2022

this cell is for GROD histograms from images given on 20220601


"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
PATH_0hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD\Image 1_PVSe33.3_2_No stress Specimen 1 FIB marks on the right Map Data 4-GROD-Ang.csv"
PATH_500hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD\Image 4_PVSe33.4_3_Stressed Specimen 1 Site 2_FIB marks on right Map Data 2-GROD-Ang.csv"

# import data - 0hr
no_stress = pd.read_csv(PATH_0hr, skiprows=[1])
kam = no_stress.pivot(index="Y",columns="X", values="GROD Angle")
kam = kam.to_numpy()
# orient image same way as EBSD tif and ToF-SIMS map
mirror1 = np.fliplr(kam) # flips along vertical axis
mirror2 = np.flipud(mirror1) # flip along horizontal axis

#check
fig, ax = plt.subplots()
ax.imshow(mirror2,vmax=3)
#ax.axis("off")
#ax.add_patch(Rectangle((15, 140), 40, 40, linestyle = 'solid', facecolor="none", ec='w', lw=1))

#%%
# import data - 500hr
stress = pd.read_csv(PATH_500hr, skiprows=[1])
kam = stress.pivot(index="Y",columns="X", values="GROD Angle")
mirror1 = np.fliplr(kam) # flips along vertical axis
mirror2 = np.flipud(mirror1) # flip along horizontal axis
#check
plt.figure()
plt.imshow(mirror2, vmax = 3)
plt.axis("off")
#%%
# convert dataframes to numpy arrays
a = no_stress.to_numpy()
b = stress.to_numpy()

# get KAM values
a1 = a[:,3].copy()
b1 = b[:,3].copy()

not_nan0hr = np.count_nonzero(~np.isnan(a1)) # number of pixels that are not NaN
print("number of nonNaN pxels in 0hr GROD image: {s}".format(s=str(not_nan0hr)))
not_nan500hr = np.count_nonzero(~np.isnan(b1)) # number of pixels that are not NaN
print("number of nonNaN pxels in 500hr GROD image: {s}".format(s=str(not_nan500hr)))

# calculate number of bins
# https://stats.stackexchange.com/questions/798/calculating-optimal-number-of-bins-in-a-histogram
# Freedman-Diaconis rule
def find_bins(data):
    q75, q25 = np.nanpercentile(data, [75 ,25])
    iqr = q75 - q25
    n = int(data.shape[0])
    h = 2*iqr*n**(-1/3)
    no_of_bins = (np.nanmax(data)-np.nanmin(data)) / h
    return int(no_of_bins)

abins = find_bins(a1)
bbins = find_bins(b1)

# take whichever is lesser
if abins < bbins:
    hbins = abins
elif bbins < abins:
    hbins = bbins

print("number of bins in histogram: {s}".format(s=str(hbins)))
#%%
# plot histograms
import matplotlib as mpl

from typing import Optional


def restore_minor_ticks_log_plot(
    ax: Optional[plt.Axes] = None, n_subticks=9
) -> None:
    """For axes with a logrithmic scale where the span (max-min) exceeds
    10 orders of magnitude, matplotlib will not set logarithmic minor ticks.
    If you don't like this, call this function to restore minor ticks.

    Args:
        ax:
        n_subticks: Number of Should be either 4 or 9.

    Returns:
        None
    """
    if ax is None:
        ax = plt.gca()
    # Method from SO user importanceofbeingernest at
    # https://stackoverflow.com/a/44079725/5972175
    locmaj = mpl.ticker.LogLocator(base=10, numticks=1000)
    ax.yaxis.set_major_locator(locmaj)
    locmin = mpl.ticker.LogLocator(
        base=10.0, subs=np.linspace(0, 1.0, n_subticks + 2)[1:-1], numticks=1000
    )
    ax.yaxis.set_minor_locator(locmin)
    ax.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    
SAVE = 0
fig, (ax1,ax2) = plt.subplots(figsize=(2.5,3),nrows=2,ncols=1,sharex=True)

ax1.hist(a1, color = "grey", alpha = 0.5, bins = hbins, label='0hr', log=True) # 0hr
ax1.set_ylim(1,1e5)
ax1.set_ylabel("Pixel Count")
restore_minor_ticks_log_plot(ax1,n_subticks=4)

ax2.hist(b1, color = "red", alpha = 0.5, bins = hbins, label = '500hr', log=True) # 500hr
ax2.set_ylim(1,1e5)
ax2.set_xlabel(u"GROD Angle (\u00b0)")
ax2.set_ylabel("Pixel Count")
#ax2.set_xticks(np.arange(0,20,4))
ax2.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator()) 
ax2.tick_params(which='minor', length=2)
ax2.set_xlim(-0.1,1) # comment out for no thresholding

restore_minor_ticks_log_plot(ax2,n_subticks=4)

if SAVE == 1:
        OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_EBSD'
        FNAME = r'\GROD_hist_thresholded.pdf'
        plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)