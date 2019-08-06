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

    y_list = list(y_axis)
    y_diff = max(y_list) - min(y_list)
    y_real = np.linspace(0, y_diff, len(y_axis))

    x_real, y_real = make_integersForTickLabels(x_real, y_real)
    print(len(y_axis))
    return x_real, y_real

def get_first_ints(axis_list):
    # Python program to find second largest number in a list 
    firstmax = max(axis_list[0], axis_list[1]) 
    secondmax = min(axis_list[0], axis_list[1]) 
    for i in range(2, len(axis_list)): 
    	if axis_list[i] < firstmax: 
    		secondmax = firstmax
    		firstmax = axis_list[i] 
    	else: 
    		if axis_list[i] < secondmax: 
    			secondmax = axis_list[i] 
    return secondmax
get_first_ints(x_rounded)

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
            #ax.xaxis.set_major_locator(tkr.MaxNLocator(integer=True))
            #ax.xaxis.get_major_ticks().label.set_fontsize(14)
            #plt.gca().xaxis.set_major_formatter(formatter)
            #plt.xticks(rotation=0)
            #plt.title(samp['Name'] + ' XBIC ' + str(scan_num))
    return


c_scan = NBL3_3['XBIC_h5s'][0]
x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
x, y = get_real_coordinates(x_axis, y_axis)
x_rounded = [round(i,3) for i in x]
y_rounded = [round(i,3) for i in y]

c_map = NBL3_3['XBIC_maps'][0]
df_map = pd.DataFrame(c_map, index = y_rounded, columns = x_rounded)
x_index_of_first_int, y_index_of_first_int = get_first_ints(x_rounded, y_rounded)
fig, ax0 = plt.subplots()
ax0 = sns.heatmap(df_map, square = True, xticklabels = 15)
ax0.invert_yaxis()
#ax0.xaxis.set_major_locator(tkr.MaxNLocator(20))

labels = [label.get_text() for label in ax0.get_xticklabels()]
ax0.set_xticklabels(map(lambda x: "{:g}".format(float(x)), labels)) # --> works! gotta get proper tick indices now

labels = [label.get_text() for label in ax0.get_yticklabels()]
ax0.set_yticklabels(map(lambda x: "{:g}".format(float(x)), labels))


my_data = np.random.rand(150,150)
x = (np.linspace(0, my_data.shape[0], my_data.shape[0]+1)-0.5)/10
y = (np.linspace(0, my_data.shape[1], my_data.shape[1]+1)-0.5)/10


fig, ax = plt.subplots()
pc = ax.pcolormesh(x, y, my_data, cmap="rocket")
fig.colorbar(pc)
ax.set_aspect("equal")
plt.show()
# =============================================================================
# x_axis, y_axis = get_real_coordinates(NBL3_2['XBIC_h5s'][0]['/MAPS/x_axis'], NBL3_2['XBIC_h5s'][0]['/MAPS/y_axis'])
# xr, yr = get_real_coordinates(x_axis, y_axis)
# replace_w_integers(xr, yr)
# 
# locator = matplotlib.ticker.MultipleLocator(2)
# plt.gca().xaxis.set_major_locator(locator)
# formatter = matplotlib.ticker.StrMethodFormatter("{x:.0f}")
# plt.gca().xaxis.set_major_formatter(formatter)
# plt.show()
# from matplotlib.ticker import FormatStrFormatter
# 
# 
# def get_nth_index(real_axis, n):
#     c = itertools.count()
#     second_matching_index = next(i for i, um in enumerate(real_axis) if isinstance(um, int) and next(c) == n-1)
#     return second_matching_index
# =============================================================================
