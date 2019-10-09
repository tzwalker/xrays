# -*- coding: utf-8 -*-
"""
Trumann
Wed Oct  9 11:27:57 2019
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

import d_clustering
import numpy as np

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
    repeat_shuffle = np.shape(real_data)[0] # equal to the number of observations in whole map; the column of master data array
    rand_corrs = []
    while count <= repeat_shuffle:
        np.random.shuffle(y) # shuffles y array; fxn returns None as it randomizes 'in-place'
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

    