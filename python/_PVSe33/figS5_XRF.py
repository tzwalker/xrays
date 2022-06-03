# -*- coding: utf-8 -*-
"""

Trumann
Tue May 31 14:51:17 2022

supplementary info fig 5 file

plots the maps and interfaces
"""
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker
import numpy as np


'''
0hr plotting

this cell is the clean way to plot maps on top of one another
and with a line plot below it - be sure to run 'integrate_XRFmaps.py'

'''
def norm(data):
    return (data)/(max(data)-min(data))

sn = df_maps[5]
sn = sn.to_numpy()
sn = sn[:,:-2]
msn = np.ma.masked_where(sn<1e3,sn,copy=True)

se = df_maps[2]
se = se.to_numpy()
se = se[:,:-2]
mse = np.ma.masked_where(se<1.75e4,se,copy=True)

te = df_maps[3]
te = te.to_numpy()
te = te[:,:-2]
mte = np.ma.masked_where(te<1.75e3,te,copy=True)

au = df_maps[4]
au = au.to_numpy()
au = au[:,:-2]
mau = np.ma.masked_where(au<8e3,au,copy=True)

masks = [msn,mse,mte,mau]

# plot overlaid images
fig, (ax1,ax2) = plt.subplots(2,1, sharex='all')
ax1.xaxis.set_ticks(np.arange(0,101,11)) # calibrate

for i,m in enumerate(masks):
    im = ax1.imshow(m,cmap=colors[i],origin='lower',alpha=0.65,aspect=9)
    #fig.colorbar(im, format=fmt)
    #color bar labels
    #cbar = plt.gcf().axes[-1]
    #cbar.set_ylabel(unit[i], rotation=90, va="bottom", labelpad=30)
    #change color bar scale label position 
    #cbar.yaxis.set_offset_position('left')



fmtr_y = lambda x, pos: f'{(x * 1.000):.0f}'
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax1.set_ylabel('$Y$ (μm)')

# plot line plot underneath image
ax2.xaxis.set_ticks(np.arange(0,101,11)) # calibrate

ax2.plot(norm(df_sums_arr[:,5]),color='g') # Sn
ax2.plot(norm(df_sums_arr[:,2]),color='b') # Se
ax2.plot(norm(df_sums_arr[:,3]),color='k') # Te
ax2.plot(norm(df_sums_arr[:,4]),color='orange') # Au


fmtr_x = lambda x, pos: f'{(x * 0.100):.0f}'
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax2.set_xlabel('$X$ (μm)')
ax2.set_ylabel('XRF (arb. unit)')

asp = np.diff(ax2.get_xlim())[0] / np.diff(ax2.get_ylim())[0]
ax2.set_aspect(asp)

#%%
'''
500hr plotting

this cell is the clean way to plot maps on top of one another
and with a line plot below it - be sure to run 'integrate_XRFmaps.py'

'''
def norm(data):
    return (data)/(max(data)-min(data))

sn = df_maps[5]
sn = sn.to_numpy()
sn = sn[:-13,13:-2]
msn = np.ma.masked_where(sn<1e3,sn,copy=True)

se = df_maps[2]
se = se.to_numpy()
se = se[:-13,13:-2]
mse = np.ma.masked_where(se<1.75e4,se,copy=True)

te = df_maps[3]
te = te.to_numpy()
te = te[:-13,13:-2]
mte = np.ma.masked_where(te<1.75e3,te,copy=True)

au = df_maps[4]
au = au.to_numpy()
au = au[:-13,13:-2]
mau = np.ma.masked_where(au<8e3,au,copy=True)

masks = [msn,mse,mte,mau]

# plot overlaid images
fig, (ax1,ax2) = plt.subplots(2,1, sharex='all')
ax1.xaxis.set_ticks(np.arange(0,76,12)) # calibrate

for i,m in enumerate(masks):
    im = ax1.imshow(m,cmap=colors[i],origin='lower',alpha=0.65)
    #fig.colorbar(im, format=fmt)
    #color bar labels
    #cbar = plt.gcf().axes[-1]
    #cbar.set_ylabel(unit[i], rotation=90, va="bottom", labelpad=30)
    #change color bar scale label position 
    #cbar.yaxis.set_offset_position('left')



fmtr_y = lambda x, pos: f'{(x * 0.160):.0f}'
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax1.set_ylabel('$Y$ (μm)')

# plot line plot underneath image
ax2.xaxis.set_ticks(np.arange(0,76,12)) # calibrate

ax2.plot(norm(df_sums_arr[13:,5]),color='g') # Sn
ax2.plot(norm(df_sums_arr[13:,2]),color='b') # Se
ax2.plot(norm(df_sums_arr[13:,3]),color='k') # Te
ax2.plot(norm(df_sums_arr[13:,4]),color='orange') # Au


