"""
tzwalker
Sun Dec  8 20:38:13 2019
coding: utf-8
"""
# imports the relevant mask and plots spearman correlation of data within that
    # mask / mask filename determiens whether cores or boundaries are considered
    # mask made in imagej and saved on the server
from skimage import io
from scipy.stats import spearmanr
import numpy as np; import pandas as pd
import seaborn as sns; import matplotlib.pyplot as plt

SAMP = NBL3_3; SCAN = 0
NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Zn']
# bound_0in_2out_mask
# cores_0in_mask
IMG_PATH = r'Z:\Trumann\XRF images\py_exports_interface\{sample}\scan{scan_idx}'.format(sample=SAMP['Name'], scan_idx=SAMP['XBIC_scans'][SCAN])
MASKFILE = IMG_PATH + r'\cores_0in_mask.txt' # <-- CORES OR BOUNDARIES \bound_0in_2out_mask
mask_core = np.loadtxt(MASKFILE)

USE_TIFS = 0
if USE_TIFS ==1:
    IMGS = []
    for channel in NAMES:
        img_name = IMG_PATH + '\\' + channel + '.tif'
        img = io.imread(img_name)
        IMGS.append(img)
    enh_maps = np.array(IMGS)
    pre_l = []
    for z in range(np.shape(enh_maps)[0]):
        enh_map = enh_maps[z,:,:]
        desired_data = enh_map[np.where(mask_core!=0)]
        pre_l.append(desired_data)
    pre_corr =np.array(pre_l).T
    corr = spearmanr(pre_corr)
else:
    maps = SAMP['XBIC_maps'][SCAN]
    pre_l = []
    for z in range(np.shape(maps)[0]):
        m = maps[z,:,:]
        desired_data = m[np.where(mask_core!=0)]
        pre_l.append(desired_data)
    pre_corr =np.array(pre_l).T
    corr = spearmanr(pre_corr)
        
def plot_spearman(array, cols, f, axis, annotate):
    df = pd.DataFrame(array, columns=cols, index=cols)
    sns.set(style="white") # set style of seaborn objects
    mask = np.zeros_like(df, dtype=np.bool) # make mask of symmetric portion
    mask[np.triu_indices_from(mask)] = True # apply mask
    sns.heatmap(df, mask=mask, ax=axis, cmap=f['color'], annot=annotate, 
                vmin=f['vs'][0], vmax=f['vs'][1], 
                cbar_kws={'label': f['cbar_title'], 'ticks':f['cbar_ticks']})
    return

fig, (ax0,ax1) = plt.subplots(2,1)
plt.tight_layout()
format_dict0 = {'color': 'coolwarm', 'vs':[-1,1], 'cbar_ticks':list(np.arange(-1,1.25,.5)), 
                'cbar_title': 'Spear. Coeff.'}
format_dict1 = {'color': 'Greys', 'vs':[0,1], 'cbar_title': 'p-value'}
plt.figure()
plot_spearman(corr[0], NAMES, format_dict0, ax0, False)
#plot_spearman(corr[1], NAMES, format_dict1, ax1)

#%%
# comparing background substractions: ImageJ vs. python
from skimage import io
import scipy.ndimage as scim
from skimage.morphology import ball
import matplotlib.pyplot as plt

# comparison before python correction #
imgj = io.imread(r'Z:\Trumann\XRF images\py_exports_interface\NBL3_2\scan422\XBIC.tif')
imgp = NBL3_2['XBIC_maps'][0][0,:,:-2]
fig, (ax0,ax1) = plt.subplots(1,2)
ax0.imshow(imgp)
ax1.imshow(imgj)
#%%
# python correction# 
s = ball(15) # Create 3D ball structure
h = int((s.shape[1] + 1) / 2) # Take only the upper half of the ball
s = s[:h, :, :].sum(axis=0) # Flat the 3D ball to a weighted 2D disc
s = (1 * (s - s.min())) / (s.max()- s.min()) # Rescale weights into 0-1
# Use im-opening(im,ball) (i.e. white tophat transform) (see original publication)
imgp_corr = scim.white_tophat(imgp, structure=s)
fig, (ax0,ax1) = plt.subplots(1,2)
ax0.imshow(imgp)
ax1.imshow(imgp_corr)