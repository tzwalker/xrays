# -*- coding: utf-8 -*-
"""

Trumann
Thu Jul 21 11:33:19 2022

run 0hr and 500hr "ToFSIMS_v5" files before this program

this program plots histograms of Cl quantities at the GB masks

it uses the masks from a part of the 0hr and 500hr CdSeTe layers that
should have about the same grain size
    the integration begins at about 3um away from the TCO, and ends around 2um away from the TCO

"""

import matplotlib.pyplot as plt

txt_size = 11

#_, bin_bounds = np.histogram(np.log10(valarr), bins='auto')

hbins = 20
bin_bounds = list(np.arange(1e18,5e20,0.1e20))
#bin_bounds = [1e18,1e19,1e20,1e21]
fig, (ax1,ax2) = plt.subplots(nrows=2,ncols=1,sharex=True)

ax1.hist(valarr, color = "grey", alpha = 0.5, bins=bin_bounds, label='0hr', log=True) # 0hr
ax1.set_ylim(0.1,1e5)
ax1.legend(fontsize=txt_size)
ax1.set_ylabel("Pixel Count",size=txt_size)
ax1.tick_params(labelsize=txt_size)

ax2.hist(valarr1, color = "red", alpha = 0.5, bins=bin_bounds, label = '500hr', log=True) # 500hr
ax2.set_ylim(0.1,1e5)
ax2.legend(fontsize=txt_size)
ax2.set_xlabel("Cl (atom/cm$^3$)",size=txt_size)
ax2.set_ylabel("Pixel Count",size=txt_size)
ax2.tick_params(labelsize=txt_size)
#plt.xscale('log')


OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps'
FNAME = r'\PVSe33_Cl_at_GB_histgrams_quant.pdf'
#plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)
