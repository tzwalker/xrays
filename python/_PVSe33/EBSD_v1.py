# -*- coding: utf-8 -*-
"""

Trumann
Tue Jun  7 09:03:06 2022

this is meant to analyze the EBSD images - i think it is less confusing 
to import/analyze EBSD data separately from the ToF-SIMS

i can alter the images in separate files, then combine the altered images in
a final file

"""

from skimage import io
import matplotlib.pyplot as plt

PATH_EBSD = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD\0hr_right_map.tif"

# import EBSD tiff
# (x,y,color_value)
EBSD = io.imread(PATH_EBSD)

# mask green (101) direction, it is confused with fiducials
green = EBSD[:,:,1]
# mask FIB marks [rows,columns,green_channel]
green[10:60,10:60] = 0 # top-left 
green[10:60,435:485] = 0 # top-right 
green[395:445,25:75] = 0 # bottom-left 
green[380:430,460:510] = 0 # bottom-left 

EBSD[:,:,1] = green

# convert EBSD image to grayscale
# =============================================================================
# EBSD_gray = EBSD.copy()
# #rgb_to_gray = lambda rgb : np.dot(rgb[... , :3] , [0.299 , 0.587, 0.114])
# rgb_to_gray = lambda rgb : np.dot(rgb[... , :3] , [0.299 , 0, 0.114])
# EBSD_gray = rgb_to_gray(EBSD_gray)
# 
# #check
# #plt.imshow(EBSD_gray,cmap='inferno')
# plt.imshow(EBSD_gray)
# plt.axis('off')
# =============================================================================

import matplotlib.ticker as mticker

SAVE = 0

cbar_txt_size = 11
scalebar_color = 'black'


fig, ax = plt.subplots(figsize=(2.5,2.5))

im = ax.imshow(EBSD)

fmtr_x = lambda x, pos: f'{(x * 0.100):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.100):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)',size=cbar_txt_size)
ax.set_ylabel('$Y$ (μm)',sie=cbar_txt_size)

if SAVE == 1:
        OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_EBSD'
        FNAME = r'\EBSD_out.pdf'
        plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)