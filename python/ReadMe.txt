Home file info:
	# WARNING: these programs are completely dependent on the dictionary keys 
		# specified by the developer (that's me, Trumann)
		# if you wish to change the dictionary keys, you will need to go within all definitions 
			# and change them accordingly
		# i hope to make roadmap of sorts for the key dependencies at some point so this can be done if desired, 
			# but for now avoid changing the keys at all possible costs! it will result in complete program failure
	# ele_iios calculated using iio_vs_depth_simulation.py
		# Cu, Cd_L, and Te_L iios of CdTe layer found by typing in each element,
		# and taking the average of the resulting iio vs. depth array.
		# attenuation by upstream Mo and ZnTe accounted
	# should make a ReadMe for that file...

Object lengths/sizes that should always match (in sample dictionaries):





Functions that change/build the sample dictionaries (syntax shown here follows "module.py/def"):
	
	h5_in_elect_scale.py/get_add_h5s(sample_dicts, scan_path)
		# import the H5s
		# makes a list, adds h5s to that list, attaches the complete list to sample dictionary
		
	h5_in_elect_scale.py/scan_scalers(sample_dicts)
		# scales the electrical channel in for either XBIC or XBIV 
			# as long as the scans are in the appropriate list, they will have the relevant scalers applied to them
			# 'c_' prefix denotes the XBIC lockin or stanford settings
			# 'v_' prefix denotes the XBIV locking settings
			# presently the beam V2F values for the scans can be seen in 'beam_conv' dict key
	h5_in_elect_scale.py/get_add_elect_channel(sample_dicts, int)	
		# enter 1 for int if XBIC/V collected through us_ic
		# enter 2 for int if XBIC/V collected through ds_ic
		# WARNING: only useful if all scans being processed had
			# the electrical signal collected through the same ion_chamber channel.
			# If scans are from different beamtimes, and a different ion_chamber scaler
				# was used at each beamtime, this function will not be suitable.
			# If this is the case it is recommended to use different processing 'start' files for the different scans
				# until the get_add_elect_channel() can be modified to accomodate such differences 
		

	
	rummage_thru_h5.py/find_ele_h5s(sample_dicts, element_list)
	# adds key value pairs into sample dictionaries
    # example: 'XBIC_eles': [[17,25], [14, 24]]
        # 17 and 14 are the index positions of the Cu_K map in two different scans
        # 25 and 24 are the index positions of the Cd_L map in two different scans
        # this needs to be done as differences in the data structures could exist from 
            # not fitting all scans using the same config file or processing scans from different beamtimes
	
	
	rummage_thru_h5.py/extract_norm_ele_maps(sample_dicts, normalization_channel, 'roi')
		# adds element maps to sample dictionaries, 
			# normalized to desired scaler and fitted data
				# for 3rd argument:
				# 'roi' --> default if fit works
				# 'fit' --> use when MAPS creates problem with quantification
				
	rummage_thru_h5.py/apply_ele_iios(sample_dicts) 
		# this function requires user input inside rummage_thru_h5.py:
			# the iio keys in the sample dictionaries must match those
				# those inside apply_ele_iios() definition
		# the list structure depends on whether one or more than 
			# one scan is being processed for a given beamtime


	d_clustering.py/get_mask(sample_dicts, mask_channel, elements_in, number_of_clusters)
		# this function does not discriminate between XBIC or XBIV as mask_channel, 
			# respective masks will be generated for each set of XBIC and XBIV scan sets of a sample
			# if you'd like to see exactly how the masks are generated, see defs in d_clustering.py
			
	e_statistics.py
	    # do i want ot perform standardization before or after clustering...?
        # since clustering is performed using many samples of 'one feature', 
        # scale between the samples within the feature are identical and 
        # standardization before clustering is not necessary
	
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
