# -*- coding: utf-8 -*-
"""

Trumann
Wed Aug 17 13:23:26 2022

this program is meant to plot the Cl density at the grain boundaries
for an intergated map near the Au side and
and integrated map near the TCO side

the Au side maps and masks were constructed from running the 'v5' programs
the TCO side maps and masks were constructed from running the 'v6' programs

the masks were saved as txt files for use in this file

"""
from skimage import io
import numpy as np

# define filenames
file1 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Cl_maps_quantified.tif"
file2 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Cl_maps_quantified.tif" 

maskfile_Au_0hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Au_mask_8537px.txt"
maskfile_Au_500hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Au_mask_8525px.txt"
maskfile_TCO_0hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_TCO_mask_10043px.txt"
maskfile_TCO_500hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_TCO_mask_10164px.txt"

# import ToF-SIMS images
imgs1 = io.imread(file1)
imgs2 = io.imread(file2)

# import masks
mskAu_0 = np.loadtxt(maskfile_Au_0hr)
mskAu_500 = np.loadtxt(maskfile_Au_500hr)
mskTCO_0 = np.loadtxt(maskfile_TCO_0hr)
mskTCO_500 = np.loadtxt(maskfile_TCO_500hr) 


# get pertinent integrations from data
iAu_0 =     imgs1[1:10,:,:].sum(axis=0)
iAu_500 =   imgs2[1:10,:,:].sum(axis=0)
iTCO_0 =    imgs1[39-18-9:39-18,:,:].sum(axis=0)
iTCO_500 =  imgs2[44-15-8:44-15,:,:].sum(axis=0)

# get masked data for histograms
a = mskAu_0     *   iAu_0
b = mskAu_500   *   iAu_500
c = mskTCO_0    *   iTCO_0
d = mskTCO_500  *   iTCO_500

data = [a,b,c,d]
plot_data = [img.ravel() for img in data]

#%%
import matplotlib.pyplot as plt

txt_size = 11

#_, bin_bounds = np.histogram(np.log10(valarr), bins='auto')

hbins = 20
bin_bounds = list(np.arange(1e18,5e20,0.1e20))
#bin_bounds = [1e18,1e19,1e20,1e21]

fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2,ncols=2,sharex=True, sharey=True)

ax1.hist(plot_data[0], color = "grey", alpha = 0.5, bins=bin_bounds, label='0hr - Au', log=True) # 0hr
#ax1.set_ylim(0.1,1e5)
ax1.set_ylim(0.5,1e4)
ax1.legend(fontsize=txt_size)
ax1.set_ylabel("Pixel Count",size=txt_size)
ax1.tick_params(labelsize=txt_size)

ax3.hist(plot_data[1], color = "red", alpha = 0.5, bins=bin_bounds, label = '500hr - Au', log=True) # 500hr
#ax2.set_ylim(0.1,1e5)
ax3.legend(fontsize=txt_size)
ax3.set_xlabel("Cl (atom/cm$^3$)",size=txt_size)
ax3.set_ylabel("Pixel Count",size=txt_size)
ax3.tick_params(labelsize=txt_size)
#plt.xscale('log')

ax2.hist(plot_data[2], color = "grey", alpha = 0.5, bins=bin_bounds, label = '0hr - TCO', log=True) # 500hr
#ax2.set_ylim(0.1,1e5)
#ax3.set_ylim(0,2)
#ax3.set_xlim(2e20,5e20)
ax2.legend(fontsize=txt_size)
ax2.set_ylabel("Pixel Count",size=txt_size)
ax2.tick_params(labelsize=txt_size)
#plt.xscale('log')

ax4.hist(plot_data[3], color = "red", alpha = 0.5, bins=bin_bounds, label = '500hr - TCO', log=True) # 500hr
#ax2.set_ylim(0.1,1e5)
#ax4.set_ylim(0,2)
#ax4.set_xlim(2e20,5e20)
ax4.legend(fontsize=txt_size)
ax4.set_xlabel("Cl (atom/cm$^3$)",size=txt_size)
ax4.set_ylabel("Pixel Count",size=txt_size)
ax4.tick_params(labelsize=txt_size)
#plt.xscale('log')


OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps'
FNAME = r'\PVSe33_Cl_at_GB_histgrams_quant.pdf'
#plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)