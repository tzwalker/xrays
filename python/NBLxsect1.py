path = r'C:\Users\triton\Desktop\NBL3_data\cross_section_MS' #r'C:\Users\triton\Desktop\NBL3_data\cross_section_MS\csvs'
defs = r'C:\Users\triton\xrays\python\1_NBL3_code'
import sys
sys.path.append(defs)
import xSect_defs
import numpy as np

sample = 'NBL31'
scannum = 8
channels = ['XBIC_lockin', 'Cu_K', 'Cd_L3']
meta_data = xSect_defs.get_scan_metadata(path, sample, scannum)
rotation = 0

dfs_rotated = xSect_defs.import_xSect_csvs(path, sample, scannum, channels, meta_data, rotation)
#%%
# manually plot xsect 
import matplotlib.pyplot as plt
import seaborn as sns

df = dfs_rotated[0] # define data (index matches that in 'channels')
fig, axes = plt.subplots(figsize=(2,5)) # changes aspect ratio
ch_max = df.values.max()
ax = sns.heatmap(df, vmax=ch_max, cmap='magma', xticklabels=40, yticklabels=40)
# for manually plotting range of axes
my_xticks = ax.get_xticks() 
# use only first and last tick position; format ticks
plt.xticks([my_xticks[0], my_xticks[-1]], visible=True, fontsize=14, rotation=90)
# set the first and last tick labels according to known map size
ax.set_xticklabels([0,12])     
plt.xlabel('X (\u03BCm)', fontsize=16, rotation=180)                   
# same for yticks
my_yticks = ax.get_yticks()  
plt.yticks([my_yticks[0], my_yticks[-1]], visible=True, fontsize=14, rotation=90)
ax.set_yticklabels([0,24])
plt.ylabel('Y (\u03BCm)', fontsize=16, rotation=90) 

ax.invert_yaxis()                                  

# colorbar label settings
cbar_ax = plt.gcf().axes[-1]                        #get seaborn cbar object
cbar_ax.set_ylabel('A', rotation = 90, size=16)     #formats cbar label
cbar_ax.tick_params(labelsize=14, rotation=90)      #formats cbar ticks
cbar_ax.yaxis.get_offset_text().set(size=14)        #formats cbar scale
cbar_ax.yaxis.set_offset_position('left')           #positions cbar scale

#%%
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

arrays = export_integrated_dfs(imported_rotated_dataframes)
#np.savetxt(r'C:\Users\Trumann\Dropbox (ASU)\1_NBL3 data\py_' + sample +"_Scan"+ str(scannum) + '.csv', arrays, delimiter = ',')
