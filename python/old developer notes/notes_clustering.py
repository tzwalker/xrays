### NOTES: d_clustering.py ###
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## debugging masking definitions
def get_index_in_user_ele_list(s, E):               # copied from d_clustering.py
    for i, e in enumerate(E):                       
        if s == e[0:2]:                             # test first two characters of ele
            ele_i = i                               # use index of matched ele in 'elements' list
    return ele_i

def get_ele_maps(samp_dict, scan_i, corr_channels, user_channels):
    ele_maps = []
    for ch in corr_channels:
        ele_i = get_index_in_user_ele_list(ch, user_channels) # this index should match the index of the given element in the list 'elements'
        e_map = samp_dict['elXBIC_corr'][scan_i][ele_i][:,:-2] # remove nan columns to match shape of kclust_arrs
        ele_maps.append(e_map)
    return ele_maps

def apply_mask(samps, channels_to_correlate, channels_inputed_by_user):
    for samp in samps:
        correlated_channels_in_ea_scan = []
        for scan_i, (c_model, v_model) in enumerate(zip(samp['c_kclust_arrs'], samp['v_kclust_arrs'])):
            stat_XBIC_map = samp['XBIC_maps'][scan_i][:,:-2] # assign matching elect map, remove nan columns
            to_be_stat_maps = get_ele_maps(samp, scan_i, channels_to_correlate, channels_inputed_by_user)
            # print(np.shape(stat_XBIC_map))
            # print(np.shape(to_be_stat_maps[0])) # good, shapes of these arrays match eachother
            # combine ele and elect lists
            to_be_stat_maps.insert(0, stat_XBIC_map) # maintain XBIC map in correct index position (0)
            # list comp for loop to reshape each array into one column
            stat_arrs = [m.reshape(-1,1) for m in to_be_stat_maps] # these arrays are of appropriate len
            # build clust dicts from model
            C_dict_clust_indices_of_clust_ele = {str(clust_num): np.where(c_model.labels_ == clust_num)[0] for clust_num in range(c_model.n_clusters)}
            # np.take application, (n clusters) * (n_correlate_ele + 1) = length of this list
            other_map_clusters = [[np.take(other_map, index_list) for index_list in C_dict_clust_indices_of_clust_ele.values()] for other_map in stat_arrs]
            # structure of above list follows [['XBIC for each cluster'], ['ele1 for each cluster'], ...]
            correlated_channels_in_ea_scan.append(other_map_clusters)
        key = 'C_kclust_masked' 
        samp.setdefault(key, correlated_channels_in_ea_scan)        # make samp dict entry
        samp['C_kclust_masked'] = correlated_channels_in_ea_scan    # update entry if needed
    return other_map_clusters

## used masking defintions
def make_IV_mask_arrays(samps, N):
    for samp in samps:
        # cluster XBIC scans first
        c_clust_arrays = []
        for i, scan in enumerate(samp['XBIC_maps']):
            stat_c_map = scan[:,:-2]                # remove nans
            c_arr = stat_c_map.reshape(-1,1)        # array data for proper clustering
            model = KMeans(init='k-means++', n_clusters=N, n_init=10) # setup model
            scn_clst_arr = model.fit(c_arr)         # cluster
            c_clust_arrays.append(scn_clst_arr)     # build mask arrays for each scan
        key = 'c_kclust_arrs'
        samp.setdefault(key, c_clust_arrays)        # make arrays
        samp['c_kclust_arrs'] = c_clust_arrays      # update arrays
        # cluster XBIV maps
        v_clust_arrays = []
        for i, scan in enumerate(samp['XBIV_maps']):
            stat_v_map = scan[:,:-2]                # remove nans
            v_arr = stat_v_map.reshape(-1,1)        # array data for proper clustering
            model = KMeans(init='k-means++', n_clusters=N, n_init=20) # setup model
            scn_clst_arr = model.fit(v_arr)         # cluster
            v_clust_arrays.append(scn_clst_arr)     # build mask arrays for each scan
        key = 'v_kclust_arrs' 
        samp.setdefault(key, c_clust_arrays)        # make arrays
        samp['v_kclust_arrs'] = v_clust_arrays      # update arrays
    return 

def get_index_in_user_ele_list(s, E):
    for i, e in enumerate(E):
        if s == e[0:2]:                             # test first two characters of ele
            ele_i = i                               # use index of matched ele in 'elements' list
    return ele_i

