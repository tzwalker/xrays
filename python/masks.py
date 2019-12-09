"""
tzwalker
Sun Dec  8 20:38:13 2019
coding: utf-8
"""
from skimage import io
from scipy.stats import spearmanr
import numpy as np; import pandas as pd
import seaborn as sns; import matplotlib.pyplot as plt

SAMP = NBL3_2; SCAN = 0
NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Zn']
# bound_0in_2out_mask
# cores_0in_mask
IMG_PATH = r'Z:\Trumann\XRF images\py_exports_interface\{sample}\scan{scan_idx}'.format(sample=SAMP['Name'], scan_idx=SAMP['XBIC_scans'][SCAN])
MASKFILE = IMG_PATH + r'\bound_0in_2out_mask.txt' # <-- CORES OR BOUNDARIES 
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
        
def plot_spearman(array, cols, f, axis):
    df = pd.DataFrame(array, columns=cols, index=cols)
    sns.set(style="white") # set style of seaborn objects
    mask = np.zeros_like(df, dtype=np.bool) # make mask of symmetric portion
    mask[np.triu_indices_from(mask)] = True # apply mask
    sns.heatmap(df, mask=mask, ax=axis, cmap=f['color'], annot=True, 
                vmin=f['vs'][0], vmax=f['vs'][1], 
                cbar_kws={'label': f['cbar_title']})
    return

fig, (ax0,ax1) = plt.subplots(2,1)
plt.tight_layout()
format_dict0 = {'color': 'coolwarm', 'vs':[-1,1], 'cbar_title': 'Spearman Coeff.'}
format_dict1 = {'color': 'Greys', 'vs':[0,1], 'cbar_title': 'p-value'}
plot_spearman(corr[0], NAMES, format_dict0, ax0)
plot_spearman(corr[1], NAMES, format_dict1, ax1)