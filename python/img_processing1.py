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

import numpy as np
SAMP = NBL3_3; SCAN = 0
NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Zn']
# bound_0in_2out_mask
# cores_0in_mask
IMG_PATH = r'Z:\Trumann\XRF images\py_exports_interface\{sample}\scan{scan_idx}'.format(sample=SAMP['Name'], scan_idx=SAMP['XBIC_scans'][SCAN])
MASKFILE = IMG_PATH + r'\\bound_0in_1out_mask.txt' # <-- CORES OR BOUNDARIES \bound_0in_1out_mask
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
# attempt to mimic ImageJ rolling-ball background substraction #

xbic = NBL3_3['XBIC_maps'][0][3,:,:-2]
import sklearn.preprocessing as sklp
import numpy as np

scaler = sklp.StandardScaler()

def standardize_map(array):
    map_dimensions = np.shape(array)
    array = array.reshape(-1,1) # standardization requires one column
    array = scaler.fit_transform(array) # transform
    array = array.reshape(map_dimensions) # shape back into map
    return array

xbic1 = standardize_map(xbic)

import scipy.ndimage as scim
from skimage.morphology import ball

# Create 3D ball structure
s = ball(30) 
# Take only the upper half of the ball
h = int((s.shape[1] + 1) / 2)
# Flat the 3D ball to a weighted 2D disc
s = s[:h, :, :].sum(axis=0)
# Rescale weights into 0-1
s = (1 * (s - s.min())) / (s.max()- s.min()) 
# Use "white tophat" transform 
xbicbk = scim.white_tophat(xbic1, structure=s)

#%%
### exploring current/voltage maps ###
import matplotlib.pyplot as plt
import numpy as np
from home_dataTransforms import ug_to_mol
from scipy.ndimage import gaussian_filter as gfilt
samp = NBL3_2; scan_idx = 3
i = samp['XBIC_maps'][scan_idx][0,:,:-2]
v = samp['XBIV_maps'][scan_idx][0,:,:-2]

mol_cu = ug_to_mol(samp, 'XBIV_maps', scan_idx, elements, 1); molfilt_cu = gfilt(mol_cu,sigma=1)
mol_te = ug_to_mol(samp, 'XBIV_maps', scan_idx, elements, 2); molfilt_te = gfilt(mol_te,sigma=1)
mol_cute = molfilt_cu / molfilt_te

fig, (ax0, ax1) = plt.subplots(1,2)
ax0.imshow(v); ax1.imshow(mol_cute)
plt.figure()
plt.hexbin(i, v, mincnt=1)

#%%
SAMP = NBL3_2; SCAN = 0
NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Zn']
# bound_0in_2out_mask
# cores_0in_mask
IMG_PATH = r'Z:\Trumann\XRF images\py_exports_interface\{sample}\scan{scan_idx}'.format(sample=SAMP['Name'], scan_idx=SAMP['XBIC_scans'][SCAN])
MASKFILE = IMG_PATH + r'\\bound_0in_1out_mask.txt' # <-- CORES OR BOUNDARIES \bound_0in_1out_mask
mask_core = np.loadtxt(MASKFILE)