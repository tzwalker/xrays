These programs extract desired data from fitted H5 files collected at Argonne National Lab. To facilitate navigation of the project, the following syntax will be used to reference functions within modules: "module.py/function_definition".


home_abs.py/get_layer_iios(samples, elements, beam_settings, layer)
# returns iio_matrix with samples as rows and user defined elements as columns
	# cumulative_upstream_attenuation returns array of corresponding iios for element string included in "elements_for_iios",
	# the user must decide which iios are relevant
		# for example, if the stack is Mo/ZnTe/CdTe/CdS/SnO2, 
		# the upstream atten. of Mo is meaningless as it is the top layer
	# the program is not configured for calculating iios of only the top layer
		# though it should easily be adaptable to perform such calculation
		
	# an especially thin (<10nm) layer, can be excluded from stack entry the sample dicts
		# as the thickness of the monolayer produces a very small difference in the avg iio results
		# one may still calculate Cu attn. if no Cu layer is present
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
