"""
tzwalker
Sun Dec  8 20:38:13 2019
coding: utf-8
"""
from skimage import io
from scipy.stats import spearmanr
import numpy as np; import pandas as pd
import seaborn as sns

SAMP = TS58A; SCAN = 1
NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Zn']

IMG_PATH = r'Z:\Trumann\XRF images\py_exports_interface\{sample}\scan{scan_idx}'.format(sample=SAMP['Name'], scan_idx=SAMP['XBIC_scans'][SCAN])
IMGS = []
for channel in NAMES:
    img_name = IMG_PATH + '\\' + channel + '.tif'
    img = io.imread(img_name)
    IMGS.append(img)
enh_maps = np.array(IMGS)

MASKFILE_CORE = IMG_PATH + r'\cores_1in_mask.txt'
MASKFILE_BOUND = IMG_PATH + r'\bound_0in_2out_mask.txt'

mask_core = np.loadtxt(MASKFILE_CORE)

pre_l = []
for z in range(np.shape(enh_maps)[0]):
    enh_map = enh_maps[z,:,:]
    desired_data = enh_map[np.where(mask_core!=0)]
    pre_l.append(desired_data)
pre_corr =np.array(pre_l).T
corr = spearmanr(pre_corr)

def get_corrmtx_plot(array, cols, f, axis, numbers):
    df = pd.DataFrame(array, columns=cols, index=cols)
    sns.set(style="white") # set style of seaborn objects
    mask = np.zeros_like(df, dtype=np.bool) # make mask of symmetric portion
    mask[np.triu_indices_from(mask)] = True # apply mask
    sns.heatmap(df, mask=mask, cbar_kws=f['cbar_format'], ax=axis,
                     cmap=f['color'], annot=numbers, vmin=f['v_range'][0], vmax=f['v_range'][1],
                     annot_kws={"fontsize":f['labs']})
    #axis.title.set_text(f['plt_title'])
    
    return
get_corrmtx_plot(corr, NAMES, format_dict, axis, True)