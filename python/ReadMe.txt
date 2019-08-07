Home file info:
	# WARNING: these programs are completely dependent on the dictionary keys 
		# specified by the developer (that's me, Trumann)
		# if you wish to change the dictionary keys, you will need to go within all definitions 
			# and change them accordingly
		# i hope to make roadmap of sorts for the key dependencies at some point so this can be done if desired, 
			# but for now avoid changing the keys at all possible costs! it will result in complete program failure
	20190805: think i've found a way around the key definitions being fixed... 
	# ele_iios calculated using iio_vs_depth_simulation.py
		# Cu, Cd_L, and Te_L iios of CdTe layer found by typing in each element,
		# and taking the average of the resulting iio vs. depth array.
		# attenuation by upstream Mo and ZnTe accounted
	# should make a ReadMe for that file...
	# if electrical settings are not provided, no XBIC maps will exist
		# more specifically, the list e.g. 'c_stanford' will be length zero
		# and iteration will be performed on this zero length list
	

Object lengths/sizes that should always match (in sample dictionaries):





Functions that change/build the sample dictionaries (syntax shown here follows "module.py/def"):
	
	b_h5_in_elect_scale.py/get_add_h5s(sample_dicts, scan_path)
		# import the H5s
		# makes a list, adds h5s to that list, attaches the complete list to sample dictionary
		
	b_h5_in_elect_scale.py/scan_scalers(sample_dicts)
		# scales the electrical channel in for either XBIC or XBIV 
			# as long as the scans are in the appropriate list, they will have the relevant scalers applied to them
			# 'c_' prefix denotes the XBIC lockin or stanford settings
			# 'v_' prefix denotes the XBIV locking settings
			# presently the beam V2F values for the scans can be seen in 'beam_conv' dict key
	b_h5_in_elect_scale.py/get_add_elect_channel(sample_dicts, int)	
		# enter 1 for int if XBIC/V collected through us_ic
		# enter 2 for int if XBIC/V collected through ds_ic
		# WARNING: only useful if all scans being processed had
			# the electrical signal collected through the same ion_chamber channel.
			# If scans are from different beamtimes, and a different ion_chamber scaler
				# was used at each beamtime, this function will not be suitable.
			# If this is the case it is recommended to use different processing 'start' files for the different scans
				# until the get_add_elect_channel() can be modified to accomodate such differences 
		

	
	c_rummage_thru_h5.py/find_ele_h5s(sample_dicts, loaded_ele_channels)
	# adds key value pairs into sample dictionaries
    # example: 'XBIC_eles': [[17,25], [14, 24]]
        # 17 and 14 are the index positions of the Cu_K map in two different scans
        # 25 and 24 are the index positions of the Cd_L map in two different scans
        # this needs to be done as differences in the data structures could exist from 
            # not fitting all scans using the same config file or processing scans from different beamtimes
	
	
	c_rummage_thru_h5.py/extract_norm_ele_maps(sample_dicts, normalization_channel, 'roi')
		# adds element maps to sample dictionaries, 
			# normalized to desired scaler and fitted data
				# for 3rd argument:
				# 'roi' --> default if fit works
				# 'fit' --> use when MAPS creates problem with quantification
				
	c_rummage_thru_h5.py/apply_ele_iios(sample_dicts) 
		# this function requires user input inside rummage_thru_h5.py:
			# the iio keys in the sample dictionaries must match those
				# those inside apply_ele_iios() definition
		# the list structure depends on whether one or more than 
			# one scan is being processed for a given beamtime
			
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
	
	d_clustering.py/kclustering(sample_dicts, number_of_clusters, features_to_cluster, loaded_ele_channels, outlier switch)
		# 'outlier_switch':
			# 0 --> for whole, no NaN, original data (in physical units)
			# 1 --> for whole, no NaN, standardized original data
				# the data and each channel was standardized independently
			# 2 --> for reduced arrays; either standardized or original data will be clustered
				WARNING: do not use switch == 2 if 'e_statistics.reduce_arrs()' is not run
				as these data will not exist in th sample dictionary;
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
