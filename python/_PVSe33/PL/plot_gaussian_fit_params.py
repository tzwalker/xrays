"""
coding: utf-8

tzwalker
Tue Mar 23 17:08:43 2021

this program is meant to be run after map_analysis_PL

it assumes a set of gaussian fit parameters have been obtained for
each pixel in a PL map, and these parameters have been saved to a csv file

it allows the user to specify a gaussian fit parameter and plot it as
a function of x and y coordinate

EDIT 20220628: 
    the 500hr Au map glitched and does not have the final pixel
    it only has 960 pixels (not 961)
    therefore the last row (30 pixels) need to be removed
    so the data can be shaped into a 31*30 array
    
"""

import pandas as pd
import matplotlib.pyplot as plt

# specify import file
FILE = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\PL\gaussian fit params - 20210304 PVSe33.3_2 Au Side_PL_map0.csv"
 
# import file array
    # 2D array, rows --> number of pixels, cols --> gaussian fit parameter
fit_params = pd.read_csv(FILE, delimiter=',', header=None)
fit_params = fit_params.to_numpy()

# specify parameter 
    #0: offset, 1: amplitude, 2: energy position, 3: width
fit_param = 1

# extract parameter for each pixel
relevant_data = fit_params[:,fit_param]

# reshape into map shape
    # note this shape must be known a priori
    # it can be found by viewing the shape of 'reader.spectra' of wdf file
        # x --> number of columns in wdf file
        # y --> number of rows in wdf file

# specify the number of rows and columns
x = 31
y = 31
param_map = relevant_data.reshape(y,x)

#%%
'''this cell is for plotting purposes'''
import matplotlib.ticker as mticker

SAVE = 0
if fit_param == 1:
    unit = 'Intensity (cts/s)'
    
img = param_map.copy()
cbar_txt_size = 11

fig, ax = plt.subplots(figsize=(2.5,2.5))

im = ax.imshow(img, cmap='viridis', vmin = 0, vmax = 1000, origin='lower')

fmtr_x = lambda x, pos: f'{(x * 1.0):.0f}'
fmtr_y = lambda x, pos: f'{(x * 1.0):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)',size=cbar_txt_size)
ax.set_ylabel('$Y$ (μm)',size=cbar_txt_size)

# format and add colorbar
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))

cax1 = fig.add_axes([ax.get_position().x1+0.025,ax.get_position().y0,0.025,ax.get_position().height])
cbar = fig.colorbar(im, cax=cax1)#, format=fmt)
cbar.ax.set_ylabel(unit, rotation=90, 
                   va="bottom", size=cbar_txt_size, labelpad=15)
cbar.ax.yaxis.set_offset_position('left')

if SAVE == 1:
        OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_renishaw'
        FNAME = r'\0hr_Au_PL_fitAmplitude.pdf'
        plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)
