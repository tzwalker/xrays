import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

num_ticks = 10

def get_real_coordinates(x_axis, y_axis):
    xpixsize = (max(x_axis) - min(x_axis)) / len(x_axis) # in um
    x_i = list(range(len(x_axis)))
    x_real = [i * xpixsize for i in x_i]
    ypixsize = (max(y_axis) - min(y_axis)) / len(y_axis)
    y_i = list(range(len(y_axis)))
    y_real = [i * ypixsize for i in y_i]
    return x_real, y_real

def make_whole_coord(x_list, y_list):
    new_x = [round(i) for i in x_list]
    new_y = [round(i) for i in y_list]
    return new_x, new_y


def plot_XBIC(samps, c_channel):
    for samp in samps:

        for i, (c_scan, c_map) in enumerate(zip(samp['XBIC_h5s'], samp['XBIC_maps'])):
            x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
            y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
            x, y = get_real_coordinates(x_axis, y_axis)
            #x_r, y_r = make_whole_coord(x,y)
            #yticks = np.linspace(0, len(y) - 1, num_ticks, dtype=np.int)
            #yticklabels = [y[idx] for idx in yticks]

            df_map = pd.DataFrame(c_map[:,:-2], index = y_r, columns = x_r[:-2])
        plt.figure()
        ax = sns.heatmap(df_map, square = True, xticklabels = 10).invert_yaxis()
        plt.title(samp['Name'] + ' XBIC')
            
    return x_r

def plot_elect_maps(samps, elect_channel): # input only 'XBIC' or 'XBIV'
    if elect_channel == 'XBIC':
        plot_XBIC(samps, elect_channel)
    else:
        plot_XBIV(samps, elect_channel)
    return

# the index of the position of yticks
# the content of labels of these yticks
