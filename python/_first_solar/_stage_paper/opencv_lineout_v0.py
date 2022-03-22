# -*- coding: utf-8 -*-
"""

Trumann
Wed Mar 16 09:31:16 2022

run "opencv_ECC_register.py" before this file

this program extends the analysis done for the stage paper

a reviewer suggested lineouts - draw a line on the map, then plot the line
to the side of the map - to compare across temperatures

i tried doing this with the Au channel, but the lines to not look
very similar, despite seeing the same features in the map

the problem is there is a distortion along the vertical axis

this was solved using ECC algorithm - the 20C and 80C XBIC maps were used

the lineouts from this program look very good
    normalized intensities are different
    peaks and troughs are in the same position

the lineouts from applying the XBIC warp matrix to the Au_L channel look alright
    the Au_L channel is noisy to begin with
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# extract line of interest
lineout_20 = im1_F32[58,:]
lineout_80 = im2_aligned[58,:]

# Normalize intensity
lineout_20N = lineout_20 / lineout_20.max()
lineout_80N = lineout_80 / lineout_80.max()

# plot line plot of at the same index as the line out
fig, ax = plt.subplots(figsize=(3.6,3.6))
ax.plot(lineout_20N, label='20C')
ax.plot(lineout_80N, label='80C')
ax.set_ylim([0.8,1.1])
ax.legend()

fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))

ax.set_xlabel("X (um)")

ax.set_ylabel("XBIC (arb. units)")
#%%
# Repeat using XBIC warp matrix on Au_L 80C map
lineout_20Au = im1Au_F32[58,:]
lineout_80Au = im2Au_aligned[58,:]

# Normalize intensity
lineout_20AuN = lineout_20Au / lineout_20Au.max()
lineout_80AuN = lineout_80Au / lineout_80Au.max()

# plot line plot of at the same index as the line out
fig, ax = plt.subplots(figsize=(3.6,3.6))
ax.plot(lineout_20AuN, label='20C')
ax.plot(lineout_80AuN, label='80C')
ax.set_ylim([0.70,1.1])
ax.legend()

fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))

ax.set_xlabel("X (um)")

ax.set_ylabel("Au XRF (arb. units)")

#%%
# Repeat using XBIC warp matrix on Se_K 80C map
lineout_20Se = im1Se_F32[58,:]
lineout_80Se = im2Se_aligned[58,:]

# Normalize intensity
lineout_20SeN = lineout_20Se / lineout_20Se.max()
lineout_80SeN = lineout_80Se / lineout_80Se.max()

# plot line plot of at the same index as the line out
fig, ax = plt.subplots(figsize=(3.6,3.6))
ax.plot(lineout_20SeN, label='20C')
ax.plot(lineout_80SeN, label='80C')
ax.set_ylim([0.70,1.1])
ax.legend()

fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))

ax.set_xlabel("X (um)")

ax.set_ylabel("Se XRF (arb. units)")