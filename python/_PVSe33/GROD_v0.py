# -*- coding: utf-8 -*-
"""

Trumann
Fri Jun  3 17:27:30 2022

this cell is for GROD histograms from images given on 20220601


"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
PATH_0hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD\Image 1_PVSe33.3_2_No stress Specimen 1 FIB marks on the right Map Data 4-GROD-Ang.csv"
PATH_500hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD\Image 4_PVSe33.4_3_Stressed Specimen 1 Site 2_FIB marks on right Map Data 2-GROD-Ang.csv"

# import data - 0hr
no_stress = pd.read_csv(PATH_0hr, skiprows=[1])
kam = no_stress.pivot(index="Y",columns="X", values="GROD Angle")
# orient image same way as EBSD tif and ToF-SIMS map
mirror1 = np.fliplr(kam) # flips along vertical axis
mirror2 = np.flipud(mirror1) # flip along horizontal axis

#check
plt.figure()
plt.imshow(mirror2, vmax = 3)
plt.axis("off")

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
plt.figure()
plt.hist(a1, color = "grey", alpha = 0.7, bins = hbins, label='0hr', log=True) # 0hr
plt.hist(b1, color = "red", alpha = 0.3, bins = hbins, label = '500hr', log=True) # 500hr
plt.ylim(1,1e5)

plt.legend()
plt.xlabel("GROD Angle (degree)")
plt.ylabel("Pixel Count")