def make_ele_mask_arrays(ele_i, samps, N):
    for samp in samps:
        # cluster ele in XBIC maps first
        c_clust_arrays = []
        for scan in samp['elXBIC_corr']:
            ele_map = scan[ele_i]                   # get element map for mask
            stat_ele_map = ele_map[:,:-2]           # remove nans
            ele_arr = stat_ele_map.reshape(-1,1)    # array data for proper clustering
            model = KMeans(init='k-means++', n_clusters=N, n_init=10)
            scn_clst_arr = model.fit(ele_arr)       # cluster
            c_clust_arrays.append(scn_clst_arr)
        key = 'c_kclust_arrs'
        samp.setdefault(key, c_clust_arrays)        # make arrays
        samp['c_kclust_arrs'] = c_clust_arrays      # update arrays
        # cluster ele in XBIV maps
        v_clust_arrays = []
        for scan in samp['elXBIV_corr']:
            ele_map = scan[ele_i]                   # get element map for mask
            stat_ele_map = ele_map[:,:-2]           # remove nans
            ele_arr = stat_ele_map.reshape(-1,1)    # array data for proper clustering
            model = KMeans(init='k-means++', n_clusters=N, n_init=10)
            scn_clst_arr = model.fit(ele_arr)       # cluster
            v_clust_arrays.append(scn_clst_arr)
        key = 'v_kclust_arrs'
        samp.setdefault(key, v_clust_arrays)
        samp['v_kclust_arrs'] = v_clust_arrays      # update arrays
    return 
def get_mask(samples, mask, eles, N):
    if mask == 'XBIC' or mask == 'XBIV':
        make_IV_mask_arrays(samples, N)
        print('this is the electrical  mask loop')
    else:
        ele_i = get_index_in_user_ele_list(mask, eles)
        make_ele_mask_arrays(ele_i, samples, N)
        print('this is the element mask loop')
    return

# make mask
cu_map = NBL3_2['eXBIC_corr'][0][0] # practice map, [area 1 : 2019_03][Cu]
stat_cu_map = cu_map[:,:-2] # eliminate nan
cu_arr = stat_cu_map.reshape(-1, 1) # array data to cluster each entry individually
model = KMeans(init='k-means++', n_clusters=3, n_init=10)
model.fit(cu_arr) # cluster array

Z = model.labels_
A = Z.reshape(np.shape(stat_cu_map)) # for cluster map
# other map to mask to
XBIC_map = NBL3_2['XBIC_maps'][0]
stat_XBIC_map = XBIC_map[:,:-2] # eliminate nan columns
XBIC_arr = stat_XBIC_map.reshape(-1, 1) # array data to identify indices matching with those in cluster labels
# to find actual values of clusters in other maps
dict_of_cu_map_cluster_indices = {str(i): np.where(Z == i)[0] for i in range(model.n_clusters)}
XBIC_from_clusters_of_cu = []
for index_list in dict_of_cu_map_cluster_indices.values():
    matched_values_in_XBIC = np.take(XBIC_arr, index_list)
    XBIC_from_clusters_of_cu.append(matched_values_in_XBIC)

cu_clust_zero = cu_arr[ClusterIndicesNumpy(0,model.labels_)]
cu_clust_one = cu_arr[ClusterIndicesNumpy(1,model.labels_)]
cu_clust_two = cu_arr[ClusterIndicesNumpy(2,model.labels_)]

## from home file
# USER input: enter 'XBIV', 'XBIC', or any element in 'elements_in'
number_of_clusters = 3
mask_channel = 'Cu'  # XRF line need not be included, but if it is no error will rise
d_clustering.get_mask(samples, mask_channel, elements_in, number_of_clusters)
# USER input:  XRF line need not be included, but if it is no error will rise
    # note masks are automatically applied to 'XBIC/V' channels
    # do not include 'XBIC/V' in 'correlate_elements' list
    # position eles in same manner as in ele_in, for use in stadardize_channels()
        # should make this more flexible in the future, but for now this is will have to do
correlate_elements = ['Cu', 'Cd'] 
# calling the mask on the element used to make the mask 
    # captures the actaul quantities within each cluster (output of kmeans model is just labels)
e_statistics.apply_mask(samples, correlate_elements, elements_in)
educe_arrs(samples, 'Cu', elements_in, 2, ['c_stat_arrs', 'v_stat_arrs']) 

