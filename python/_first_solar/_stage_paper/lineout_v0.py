# -*- coding: utf-8 -*-
"""

Trumann
Wed Mar 16 09:31:16 2022

run "fig4_get_plot_XRF.py" before this file

this program extends the analysis done for the stage paper

a reviewer suggested lineouts - draw a line on the map, then plot the line
to the side of the map - to compare across temperatures

i tried doing this with the Au channel, but the lines to not look
very similar, despite seeing the same features in the map

the problem is there is a distortion along the vertical axis

this distortion was not accounted for using the SIFT translation in ImageJ

"""

from scipy.ndimage.filters import gaussian_filter1d
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

lineout_20 = aligned_crop[0][4,58,:]
lineout_80 = aligned_crop[1][4,58,:]

# plot line plot of at the same index as the line out
fig, ax = plt.subplots(figsize=(3.6,3.6))
ax.plot(lineout_20, label='20C')
ax.plot(lineout_80, label='80C')
ax.set_ylim([9,16])
ax.legend()

fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))

ax.set_xlabel("X (um)")

ax.set_ylabel("Au XRF (arb. unit)")

# smooth lineout
x = np.array(list(range(0,len(lineout_20))))
# =============================================================================
# from scipy.interpolate import make_interp_spline, BSpline
# 
# # 300 represents number of points to make between T.min and T.max
# 
# xnew = np.linspace(x.min(), x.max(), 386) 
# 
# spl = make_interp_spline(x,lineout, k=3)  # type: BSpline
# power_smooth = spl(xnew)
# plt.plot(xnew,power_smooth)
# =============================================================================

ysmoothed = gaussian_filter1d(lineout_20, sigma=1)
ysmoothed1 = gaussian_filter1d(lineout_80, sigma=1)

fig, ax = plt.subplots(figsize=(3.6,3.6))
ax.plot(x, ysmoothed, label='20C - smoothed')
ax.plot(x, ysmoothed1, label='80C - smoothed')
# despite the similarities by eye, the lineouts are very different
    # even for easily seen features
    # this is probably due to the distortion along the y axis
    # between the 20C and 80C image
    # try a horizontal lineout
ax.set_ylim([9,16])
#ax.set_ylim([0.85,1.4])
ax.legend()

fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))

ax.set_xlabel("X (um)")

ax.set_ylabel("Au XRF (arb. unit)")