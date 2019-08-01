import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import pandas as pd
import numpy as np
#import itertools

def make_integersForTickLabels(xreal, yreal):
    x = []
    for i,um in enumerate(xreal):
        if um.is_integer():
            um = int(um)
        x.append(um)
    y = []
    for i,um in enumerate(yreal):
        if um.is_integer():
            um = int(um)
        y.append(um)
    return x, y

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

def get_ticklabels(x_real, y_real):
    # i don't need to check if it's an integer because i have integers now in x and y
    track_x_index = [i for i, um in enumerate(x_real) if isinstance(um, int)] # if x_real is whole um, record the index
    xticks = track_x_index[1]                                             # take index closest to 0 index
    track_y_index = [i for i, um in enumerate(y_real) if isinstance(um, int)] #um.is_integer()
    yticks = track_y_index[1]
    return xticks, yticks


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
# =============================================================================
#             plt.xticks(x)
#             plt.yticks(y)
# =============================================================================
            ax = sns.heatmap(df_map, square = True, xticklabels  = 20, yticklabels = 20)
            ax.invert_yaxis()
            #ax.xaxis.set_major_locator(tkr.MaxNLocator(integer=True))
            #ax.xaxis.get_major_ticks().label.set_fontsize(14)
            #plt.gca().xaxis.set_major_formatter(formatter)
            #plt.xticks(rotation=0)
            #plt.title(samp['Name'] + ' XBIC ' + str(scan_num))
    return

def plot_ele_maps(samps):
    for samp in samps:
        for scan in samp:
            print('do ele after')
    return

# =============================================================================
# locator = matplotlib.ticker.MultipleLocator(2)
# plt.gca().xaxis.set_major_locator(locator)
# formatter = matplotlib.ticker.StrMethodFormatter("{x:.0f}")
# plt.gca().xaxis.set_major_formatter(formatter)
# plt.show()
# from matplotlib.ticker import FormatStrFormatter
# 
# fig, ax = plt.subplots()
# 
# ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# =============================================================================
# =============================================================================
# #next(x for x in lst if matchCondition(x)) 
# 
# 
# x_axis, y_axis = get_real_coordinates(NBL3_2['XBIC_h5s'][0]['/MAPS/x_axis'], NBL3_2['XBIC_h5s'][0]['/MAPS/y_axis'])
# xr, yr = get_real_coordinates(x_axis, y_axis)
# replace_w_integers(xr, yr)
# =============================================================================
# =============================================================================
# def get_nth_index(real_axis, n):
#     c = itertools.count()
#     second_matching_index = next(i for i, um in enumerate(real_axis) if isinstance(um, int) and next(c) == n-1)
#     return second_matching_index
# =============================================================================