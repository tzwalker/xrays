# this file is to plot gold "4" @ 100C during the first stage experiment
    # scalers for 2019_06_2IDD were not defined properly during fit (20190709)
    # this includes all stage scans of FS3
    # refit needs to be performed before presentinig XRF data on the stage!
# instead of processing h5 in python, process ASCII exported
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# MAPS exports ASCIIs with column header whitespace, this removes that whitespace
def noColNameSpaces(pd_csv_df):
    old_colnames = pd_csv_df.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    pd_csv_df.rename(columns = {i:j for i,j in zip(old_colnames,new_colnames)}, inplace=True)
    return pd_csv_df

def custom_format_ticks(axes_object):
    x_txt_labs = [label.get_text() for label in axes_object.get_xticklabels()]
    x_ticking = ['{:g}'.format(float(x)) for x in x_txt_labs]
    y_txt_labs = [label.get_text() for label in axes_object.get_yticklabels()]
    y_ticking = ['{:g}'.format(float(y)) for y in y_txt_labs]
    return x_ticking, y_ticking

def plot_nice_from_ascii(xrf_image_full_path):
    df = pd.read_csv(xrf_image_full_path, skiprows = 1)
    df = noColNameSpaces(df)
    resolution = abs(df['y position'][0] - df['y position'][1]) * 1000
    df['x pixel no'] = df['x pixel no'] * resolution
    df['x pixel no'] = round(df['x pixel no'], 1)
    df['y pixel no'] = df['y pixel no'] * resolution
    df['y pixel no'] = round(df['y pixel no'], 1)
    map_df = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = 'Au_L')
    
    fig, ax0 = plt.subplots()
    ax0 = sns.heatmap(map_df, square = True, cmap = 'YlOrBr_r', 
                      xticklabels = 40, yticklabels = 40)
    # figure level
    plt.xlabel('X (\u03BCm)', fontsize=16)
    plt.ylabel('Y (\u03BCm)', fontsize=16)
    # axis level
    ax0.tick_params(labelsize = 14)                     #formats size of ticklabels
    x_labls, y_labls = custom_format_ticks(ax0)         #formats tick label strings without ".0"
    ax0.set_xticklabels(x_labls)                        #set the tick labels
    ax0.set_yticklabels(y_labls, rotation = 0)   
    ax0.invert_yaxis()
    
    cbar_ax = plt.gcf().axes[-1]                        #gets colorbar of current figure object, behaves as second y object
    # colorbar label settings
    cbar_ax.set_ylabel('\u03BCg/cm'+ r'$^{2}$', fontsize = 16, 
                       rotation = 90, labelpad = 10)   #label formatting
    cbar_ax.tick_params(labelsize=12)                   #tick label formatting
    cbar_ax.yaxis.set_offset_position('left')           #scale at top of colorbar (i.e. 'offset') position
    cbar_ax.yaxis.get_offset_text().set(size=12)        #format colorbar offset text
    #cbar_ax.set_yticklabels('0.2f') --> debug
    return

four_img = r'C:\Users\Trumann\Desktop\stage_data\combined_ASCII_2idd_0259.h5.csv'
plot_nice_from_ascii(four_img)