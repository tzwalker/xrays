### boxplotting ###
# -*- coding: utf-8 -*-
"""
Trumann
Wed Sep 11 11:46:27 2019

### batch plot boxplots ###
"""
import numpy as np
import matplotlib.pyplot as plt

def plot_more_boxes(model, key, scans):
    for samp, samp_name in zip(samples, samp_names):
        for scan in scans:
            clust_labs = samp[model][scan].labels_
            data = [samp[key][scan][:,i] for i, ele in enumerate(samp[key][scan].T)] # this format is necessary for boxplots
            plot_clust_boxes(clusts, clust_labs, data, scan, samp_name)
    return

def plot_clust_boxes(clust_nums, clust_labs, data, scan, sam):
    fig, axs = plt.subplots(len(data),1)
    plt.tight_layout()
    clusters_for_each_channel = []
    for channel in data: # data is a list; each item is a column from the original numpy arr
        cluster_list = [channel[np.where(clust_labs == clust)[0]] for clust in clust_nums]
        clusters_for_each_channel.append(cluster_list)
    for i, clusters in enumerate(clusters_for_each_channel):
        bp_dict = axs[i].boxplot(clusters, showfliers=False)
        for line in bp_dict['medians']:
            med = line.get_ydata()                  # get median value array
            xpoint, ypoint = line.get_xydata()[1]   # get plot coordinates of median
            # annotate this position with median as string
            axs[i].annotate(xy=(xpoint,ypoint), 
               s=' ' + "{:.4g}".format(med[0]), 
               horizontalalignment='left') # add text with formatting
        axs[i].title.set_text(boxplot_names[i])
    return

#samp_names = ['NBL3_2', 'NBL3_3', 'TS58A']
#boxplot_names = ['reduced xbic', 'reduced cu','reduced cd','reduced te']
#plot_more_boxes(model, data_key, scans)
def clust_scatter_matrix(cluster_data, elements):
    cols = elements.insert(0, 'xbic')
    df = pd.DataFrame(cluster_data[0], columns = cols) # make for loop to go over each cluster in cluster_data
    pd.plotting.scatter_matrix(df, alpha = 0.2)
    return

def return_cluster_unique_lists(cluster_data):
    
    medians = [np.median(cluster, axis=0) for cluster in cluster_data]
    arr_medians = np.array(medians).T # for convenience of max/min identification between clusters
    
    indices_of_median_maxes = []
    indices_of_median_mins = []
    for channel in medians:
        index_of_median_maxes = channel.index(max(channel)) #--> really "cluster containing median max"
        index_of_median_mins = channel.index(min(channel))  #--> really "cluster containing median min"
        indices_of_median_maxes.append(index_of_median_maxes)
        indices_of_median_mins.append(index_of_median_mins)
    
    # these lists trade off, producing a unique identifier for a given combo in the max XBIC cluster
    indices_test_cluster0 = [i for i, cluster in enumerate(indices_of_median_maxes) if cluster == 0]
    indices_test_cluster1 = [i for i, cluster in enumerate(indices_of_median_maxes) if cluster == 1]
    indices_test_cluster2 = [i for i, cluster in enumerate(indices_of_median_maxes) if cluster == 2]
    return 

### basic boxplots of raw data 
cu_maps = [samp['elXBIC_corr'][scan][0][:,:-2] for samp in samples]
xbic_maps = [samp['XBIC_maps'][scan][:,:-2] for samp in samples]

cu_data = [samp['elXBIC_corr'][scan][0][:,:-2].ravel() for samp in samples]
xbic_data = [samp['XBIC_maps'][scan][:,:-2].ravel() for samp in samples]
    
x_boxlabs = [samp['Name'] for samp in samples]

fig, axs = plt.subplots(1,2)
plt.tight_layout()
axs[0].imshow(cu_maps[2], origin='lower')
axs[1].imshow(xbic_maps[2], origin='lower')


# -*- coding: utf-8 -*-
"""
Trumann
Wed Oct  9 11:27:57 2019
### p-value test via permuations ###
"""

### runs a simple permutation test for any two variables of interest
# this is a version of numerically computing a p-value,
# without assumptions of the distributions of the data
    # to be compared with the p-values returned from pearson and spearman
    
# keeping x constant, shuffles y and computes a new pearson correlation coefficient
    # appends this coeff to a list
    # converts list to array
    # find all indices with values less than the coeff of the original data
    # convert boolean to binary
    # proportion of shuffeld_r values that do not exceed the original correlation calc
        # = (# of values less than coeff of original data / # of shuffle trials)

# pvalue --> probability the correlation happened by "accident"
      
 # program uses max number of shuffles equal to the number of pixels in the map;
 # if all shuffles result in corrcoef < test_stat, then the returned value will be 0
 # not enough shuffles may have been performed, but can compare to the spearman and pearson
 # for validation

# scan level
real_data = NBL3_3['c_reduced_arrs'][0]
number_of_clusters = 3
trials = NBL3_3['c_kmeans_trials'][0]
# trial level
focus_cluster_row = 'high'
focus_channel_col = 0 # XBIC
permutation_x = 1 # column idx for Cu in data array=1
permutation_y = 3 # column idx for Te in data array=3
Cu_Te_corrs = []

def permutation_test(vars_of_interest, test_statistic):
    count = 0
    x = vars_of_interest[0,:].reshape(-1,1)
    y = vars_of_interest[1,:].reshape(-1,1)
    # repeat shuffle as many times as there are observations;
    # number of observations equal to the number of cells in a raveled map
    repeat_shuffle = np.shape(real_data)[0] 
    rand_corrs = []
    while count <= repeat_shuffle:
        np.random.shuffle(y) # shuffles y array
        combine_xy = np.concatenate((x, y), axis=1)
        combine_xy = combine_xy.T
        rand_corr = np.corrcoef(combine_xy)
        rand_corrs.append(rand_corr[0,1])
        count = count + 1
    rand_corrs = np.array(rand_corrs)
    bool_arr = rand_corrs <= test_statistic[0,1]
    binary_arr = bool_arr.astype(int)
    corrs_more_than_test_stat =  1 - np.sum(binary_arr[:-1]) / repeat_shuffle
    return corrs_more_than_test_stat


cluster_data = [real_data[np.where(trials[0]==clust)[0]] for clust in list(range(number_of_clusters))]
focus_cluster = d_clustering.get_focus_cluster(cluster_data, focus_cluster_row, focus_channel_col)
Cu_Te_extracted = focus_cluster[[permutation_x,permutation_y],:] # channel columns in data array
Cu_Te_corr_starr = np.corrcoef(Cu_Te_extracted) # test pearson statistic
pvalue = permutation_test(Cu_Te_extracted, Cu_Te_corr_starr)

    