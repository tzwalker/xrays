import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.transform import rotate

def get_scan_metadata(sample, scannum):
    metafile_string = '\CdTe_X_' + sample + '_Scan_' + str(scannum) + '_Metadata.csv'
    metafile = path + metafile_string
    df = pd.read_csv(metafile, header=None) # import metadata
    new_names = [name[0:6] for name in df[0]] # make new names from labels in 1st column
    df = df.T                           # transpose df to make labels in first row
    df.columns = df.iloc[0]             # rename df column headers as labels in first row
    df = df.reindex(df.index.drop(0))   # remove first row
    df.rename(columns = {old:new for old, new in zip(df.columns.values, new_names)}, inplace=True) # rename column headers with short names
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

def custom_format_ticks(axes_object_labels, string_type):
    txt_labs = [label.get_text() for label in axes_object_labels]
    ticking = [string_type.format(float(txt)) for txt in txt_labs]
    return ticking

def plot_2D_xSect(imp_rot_dfs, ch_units, colors):
    for df, un, color in zip(imp_rot_dfs, ch_units, colors):
        fig, ax0 = plt.subplots()
        ch_max = df.values.max()
        sns.heatmap(df, ax=ax0, vmax=ch_max, xticklabels=50, yticklabels=50, cmap=color)
        x_labls = custom_format_ticks(ax0.get_xticklabels(), '{:.0f}')
        y_labls = custom_format_ticks(ax0.get_yticklabels(), '{:.0f}')         #formats tick label strings without ".0"
        ax0.set_xticklabels(x_labls)                        #set the tick labels
        ax0.set_yticklabels(y_labls, rotation = 0)          #set the ticklabels and rotate (if needed)
        ax0.invert_yaxis()                                  #invert the yaxis after formatting is complete
        
        cbar_ax = plt.gcf().axes[-1]                        #gets colorbar of current figure object, behaves as second y axes object
        # colorbar label settings
        cbar_ax.set_ylabel(un, fontsize = 16, 
                           rotation = 90, labelpad = 10)   #label formatting
        cbar_ax.tick_params(labelsize=12)                   #tick label formatting
        cbar_ax.yaxis.get_offset_text().set(size=12)        #format colorbar offset text
        cbar_ax.yaxis.set_offset_position('left')           #scale at top of colorbar (i.e. 'offset') position
        z_labls = custom_format_ticks(cbar_ax.get_yticklabels(), '{:g}')
        #cbar_ax.set_yticklabels(, fontsize=16, weight='bold') --> from internet
        cbar_ax.set_yticklabels(z_labls)
        #fig.tight_layout(pad=0, h_pad=0, w_pad=0)
    return

def import_xSect_csvs(sample, scannum, channels, meta, rot):
    rot_dfs = []
    fig, ax0 = plt.subplots() 
    for chan in channels:
        file_string = '\CdTe_X_' + sample + '_Scan_' + str(scannum) + '_' + chan + '_data.csv'
        file = path + file_string
        df = pd.read_csv(file, header=None)  # import scan
        rot_nparray = rotate(df, rot) # rotate image
        rot_df = pd.DataFrame(rot_nparray) # cast from numpy array to df
        get_axes_from_metadata(rot_df, meta) # set column/row(index) headers to real units
        rot_dfs.append(rot_df) # build imported list
    #sns.heatmap(rot_dfs[0]) # print map to check rotation
    return rot_dfs

path = r'C:\Users\Trumann\Desktop\NBL3_data\cross_sections_MS\csvs'
sample = 'NBL33'
scannum = 17
channels = ['XBIC_lockin', 'Cu_K', 'Cd_L3']
meta_data = get_scan_metadata(sample, scannum)
rotation = 5

imported_rotated_dataframes = import_xSect_csvs(sample, scannum, channels, meta_data, rotation)

# there should be as many entries in these lists as channels imported
ch_units = ['nA', '\u03BCg/cm'+ r'$^{2}$', '\u03BCg/cm'+ r'$^{2}$']
heat_colors = ['magma', 'Oranges_r', 'viridis']

#plot_2D_xSect(imported_rotated_dataframes, ch_units, heat_colors)

# should normalize the line scans so i don't have to worry about units!
def plot_integrated_line_scans(imp_rot_dfs, colors):
    fig, ax0 = plt.subplots()
    for index, (df,color) in enumerate(zip(imp_rot_dfs, colors)):
        x_position = list(df.columns.values)
        y_integrate = df.sum(axis=0)
        if index == 0:
            ax0.plot(x_position, y_integrate, color=color)
            plt.ylim([0, df.values.max()])
            #y_labls = custom_format_ticks(ax0.get_yticklabels(), '{:.1e}')
            #ax0.set_yticklabels(y_labls)
        else:
            ax1=ax0.twinx()
            ax1.plot(x_position, y_integrate, color=color)
            plt.ylim([0,1e7])
        plt.xlim([0, max(df.columns.values)])
        ax0.grid()
    return
line_colors = ['tab:blue', 'tab:orange', 'tab:green']
plot_integrated_line_scans(imported_rotated_dataframes, line_colors)