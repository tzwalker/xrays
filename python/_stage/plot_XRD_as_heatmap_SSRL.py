"""
coding: utf-8

tzwalker
Tue Nov  2 12:17:01 2021

this program is meant to plot the XRD (80C) vs time data
see the XYE files in
"Z:\BertoniLab\Synchrotron Data\2021_10_BL2-1\raw_data"

"""

# this cell imports the data
import numpy as np
scans = [20,25,30,45,60,75,90,170,245,320,390,460,535]
scans_str = [str(s) for s in scans]

PATH = r'Z:\BertoniLab\Synchrotron Data\2021_10_BL2-1\raw_data\CSET82p3_80C_2_scan'

# import XRD intensities for scans at 80C
intensities = []
for scan_str in scans_str:
    DATAFILE = PATH + "{s}.xye".format(s=scan_str)
    data = np.loadtxt(DATAFILE)
    intensities.append(data[:,1])

# import XRD intensities for final scan at room temperature
DATAFILE2 = r"Z:\BertoniLab\Synchrotron Data\2021_10_BL2-1\raw_data\CSET82p3_roomtemp_final_xrd_scan1.xye"
data2 = np.loadtxt(DATAFILE)

# add final room temp scan to 80C scans
intensities.append(data2[:,1])

z = np.array(intensities).T


#%%
'''this cell plots the heatmap'''

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import  matplotlib.ticker as tkr

# define theta array
    # uses last loaded scan
    # in my case this is the same for all scans
    # will not work if range and step are not the same for all scans
theta_arr = data[:,0]
theta_step = 0.01

# define time array
    # should corresond to the scan index
    # zero must be added here to account for pcolormesh
times = [0.5, 0.75, 1,2,3,4,5,10,15,20,25,30,35,38]

# contruct time and theta axes
    # column 0 in data is 2theta
    # time is defined by user
x,y = np.meshgrid(times, theta_arr+theta_step)

fig, ax = plt.subplots(figsize=(3.54,2.75))
ax.set_yscale('log')
cs = ax.pcolormesh(y, x, z, norm=colors.LogNorm(vmin=z.min(), vmax=z.max()),cmap='gray')

x_range = [15.70,16.0]
x_arr = np.array(x_range)

for time in times:
    ax.plot(x_arr, (time, time), 'k:', linewidth=1)

plt.xlim(x_range)

ax.set_yticks([1, 10])
ax.yaxis.set_major_formatter(tkr.ScalarFormatter())

ax.yaxis.set_minor_locator(plt.FixedLocator([5,20,35]))
ax.yaxis.set_minor_formatter(plt.FormatStrFormatter('%d'))

plt.xlabel('2\u03B8 (\u00B0)', size=11)
ax.xaxis.set_tick_params(labelsize=11)
plt.ylabel('Time (hr)', size=11)
ax.yaxis.set_tick_params(labelsize=11)

cbar = fig.colorbar(cs)
cbar.set_label('Intensity (cts/s)', rotation=90)

OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\insitu_subfigures'
FNAME = r'\111peak_vs_time.pdf' 
plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)