# --> left off: revised boundaries with which to remove data samples before tranformation
    # whole standardized arrays exist in samp dictionary along with whole original data
    # check if the function above will make reduced scan_channel_arrays for either the original data
        # and the standardized data

 def standardize_channels(samps):
     scaler = skpp.Stahttps://docs.scipy.org/doc/numpy/reference/generated/numpy.delete.htmlndardScaler()
     for samp in samps:
         # apply_mask() also saves an arrayed version of every map; this is a requirement for proper statistics and standardization
         c_stand_arrs = [[scaler.fit_transform(channel) for channel in stat_arr] for stat_arr in samp['c_stat_arrs']]
         # essentially the clustered arrays are just one level deeper, i.e. each channel has n clusters
         c_stand_clust_arrs = [[[scaler.fit_transform(clust.reshape(-1,1)) for clust in channel] for channel in stat_arr] for stat_arr in samp['C_kclust_masked']]
         # do the same with XBIV maps
         v_stand_arrs = [[scaler.fit_transform(channel) for channel in stat_arr] for stat_arr in samp['v_stat_arrs']]
         v_stand_clust_arrs = [[[scaler.fit_transform(clust.reshape(-1,1)) for clust in channel] for channel in stat_arr] for stat_arr in samp['V_kclust_masked']]
         
         c_key = 'c_stat_arrs_stand'
         v_key = 'v_stat_arrs_stand'
         samp.setdefault(c_key, c_stand_arrs)
         samp.setdefault(v_key, v_stand_arrs)
         samp['c_stat_arrs_stand'] = c_stand_arrs
         samp['v_stat_arrs_stand'] = v_stand_arrs
         
         c_key = 'c_kclust_arrs_stand'
         v_key = 'v_kclust_arrs_stand'
         samp.setdefault(c_key, c_stand_clust_arrs)
         samp.setdefault(v_key, v_stand_clust_arrs)
         samp['c_kclust_arrs_stand'] = c_stand_clust_arrs
         samp['v_kclust_arrs_stand'] = v_stand_clust_arrs
     return

#use with apply_mask() maybe...
def get_index_in_user_ele_list(s, E):               # copied from d_clustering.py
  for i, e in enumerate(E):                       
      if s == e[0:2]:                             # test first two characters of ele
          ele_i = i                               # use index of matched ele in 'elements' list
  return ele_i

def get_ele_maps(samp_dict, scan_i, corr_channels, user_channels):
  ele_maps = []
  for ch in corr_channels:
      ele_i = get_index_in_user_ele_list(ch, user_channels) 
      e_map = samp_dict['elXBIC_corr'][scan_i][ele_i][:,:-2]
      ele_maps.append(e_map)
  return ele_maps

def apply_mask(samps, channels_to_correlate, channels_inputed_by_user):
  for samp in samps:
      # apply mask to channels in XBIC scans first
      c_correlated_channels_in_ea_scan = []
      for scan_i, c_model in enumerate(samp['c_kclust_arrs']):
          clust_ele_mask_dict = {str(clust_num): np.where(c_model.labels_ == clust_num)[0] for clust_num in range(c_model.n_clusters)}
          other_map_clusters = [[np.take(other_map, mask_indices) for mask_indices in clust_ele_mask_dict.values()] for other_map in stat_arrs]
          c_correlated_channels_in_ea_scan.append(other_map_clusters) # save masked arrays 
      key = 'C_kclust_masked' 
      samp.setdefault(key, c_correlated_channels_in_ea_scan)        # store masked arrays
      samp['C_kclust_masked'] = c_correlated_channels_in_ea_scan    # update entry if needed
       # apply mask to channels in XBIV scans
      v_correlated_channels_in_ea_scan = []
      for scan_i, c_model in enumerate(samp['c_kclust_arrs']):
          clust_ele_mask_dict = {str(clust_num): np.where(c_model.labels_ == clust_num)[0] for clust_num in range(c_model.n_clusters)}
          other_map_clusters = [[np.take(other_map, mask_indices) for mask_indices in clust_ele_mask_dict.values()] for other_map in stat_arrs]
          v_correlated_channels_in_ea_scan.append(other_map_clusters)
      key = 'V_kclust_masked' 
      samp.setdefault(key, v_correlated_channels_in_ea_scan)        # make samp dict entry
      samp['V_kclust_masked'] = v_correlated_channels_in_ea_scan    # update entry if needed
  return

### troubleshooting kmeans iterations
#need some way to visualize this... ask Tara
# will adding more data to the optimization reduce the number of local minima?
    # rerun code above with full data array
    # result: still varied convergence
# using labels to index into real data is a no-go as the reustling arrays will be of different lengths
    # according to the difference in the labels (which is what i'm trying to determine)
    # for simplicity, only use xbic channel to cluster for now
