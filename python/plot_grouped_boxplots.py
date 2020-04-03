# -*- coding: utf-8 -*-
"""
Trumann
Thu Mar  5 16:22:57 2020
-this file is intended to compare distributions of xbic maps
in the form of grouped boxplots
-to be compatible with seaborn plotting:
    -labels needs to be generated
    -data need to be reshaped and aligned with labels
-this file accomplishes most of that
-simply change the scan idxs for each sample, and the corresponding
channel idx one would like to plot
-CAVEAT: the file has only be tested using maps of same size
and resolution; it may fail if these conditions are not meant
-more may be added to make seaborn plots prettier
"""

import numpy as np
import pandas as pd
#this for loop is for extracting data to go to Origin
#compile relevant scans
xbic_scans1 = [NBL31.maps[i][0,:,:-2].ravel() for i in [0,1,2]]
xbic_scans2 = [NBL32.maps[i][0,:,:-2].ravel() for i in [0,1,2]]
xbic_scans3 = [NBL33.maps[i][0,:,:-2].ravel() for i in [0,1,2]]
xbic_scans4 = [TS58A.maps[i][0,:,:-2].ravel() for i in [0,1,2]]

#prep for iterations with sample labels
scan_sets = [xbic_scans1, xbic_scans2, xbic_scans3, xbic_scans4]
#sample labels to use for each set of scans
sample_labels = ["HTLC", "HT", "HTHC", "LT"]
#intermediate lists to store extracted data
df_samp_labels = []; df_map_labels = []; df_raveled_data = []
#generate sample labels and map labels
def make_labels_and_shape_data_for_boxplots(data, sample_label):
    #list to array
    data = np.array(data)
    #sample labels = # of data points in each scan* # of scans
    sample_label = [sample_label] * len(data[0]) * len(data)
    #store sample labels in intermediate list
    df_samp_labels.append(sample_label)
    #map labels = # of maps (map idx as label) * # of data points in each scan
    map_label = [i for i, map in enumerate(data)] * len(data[0])
    #store map labels in intermediate list
    df_map_labels.append(map_label)
    #change shape of data to prep for stacking
    shaped_data = data.T
    #stack shaped data to align with map labels
    shaped_data1 = shaped_data.ravel()
    #store data aligned with labels
    df_raveled_data.append(shaped_data1)
    return
#generate labels for each sample
for scan_set, label in zip(scan_sets, sample_labels):
    make_labels_and_shape_data_for_boxplots(scan_set, label)

#merge intermediate lists into final form for pandas df
flat_samp_labs = [item for sublist in df_samp_labels for item in sublist]
flat_map_labs = [item for sublist in df_map_labels for item in sublist]
flat_data = [item for sublist in df_raveled_data for item in sublist]

#dictionary for pandas df from which to plot boxplots
d = {'Sample Label': flat_samp_labs, 'Map Label':flat_map_labs, 
     'Data':flat_data}
#pandas df for seaborn boxplot function
df = pd.DataFrame(data=d)
df.to_csv(r'C:\Users\Trumann\Desktop\xbic_arrays_for_boxtplots.csv')
#plot boxplots 
#sns.boxplot(x='Sample Label', y='Data', hue='Map Label',data=df, palette="Set1")