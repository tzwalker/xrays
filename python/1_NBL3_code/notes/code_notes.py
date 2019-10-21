### f_corr_pearsons.py
#samp = NBL3_2
#scans = [0,1,2]
#model = 'c_kmodels'
#data_key = 'c_reduced_arrs'
# column index of channel in which you wish to search for max or min medians
#channel_of_interest = 0 
# input 'high' or 'low' to get cluster with highest or lowest values among the clusters
    # not configured to find relative performance of 'medium' clusters
#clusters_of_interest = 'high'
# returns 3D pearson correlation coeff matrix for each scan
    # based off the highest or lowest cluster of the given feature
    # example of process:
        # find cluster with highest xbic value for a given scan (channel_of_interest = 0)
        # calculate correlation matrix between the elements and xbic in that cluster
        # repeat for the length of 'scans'
        
# two compenents to finding cluster data
# example: 'high' xbic cluster
    # compenent 1: the channel you want to 
# focus_channel --> 'high' xbic finds medians of feature, i.e. the column in all_channel_medians
# focus_cluster finds row of cluster...

# clustering performed with reduced_stand arrays, but map retrieved from reduced_normal-unit
    # no error thrown because both arrays are same length
    # but need to check if there's a difference in the mask produced
        # need to check using arrs as reduced cannot be shaped easily
    # RESULT: clustering mask seemed identical when only using a single cluster channel
#--> taking Cu, Cd, Te, and Mo (skipped Zn) in bad geometry scans
    # these beamtimes were run at 12.7 keV, and therefore have more XRF channels
    
#a[:, indices[:,None], indices] # --> in 3d array, get specified row and column indices
    
# find elements and return normalized maps of elements using numpy; note this turned out not to be as flexible
    #as lists, in that the order of the elements must be ordered that same as in the h5 file)


### quick plotting roughness lines ###
# labels for legend are automatically genrated
# =============================================================================
# label_nums = roughnesses * 100
# label_list = []
# for num in label_nums:
#     b = int(num)
#     c = str(b)
#     d = '+/- ' + c + '%'
#     label_list.append(d)
# 
# # note these list lengths must be greater than or equal to the steps in 'roughnesses'
# color_list = ['r', 'b', 'g', 'c', 'm', 'r', 'b', 'g', 'c']
# line_list = ['--', '--','--','--', '--', '-.', '-.', '-.', '-.']
# # plot
# fig, ax = plt.subplots()
# plt.plot(no_rough_in_um, no_rough_iio, 'k', label = 'No roughness')
# for rough_down, rough_up, l, c, lab in zip(ele_rough_iios_down, ele_rough_iios_up, line_list, color_list, label_list):
#     plt.plot(no_rough_in_um, rough_down, linestyle = l, color = c, label = lab)
#     plt.plot(no_rough_in_um, rough_up, linestyle = l, color = c)
# # axis settings
# plt.xlabel('CdTe Thickness (um)', fontsize = 16)
# plt.ylabel('% ' + ele + ' Signal', fontsize = 16)
# ax.tick_params(axis = 'both', labelsize = 14) 
# plt.ylim([0, 1.0])
# plt.grid()
# ax.legend()
# plt.legend(prop={'size': 14})
# plt.show()
# =============================================================================

Notes to self:
# can one estimate the placement/thickness of the Cu layer better using SIMS or xsect XRF?
# ran code for 75 degree geometry and got identical cumulative_upstream attenuation
    # as those from Reabsorption Explore Plots slide 42 in consolidated notes1.ppt
			
	e_statistics.py
	    # do i want to standardize before or after clustering...?
        # if only clustering features of the same scale, no
        # if clustering features with different scale, yes 
    
	e_statistics.py/reduce_arrs(sample_dicts, bad_channel, loaded_ele_channels, standard_deviation_control)
        # this function assumes the electrical channel will be of better quality than any XRF
        # 'bad channel' string is any element string in the 'loaded_ele_channels' list
        # this function only uses the standardized data of each channel
            # therefore the standard deviations of each channel is close to unity
        # 'standard_deviation_control' defines the number of standard deviations away from the mean
        # that set the bounds for data in 'bad_channel';
            # within 'bad_channel', find all samples (pixels) between (mean +/- 'standard_deviation_control' * sigma)
			# keep only the indices of these samples in ALL loaded channels (including electrical)
			# store smaller arrays in '...reduced_arrs' sample dictionary key
            # note this fucntion essentially changes the shape of the map...
                # replacing with nan is an option, but is avoided for stat processing
            # clustering can be done with either the reduced stat arrays (reccommended) 
                # or the complete standardized arrays
        # --> outliers in one channel do not qualify as outliers in another 
        # --> one channel needs to be specified as the channel with which to exclude pixels
        # --> the channel with the most outliers (values ouside the specified boundaries above)
            # is not suitable criteria; Cd channel actually 
            # has more of these points than Cu in the arr tested
            # therefore, specfiy the channel yourself
	
	d_clustering.py/get_mask(sample_dicts, mask_channel, loaded_ele_channels, number_of_clusters)
		# this function does not discriminate between XBIC or XBIV as mask_channel, 
			# respective masks will be generated for each set of XBIC and XBIV scan sets of a sample
			# if you'd like to see exactly how the masks are generated, see defs in d_clustering.py
	
	d_clustering.py/kclustering(sample_dicts, number_of_clusters, features_to_cluster, loaded_ele_channels, outlier_switch)
		# 'outlier_switch':
			# 0 --> for whole, no NaN, original data (in physical units)
			# 1 --> for whole, no NaN, standardized original data
				# the data and each channel was standardized independently
			# 2 --> for reduced original data arrays; original data will be clustered
			# 3 --> for reduced standardized arrays; standardized arays of either whole or reduced original data will be clustered (depends on whether reduce_arrs() is run)
		WARNING: do not use outlier_switch == 2 or 3 if 'e_statistics.reduce_arrs()' is not run; these data will not exist in th sample dictionary;
		you will likely get a KeyError as the dictionary is accessed

	
Obsolete debugging notes, for developer reference only:
for clustering.get_mask(sample_dicts, mask_channel, element_list, number_of_clusters)
# note: the label array of the clustered
    # mask_channel only corresponds to the channel
    # that was first processed; i.e. it does not 
    # get overwritten when the mask_channel changes...
    # debugging:
        # the first index of scn_clst_arr.labels_ changes when mask_channel was changed
        # the cluster algorithim does NOT cluster the same if the algorithim is run
            # more than once on the same mask_channel
                # --> increase the number of iterations?

# setdefault() method does nothing if key already exists,
# update dict with new values if mask_channel was changed
    # or even if the clustering is run again
