import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import pandas as pd
import numpy as np
#import itertools

def get_real_coordinates(x_axis, y_axis):
    x_list = list(x_axis)
    x_diff = max(x_list) - min(x_list)
    x_real = np.linspace(0, x_diff, len(x_axis))
    x_real_rounded = [round(i,3) for i in x_real]
    y_list = list(y_axis)
    y_diff = max(y_list) - min(y_list)
    y_real = np.linspace(0, y_diff, len(y_axis))
    y_real_rounded = [round(i,3) for i in y_real]
    return x_real_rounded, y_real_rounded

def plot_elect_maps(samps, elect_channel): # input only 'XBIC' or 'XBIV'
    #formatter = tkr.FormatStrFormatter("%.05f")
    #locator = tkr.LinearLocator(numticks = 5)
    if elect_channel == 'XBIC':
        for samp in samps:
            for c_scan, c_map, scan_num in zip(samp['XBIC_h5s'], samp['XBIC_maps'], samp['XBIC_scans']):
                x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
                y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
                x, y = get_real_coordinates(x_axis, y_axis)
                #xt, yt = get_ticklabels(x,y)
                df_map = pd.DataFrame(c_map, index = y, columns = x)
            plt.figure()
            ax = sns.heatmap(df_map, square = True, xticklabels  = 20, yticklabels = 20)
            ax.invert_yaxis()
            #plt.xticks(rotation=0)
            #plt.title(samp['Name'] + ' XBIC ' + str(scan_num))
    return

def custom_format_ticks(axes_object):
    x_txt_labs = [label.get_text() for label in axes_object.get_xticklabels()]
    x_ticking = ['{:g}'.format(float(x)) for x in x_txt_labs]
    
    y_txt_labs = [label.get_text() for label in axes_object.get_yticklabels()]
    y_ticking = ['{:g}'.format(float(y)) for y in y_txt_labs]
    return x_ticking, y_ticking

c_scan = TS58A['XBIC_h5s'][3]
x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
x_real, y_real = get_real_coordinates(x_axis, y_axis)

c_map = TS58A['XBIC_maps'][3]
df_map = pd.DataFrame(c_map, index = y_real, columns = x_real)


fig, ax0 = plt.subplots()
#ax0 = plt.pcolormesh(x_real, y_real, df_map, cmap="rocket")
ax0 = sns.heatmap(df_map, square = True, xticklabels = 30, yticklabels = 30, vmin = 0)#, cbar_kws={'format': '%0.2f'})

plt.xlabel('um', fontsize=16)
plt.ylabel('um', fontsize=16)

x_labls, y_labls = custom_format_ticks(ax0)
ax0.tick_params(labelsize = 14)

ax0.set_xticklabels(x_labls)

ax0.set_yticklabels(y_labls, rotation = 0)
ax0.invert_yaxis()

#fig.colorbar(ax0).ax0 <--> plt.gcf().axes[-1]
cbar_ax = plt.gcf().axes[-1]
cbar_ax.set_ylabel('A', fontsize = 16, rotation = -90, labelpad = 20)
cbar_ax.tick_params(labelsize=12) 

cbar_ax.yaxis.set_offset_position('left')
cbar_ax.yaxis.get_offset_text().set(size=12)
#cbar_ax.get_yticklabels()





