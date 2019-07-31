import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

num_ticks = 10

def get_real_coordinates(x_axis, y_axis):
    x_list = list(x_axis)
    x_diff = max(x_list) - min(x_list)
    print()
    x_real = np.linspace(0, x_diff, len(x_axis))
    y_list = list(y_axis)
    y_diff = max(y_list) - min(y_list)
    y_real = np.linspace(0, y_diff, len(y_axis))
    return x_real, y_real

def get_ticklabels(x_real, y_real):
    # how to figure out what the proper indeices to plot are...?
    # the integer in xticklabels represents every 'n' index to be plotted
        # e.g. xtixklabels = 50 --> 0, 50, 150 all plotted
        # the list x_real has actual numbers that map to the indices... but how does that help me...   
        # could use mod?
    # find where first whole number is in x_real!
      # get index of this number... 
      # when would whole number not exist...? 
          # when the width of the axis is not evenly split by the resolution
          # e.g. np.linspace(0,16,38)
      # HOWEVER: the first and last number, as they are int, are guaranteed
          # to be whole, therefore, the above approach will always find a whole number index
          # and will plot either the bounds of the axes, or every whole number that exists in the linear space!
    return xticks, yticks

def plot_elect_maps(samps, elect_channel): # input only 'XBIC' or 'XBIV'
    if elect_channel == 'XBIC':
        for samp in samps:
            for c_scan, c_map, scan_num in zip(samp['XBIC_h5s'], samp['XBIC_maps'], samp['XBIC_scans']):
                x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
                y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
                x, y = get_real_coordinates(x_axis, y_axis)
                #xt, yt = get_ticklabels(x,y)
                df_map = pd.DataFrame(c_map[:,:-2], index = y, columns = x[:-2])
            print(x)
            #plt.figure()
            #ax = sns.heatmap(df_map, square = True, xticklabels = 50).invert_yaxis()
            #plt.title(samp['Name'] + ' XBIC ' + str(scan_num))
    else:
        for samp in samps:
            for v_scan, v_map, scan_num in zip(samp['XBIV_h5s'], samp['XBIV_maps'], samp['XBIV_scans']):
                x_axis = v_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
                y_axis = v_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
                x, y = get_real_coordinates(x_axis, y_axis)
                df_map = pd.DataFrame(v_map[:,:-2], index = y, columns = x[:-2])
            plt.figure()
            ax = sns.heatmap(df_map, square = True).invert_yaxis()
            plt.title(samp['Name'] + ' XBIV scan ' + str(scan_num))
    return

def plot_ele_maps(samps):
    for samp in samps:
        for scan in samp:
            print('do ele after')
    return


    