# the most common sums resulting from summing along rows of clust_labels_from_each_attempt 
    # will identify a data point that was put in the same cluster between each clustering attempt
    # exception: if all cluster attempts place a data point in cluster "0",
    # then the sum of that row will equal zero (this is unlikely)
        # solution would be to first check the summed_rows array for any sums of zero
summed_rows = np.sum(clust_labels_from_each_attempt1, axis=1)
if 0 in summed_rows:
    print('cannot use bincount')
else:
    print("take indices of 'most common' sums")
try_bincount = np.bincount(summed_rows)
# find indices of "most common" sums
# note this threshold of 100 will have to scale with the number of kmeans iterations, 
    # for now the number of iterations will be 10
    # future suggestion: make threshold 10x the number of iterations
trim_bincount = np.array(np.where(try_bincount > 100))
indices_of_consistently_clustered_data = np.where(summed_rows == trim_bincount)
indices_of_consistently_clustered_data = [np.array(np.where(summed_rows==important_sum)) for important_sum in trim_bincount[0]]
# combine all these indices in preparation for indexing into actual data
indices_of_consistent_data_combined = np.vstack(indices_of_consistently_clustered_data)

### old definitions before making code for many ktrials 
def get_column_indices(clust_chans, available_chans): # this is finding the column in the stat arrays that corresponds to the channels you want to cluster
    if 'all' in clust_chans:
        indices = list(range(len(available_chans) + 1)) # add one to include XBIC array
        return indices
    else:
        indices = []
        for index, channel in enumerate(available_chans):
            if channel[0:2] in clust_chans:
                index = index + 1 # XBIC is always @ index 0
                indices.append(index)
        if 'perf' in clust_chans:
            indices.insert(0,0)
        # do not need to sort indices because i'm iterating over the available channels,
            # the indices of which, by earlier design in e_statistics.py,
            # correspond directly to those in the stat arrays
        return indices

def find_clusters(samps, num_of_clusters, clust_channels, loaded_XRF, dict_data):
    column_indices = get_column_indices(clust_channels, loaded_XRF) # returns indices of columns of stat/standardized array for scan; used to cluster only channels of interest
    for samp in samps:
        c_scan_models = []
        for preclust_arr in samp[dict_data[0]]:
            trimmed_pre_clust_arrs = preclust_arr[:, column_indices] # use only array columns of interest
            model = KMeans(init='k-means++', n_clusters=num_of_clusters, n_init=10) # define model (must be included in this loop to reset for each scan/pre_clust_arrs)
            clust_arrs = model.fit(trimmed_pre_clust_arrs) # perform clustering
            c_scan_models.append(clust_arrs) # save model
        samp_dict_grow.build_dict(samp, 'c_kmodels', c_scan_models) # store models
        v_scan_models = []
        for preclust_arr in samp[dict_data[1]]:
            trimmed_pre_clust_arrs = preclust_arr[:, column_indices] # use only array columns of interest
            model = KMeans(init='k-means++', n_clusters=num_of_clusters, n_init=10) # define model (must be included in this loop to reset for each scan/pre_clust_arrs)
            clust_arrs = model.fit(trimmed_pre_clust_arrs) # perform clustering
            v_scan_models.append(clust_arrs) # save model
        samp_dict_grow.build_dict(samp, 'v_kmodels', v_scan_models) # store models
    return

def kclustering(samps, N, clust_channels, available_channels, outlier_switch):
    if outlier_switch == 0: # use this switch for original data without two nan columns on the end (removed in )
        samp_dict_data = ['c_stat_arrs', 'v_stat_arrs'] 
        find_clusters(samps, N, clust_channels, available_channels, samp_dict_data) 
    elif outlier_switch == 1: # use this switch for whole standardized original data
        samp_dict_data = ['c_stand_arrs', 'v_stand_arrs'] 
        find_clusters(samps, N, clust_channels, available_channels, samp_dict_data)
    elif outlier_switch == 2: # use this switch for reduced data of the original data
        samp_dict_data = ['c_reduced_arrs', 'v_reduced_arrs'] 
        find_clusters(samps, N, clust_channels, available_channels, samp_dict_data)
    elif outlier_switch == 3: # use this switch for reduced data of the original data
        samp_dict_data = ['c_redStand_arrs', 'v_redStand_arrs'] 
        find_clusters(samps, N, clust_channels, available_channels, samp_dict_data)
    return

