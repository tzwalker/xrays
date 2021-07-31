"""
20210623
this is the most recent program used to access and plot xsect NBL3 data

-the program assumes you have all the csvs shared with us by M. Stuckelberger
and these csvs are in the directory "PATH"

"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from skimage.transform import rotate

def get_scan_metadata(path, sample, scannum):
    metafile_string = '\CdTe_X_' + sample + '_Scan_' + str(scannum) + '_Metadata.csv'
    metafile = path + metafile_string
    # import metadata
    df = pd.read_csv(metafile, header=None)
    # make new names from labels in 1st column
    new_names = [name[0:6] for name in df[0]] 
    # to put labels in first row, transpose df 
    df = df.T
    # using labels in 1st row, make column headers                     
    df.columns = df.iloc[0]
    # remove first row         
    df = df.reindex(df.index.drop(0))   
    # rename column headers with short names
    df.rename(columns = {old:new for old, new in zip(df.columns.values, new_names)}, inplace=True) 
    return df

def get_axes_from_metadata(data_df, units_df):
    old_x = data_df.columns.values                      # get column labels in data df (type: numpy array)
    # scale indices according to axis step 
        # cast to float from string, 
        # and cast to list to prep for rounding
    x_real = list(old_x * float(units_df['xstep ']))    
    x_round = [round(i,3) for i in x_real] # round off axis units
    # same for y
    old_y = data_df.index.values
    y_real = list(old_y * float(units_df['ystep ']))
    y_round = [round(i,2) for i in y_real] # round off axis units
    
    data_df.rename(columns = {old:new for old,new in zip(old_x, x_round)},
                              index = {old:new for old,new in zip(old_y, y_round)}, inplace=True)
    return 

def import_xSect_csvs(path, sample, scannum, channels, meta, rot):
    rotated_map_dfs = []
    for chan in channels:
        str_scannum = str(scannum)
        file_string = '\CdTe_X_{s}_Scan_{n}_{c}_data.csv'.format(s=sample,
                                                                 n=str_scannum,
                                                                 c=chan)
        file = path + file_string
        # import scan
        df = pd.read_csv(file, header=None)  
        # rotate image
        rot_nparray = rotate(df, rot) 
        # numpy array to df
        rot_df = pd.DataFrame(rot_nparray) 
        #set column/row(index) headers to real units
        get_axes_from_metadata(rot_df, meta) 
        # build imported list
        rotated_map_dfs.append(rot_df) 
    return rotated_map_dfs # can have no rotation

#r'C:\Users\Trumann\data_NBL3\cross_sections_MS'
#r'C:\Users\triton\NBL3_data\cross_section_MS'
PATH = r'C:\Users\triton\NBL3_data\cross_section_MS' 


SAMPLE = 'NBL33'
SCAN = 1
CHANNELS = ['XBIC_lockin', 'Cu_K', 'Cd_L3']

META_DATA = get_scan_metadata(PATH, SAMPLE, SCAN)
ROTATION = 0

map_dfs = import_xSect_csvs(PATH, SAMPLE, SCAN, CHANNELS, META_DATA, ROTATION)

#%%
'''
everything from this point on is for plotting or some sort of post-analysis

you can ignore or edit it as you see fit

'''

# this if statement was created so that the same number of rows could be
# compared between scans (i.e. the same number of pixels or data points)
PLT_CHAN_IDX = 2
if SAMPLE == 'NBL31':
# for NBL31 scan 8 to have the same points and 5um length as NBL33 scan 1
    # XBIC scale from 0-250 nA
    map_data = map_dfs[PLT_CHAN_IDX].iloc[:34,:] # 34 pts at 150nm step ~ 5um
else: 
    # otherwise (for NBL33) plot data frame normally
    map_data = map_dfs[PLT_CHAN_IDX]


# for exporting cross-section maps
plt.figure()
fig, ax = plt.subplots(figsize=(5,5))
im = ax.imshow(map_data, cmap='inferno')
#plt.gca().invert_xaxis() --> flips map
ax.axis('off')


OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20200525 figures_rev3\xsect_exp\FINALS_maps with colorbars'
FNAME = r'\map_NBL31scan8_XBIC_flip.eps'
#plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)

# for exporting cross-section integration
#integrate = data.sum(axis=0)
#plt.figure()
#plt.plot(integrate)
#OUT_PATH1 = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\xsect integreated and models'
#FNAME = r'\py_NBL31_Scan8_trimTo5um_Cd.csv'
#integrate.to_csv(OUT_PATH1+FNAME, header=False)
#%%

def plot_NBL3_xsect(df, fig_size, color, cbar_bounds,
                    xyinterval,ticksize,
                    xtick_bounds,xlabelsize,xlab_roatation,
                    ytick_bounds,ylabelsize,ylab_roatation,
                    cbar_label, cbar_labelsize, cbar_ticksize, cbar_tick_rot):

    # change aspect ratio
    fig, axes = plt.subplots(figsize=fig_size)
    #plot using seaborn
    ax = sns.heatmap(df, vmin=cbar_bounds[0],vmax=cbar_bounds[1], cmap=color, 
                     xticklabels=xyinterval, yticklabels=xyinterval)
    # for manually plotting range of axes
    my_xticks = ax.get_xticks() 
    # use only first and last tick position; format ticks
    plt.xticks([my_xticks[0], my_xticks[-1]], 
               visible=True, fontsize=ticksize, rotation=xlab_roatation)
    # set the first and last tick labels according to known map size
    ax.set_xticklabels(xtick_bounds)     
    plt.xlabel('X (\u03BCm)', fontsize=xlabelsize, rotation=0)                   
    # same for yticks
    my_yticks = ax.get_yticks()  
    plt.yticks([my_yticks[0], my_yticks[-1]], 
               visible=True, fontsize=ticksize, rotation=ylab_roatation)
    ax.set_yticklabels(ytick_bounds)
    plt.ylabel('Y (\u03BCm)', fontsize=ylabelsize, rotation=90) 
    ax.invert_yaxis()                                  
    
    # colorbar label settings
    #get seaborn cbar object
    cbar_ax = plt.gcf().axes[-1]                        
    #formats cbar label
    cbar_ax.set_ylabel(cbar_label, rotation=90, size=cbar_labelsize) 
    #formats cbar ticks    
    cbar_ax.tick_params(labelsize=cbar_ticksize, rotation=cbar_tick_rot)  
    #formats cbar scale    
    cbar_ax.yaxis.get_offset_text().set(size=cbar_ticksize)
    #positions cbar scale
    cbar_ax.yaxis.set_offset_position('left')           
    return
PLOT_CHANNEL_IDX = 0
PLOT_CHANNEL = dfs[PLOT_CHANNEL_IDX]
FULL_YRANGE = np.max(np.max(PLOT_CHANNEL))
plot_NBL3_xsect(PLOT_CHANNEL, (2,2), 'magma', [0,FULL_YRANGE],
                50, 14,
                [0,17], 14, 90, 
                [0,30], 14, 90,
                '(a.u.)', 16,14, 0)


def export_integrated_dfs(imp_rot_dfs):
    integrated_arrays_of_each_channel = []
    x = imp_rot_dfs[0].columns.values
    x = x.reshape(-1,1)
    for df in imp_rot_dfs:
        y_integrate = df.sum(axis=0)        #df
        y_integrate = y_integrate.to_numpy()
        y_integrate = y_integrate.reshape(-1,1)
        integrated_arrays_of_each_channel.append(y_integrate)
    integrated_arrays_of_each_channel.insert(0, x)
    arrays = np.concatenate(integrated_arrays_of_each_channel, axis=1)
    return arrays

arrays = export_integrated_dfs(dfs)
#SYS_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\xsectMS'
#np.savetxt(SYS_PATH + r'\py_' + sample +"_Scan"+ str(scannum) + '.csv', arrays, delimiter = ',')
print(arrays[0,1], 'v', arrays[0,2])

#%%
"""
this program is meant to extract the peak of the integrated
XBIC (or XRF) signals through the depth of the CdTe device
AND
check to see if the XBIC scaler settings of the scans are the same...
to be used on the data from M. Stuckelberger Spring, 2018 ESRF
cross-section maps of NBL3 sample set
"""
#r'' C:\Users\triton\Desktop\NBL3_data\cross_section_MS
PATH = r'C:\Users\Trumann\Desktop\NBL3_data\cross_sections_MS' 
#r'' C:\Users\triton\xrays\python\_NBL3
DEFS = r'C:\Users\Trumann\xrays\python\_NBL3' 

import sys
sys.path.append(DEFS)
from definitions_NBLxSect import import_xSect_csvs, get_scan_metadata
import numpy as np

def integrate_maps(imp_rot_dfs):
    integrated_arrays_of_each_channel = []
    x = imp_rot_dfs[0].columns.values
    x = x.reshape(-1,1)
    for df in imp_rot_dfs:
        y_integrate = df.sum(axis=0)        #df
        y_integrate = y_integrate.to_numpy()
        y_integrate = y_integrate.reshape(-1,1)
        integrated_arrays_of_each_channel.append(y_integrate)
    integrated_arrays_of_each_channel.insert(0, x)
    arrays = np.concatenate(integrated_arrays_of_each_channel, axis=1)
    return arrays

SAMPLES = ['NBL31','NBL31','NBL31','NBL31', 
          'NBL33','NBL33','NBL33','NBL33',
          'NBL33','NBL33','NBL33','NBL33',
          'TS58A','TS58A','TS58A','TS58A']
SCANS = [1,6,7,8, 
        1,2,12,13,
        14,15,17,20, 
        2,3,4,5]
ROTATION = [0,0,0,0,
            15,15,15,15,
            15,15,15,15,
            0,0,0,0]

CHANNELS = ['XBIC_direct', 'Cd_L3']

# EXTRACT AVERAGES AND PEAKS OF EACH XSECT SCAN
profiles = []; maxes = [] ; avgs = []
for sample,scan,rot in zip(SAMPLES,SCANS,ROTATION):
    META_DATA = get_scan_metadata(PATH, sample, scan)
    MAPS = import_xSect_csvs(PATH, sample, scan, CHANNELS, META_DATA, rot)
    ARRAYS = integrate_maps(MAPS)
    profiles.append(ARRAYS)
    XBIC_MAX = np.max(ARRAYS[:,1])
    maxes.append(XBIC_MAX)
    XBIC_AVG = np.mean(ARRAYS[:,1])
    avgs.append(XBIC_AVG)
maxes_arr = np.array(maxes)
avgs_arr = np.array(avgs)

#%%
# fast-check scaler settings
xsect_meta = []
for SAMP,SCAN,ROT in zip(SAMPLES,SCANS,ROTATION):
    META_DATA = get_scan_metadata(PATH, SAMP, SCAN)
    xsect_meta.append(META_DATA)

for i, DF in enumerate(xsect_meta):
    if DF['XBIC_l'].item() == str(1):
        print('{s}_scan{n}_{r}'.format(s=SAMPLES[i],n=str(SCANS[i]),r='true'))
    else: 
        print('{s}_scan{n}_{r}'.format(s=SAMPLES[i],n=str(SCANS[i]),r='false'))