fmtr_x = lambda x, pos: f'{(x * 0.160):.0f}'
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax2.set_xlabel('$X$ (μm)')
ax2.set_ylabel('XRF (arb. unit)')

asp = np.diff(ax2.get_xlim())[0] / np.diff(ax2.get_ylim())[0]
ax2.set_aspect(asp)


#%%
'''
plotting 0hr maps

this cell was the dirty way to mask and plot maps in a column
could be useful if i need to plot the maps in a single column quickly
'''
PERCENTILE = 80

sn = df_maps[5]
sn = sn.to_numpy()
sn = sn[:,:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(sn, PERCENTILE)
print(bound)
#sn[sn<bound] = np.nan


se = df_maps[2]
se = se.to_numpy()
se = se[:,:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(se, PERCENTILE)
print(bound)
#se[se<bound] = np.nan


te = df_maps[3]
te = te.to_numpy()
te = te[:,:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(te, PERCENTILE)
print(bound)
#te[te<bound] = np.nan


au = df_maps[4]
au = au.to_numpy()
au = au[:,:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(au, PERCENTILE)
print(bound)
#au[au<bound] = np.nan


fig, axs = plt.subplots(4,1,sharex='all')

maps = [sn,se,te,au]
colors = ['Greens_r','Blues_r','Greys_r','YlOrBr_r']
unit = ['Sn XRF \n (cts/s)','Se XRF \n (cts/s)','Te XRF \n (cts/s)','Au XRF \n (cts/s)']

for i,ax in enumerate(axs):
    im = ax.imshow(maps[i], cmap=colors[i], origin='lower')
    ax.set_aspect(9)
    ax.set_ylabel('$Y$ (μm)')
    # outline possible position of interfaces
    ax.axvline(20,color='r',linestyle='-', linewidth=0.5)
    ax.axvline(65,color='r',linestyle='-', linewidth=0.5)
    
    fmt = mticker.ScalarFormatter(useMathText=True)
    fmt.set_powerlimits((0, 0))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='2%',pad=-1.8) # for 072
    
    fig.colorbar(im, cax=cax, format=fmt)
    #color bar labels
    cbar = plt.gcf().axes[-1]
    cbar.set_ylabel(unit[i], rotation=90, va="bottom", labelpad=30)
    #change color bar scale label position 
    cbar.yaxis.set_offset_position('left')
    
    fmtr_y = lambda x, pos: f'{(x * 1.000):.0f}'
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
    
fmtr_x = lambda x, pos: f'{(x * 0.100):.0f}'
axs[3].xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
axs[3].set_xlabel('$X$ (μm)')
    
plt.tight_layout()

#%%
'''
plotting 500hr maps

this cell was the dirty way to mask and plot maps in a column
could be useful if i need to plot the maps in a single column quickly
'''
sn = df_maps[5]
sn = sn.to_numpy()
sn = sn[:-13,13:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(sn, PERCENTILE)
print(bound)
#sn[sn<bound] = np.nan


se = df_maps[2]
se = se.to_numpy()
se = se[:-13,13:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(se, PERCENTILE)
print(bound)
#se[se<bound] = np.nan


te = df_maps[3]
te = te.to_numpy()
te = te[:-13,13:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(te, PERCENTILE)
print(bound)
#te[te<bound] = np.nan


au = df_maps[4]
au = au.to_numpy()
au = au[:-13,13:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(au, PERCENTILE)
print(bound)
#au[au<bound] = np.nan


fig, axs = plt.subplots(4,1,sharex='all')

maps = [sn,se,te,au]
colors = ['Greens_r','Blues_r','Greys_r','YlOrBr_r']
unit = ['Sn XRF \n (cts/s)','Se XRF \n (cts/s)','Te XRF \n (cts/s)','Au XRF \n (cts/s)']

for i,ax in enumerate(axs):
    im = ax.imshow(maps[i], cmap=colors[i], origin='lower')
    ax.set_aspect(1)
    ax.set_ylabel('$Y$ (μm)')
    # outline possible position of interfaces
    ax.axvline(10,color='r',linestyle='-', linewidth=0.5)
    ax.axvline(55,color='r',linestyle='-', linewidth=0.5)
    
    fmt = mticker.ScalarFormatter(useMathText=True)
    fmt.set_powerlimits((0, 0))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='20%',pad=0.1) # for 072
    
    fig.colorbar(im, cax=cax, format=fmt)
    #color bar labels
    cbar = plt.gcf().axes[-1]
    cbar.set_ylabel(unit[i], rotation=90, va="bottom", labelpad=30)
    #change color bar scale label position 
    cbar.yaxis.set_offset_position('left')
    
    fmtr_y = lambda x, pos: f'{(x * 0.160):.0f}'
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
    
fmtr_x = lambda x, pos: f'{(x * 0.160):.0f}'
axs[3].xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
axs[3].set_xlabel('$X$ (μm)')

plt.tight_layout()