def get_focus_cluster_index(medians, chan_column_index, focus_cluster):
    medians_of_focus_channel = medians[:,chan_column_index] # if chan_column_index = 0 --> gets xbic medians; they are first column in medians_of_each_cluster
    if focus_cluster == 'high':
        cluster_index = np.argmax(medians_of_focus_channel)# returns index of largest median cluster
    elif focus_cluster == 'low':
        cluster_index = np.argmin(medians_of_focus_channel)  # returns index of smallest median cluster
    return cluster_index

def get_focus_cluster_data(real_data,clust_labs,clust_nums,focus_channel, focus_cluster):
    # separate data into clusters
    cluster_data = [real_data[np.where(clust_labs == clust)[0]] for clust in clust_nums]
    # array of median values of the data in each cluster 
        # row --> cluster; column --> median of feature (xbic,cu,cd,...)
    medians_of_clusters = np.array([np.median(cluster, axis=0) for cluster in cluster_data]) 
    focus_cluster_row_index = get_focus_cluster_index(medians_of_clusters, focus_channel, focus_cluster)
    # extract channels of focus cluster; transpose to prep for correlation
    data_of_focus_cluster = cluster_data[focus_cluster_row_index].T 
    return data_of_focus_cluster

def plot_pearson_matrix(corr1, corr2, eles):
    cols = ['XBIC'] + eles
    corr1 = pd.DataFrame(corr1, columns=cols, index=cols)
    corr2 = pd.DataFrame(corr2, columns=cols, index=cols)
    # plot
    sns.set(style="white")
    # generate a mask for the upper triangle
    mask = np.zeros_like(corr1, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    # make cbar ticks
    cbar_tick={'ticks': list(list(np.linspace(-1,1,5))), 'label': 'Pearson Correlation Coeff.'}
    cbar_tick1={'ticks': list(list(np.linspace(-1,1,5))), 'label': 'Standard Deviation'}
    fig, (ax0, ax1) = plt.subplots(2,1)
    plt.tight_layout()
    sns.heatmap(corr1, mask=mask, cbar_kws=cbar_tick, ax=ax0,
                 cmap='coolwarm',annot=True, vmin=-1, vmax=1)
    ax0.title.set_text('Average Linearity Between Scans')
    sns.heatmap(corr2, mask=mask, cbar_kws=cbar_tick1, ax=ax1,
                 cmap='Greys',annot=True, vmin=0, vmax=1)
    ax1.title.set_text('Standard Devation')
    return

def stats_after_many_kmeans_trials(samp, scans, data_key, model_key, cluster_number, 
                           focus_channel, focus_cluster, iterations, eles):
    correlation_of_all_scans = []
    deviation_of_all_scans = []
    for scan in scans:
        real_data = samp[data_key][scan]
        model_xbic_data = samp[model_key][scan][:,focus_channel]
        model_xbic_data = model_xbic_data.reshape(-1,1)
        model =  KMeans(init='k-means++', n_clusters=cluster_number, n_init=10)
        
        correlations_of_all_clusterings = []
        count = 0
        while count < iterations:
            clust_xbic = model.fit(model_xbic_data)
            clust_labs = clust_xbic.labels_
            clust_nums = list(range(cluster_number))
            data_of_focus_cluster = get_focus_cluster_data(real_data,
                                                           clust_labs,
                                                           clust_nums,
                                                           focus_channel,
                                                           focus_cluster)
            # pearson correlation matrix of focus cluster
            clust_corrcoeffs = np.corrcoef(data_of_focus_cluster)
            # store coefficient matrix of this clustering
            correlations_of_all_clusterings.append(clust_corrcoeffs)
            count = count+1
        correlations_of_all_clusterings = np.array(correlations_of_all_clusterings)
        # calculate average of coeff matrices for all clusterings performed
        avg_corr_kmeans = np.mean(correlations_of_all_clusterings, axis=0)
        std_corr_kmeans = np.std(correlations_of_all_clusterings, axis=0)
        #plot_pearson_matrix(avg_corr_kmeans, std_corr_kmeans, elements)
        # store average coeff matrix of this scan
        correlation_of_all_scans.append(avg_corr_kmeans)
        deviation_of_all_scans.append(std_corr_kmeans)
        
    correlation_of_all_scans = np.array(correlation_of_all_scans)
    deviation_of_all_scans = np.array(deviation_of_all_scans)
    # calculate the average of coeff matrices for all scans looked at
    avg_corr_scans = np.mean(correlation_of_all_scans, axis=0)
    std_corr_scans = np.std(correlation_of_all_scans, axis=0)
    plot_pearson_matrix(avg_corr_scans, std_corr_scans, eles)
    return avg_corr_scans, std_corr_scans
