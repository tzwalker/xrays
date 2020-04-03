# -*- coding: utf-8 -*-
"""
Trumann
Wed Jan 29 13:34:11 2020

segmentation for XBIC maps as a function of temperature
Sample FS3_3: 2019_06_2IDD
XBIC
20C: scan0323
40C: scan0327
60C: scan0332
80C: scan0344
100C: scan344

XBIV
20C: scan0321
40C: scan0325
60C: scan0330
80C: scan0337
100C: scan0342
"""

from skimage.segmentation import slic, mark_boundaries
import numpy as np

img = r'C:\Users\Trumann\Desktop\FS_data\FS3_2019_06_2IDD_stage\output\combined_ASCII_2idd_0344.h5.csv'
df = pd.read_csv(img, skiprows = 1)
map_df = df.pivot(index = ' y pixel no', columns = 'x pixel no', values = ' us_ic')
map_np = map_df.to_numpy()
#plt.imshow(map_np, vmin=100000)


edges = slic(map_np, n_segments=100, compactness=5000, sigma=1)

# for some reason the boundaries from SLIC are not changing color
# initiate RGB channel to act as boundary mask
bm = mark_boundaries(map_np, edges, color=(1,0,0)) #-> color is RGB
# make boolean mask
bm_mask = bm[:,:,0] == 1
#everywhere where bm_edit is True, convert to nan
img_masked = map_np.copy(); img_masked[bm_mask] = np.nan
bm = mark_boundaries(map_np, edges, color=(1,0,0)) #-> color is RGB

# plot somehwat nicely
fig, ax1 = plt.subplots()
#ax0.imshow(map_np, cmap='magma', origin='lower', vmin=1E5)
im1 = ax1.imshow(map_np, cmap='magma', origin='lower', vmin=1E5) #bm[:,:,0]
plt.xlabel('X (\u03BCm/10)', fontsize=16)
plt.ylabel('Y (\u03BCm/10)', fontsize=16)
plt.colorbar(im1,fraction=0.046, pad=0.04)
cbar_ax = plt.gcf().axes[-1]                        #gets colorbar of current figure object, behaves as second y object
# colorbar label settings
cbar_ax.set_ylabel('cts/s', fontsize = 16, #\u03BCg/cm'+ r'$^{2}$
                   rotation = 90, labelpad = 10)   #label formatting
ax1.tick_params(labelsize = 14)
