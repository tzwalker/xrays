### NOTES: b_h5_in_elect_scale.py ###
# =============================================================================
# 
# # finding elements in h5
# wanted =        ['cu', 'cd', 'te']
# h5_channels =   ['cd', 'fe', 'cu', 'zn', 'se', 'te']
# h5_channels = [x.encode('utf-8') for x in h5_channels]
# 
# def find_eles_in_channel_names(w, chan):
#     chan = [x.decode('utf-8') for x in chan]
#     index_list = [i for i,ele in enumerate(chan) for e in w if e == ele]
#     return index_list
# 
# new_list = find_eles_in_channel_names(wanted, h5_channels)
# 
# # adding elements to sample dictionary
# list_of_lists = NBL3_2['XBIC_eles']
# h5s = NBL3_2['XBIC_h5s']
# 
# def extract_maps(H5s, list_of_lists):
#     maps = []                                                       #initialize master list
#     for H5, channel_indices in zip(H5s, list_of_lists):
#         scan_maps = []                                              #initialize internal (single scan) list
#         XRF_fits = H5['/MAPS/XRF_fits']                             #navigate to structure containing all fitted XRF data
#         for element_index in channel_indices:
#             map_of_interest = XRF_fits[element_index,:,:]           #use element index to extract map of interest
#             scan_maps.append(map_of_interest)                       #build internal list
#     maps.append(scan_maps)                                      #add internal list (i.e. a scan) to master list
#     return 
# 
# list_of_maps = extract_maps(h5s, list_of_lists)
# 
# sample_dict = NBL3_2
# sample_maps = []
# for h5, ch_inds in zip(sample_dict['XBIC_h5s'], sample_dict['XBIC_eles_i']):
#     maps_of_eles_in_scan = [h5['/MAPS/XRF_fits'][ind,:,:]  for ind in ch_inds]
#     sample_maps.append(maps_of_eles_in_scan)
# key = 'test_ele_maps'
# sample_dict.setdefault(key, sample_maps)
# =============================================================================

### NOTES: c_rummage_thru_h5.py ###
# =============================================================================
# 
# #this function performs a strign comparison within the pertinent H5 group and extracts the index of interest
# def get_desired_channel_index(H5_channel_names_as_strings, e):
#     s=0                                                                             #initialize index search
#     for index, channel_string in enumerate(H5_channel_names_as_strings):            #search channel_names for element string
#         if e == channel_string.decode():                                            #compare element string to decoded channel_name string
#             s = index                                                               #get appropriate index
#     return s
# 
# #returns list of lists
# #each internal list represents a scan, and contains the indices of the channels of interest
# #channel indices are required to navigate the H5 data structures
# def get_ChOIs_for_all_scans(files, ChOIs):
#     list_of_indices = []                                            #initialize master list
#     for scan_index, file in enumerate(files):
#         channel_names = file['/MAPS/channel_names']                 #navigate to the structure conatining the channel names as element strings, e.g. 'Cd_L'
#         decoded_ele_string_indices = []                             #initialize internal list
#         for ele in ChOIs:
#             s = get_desired_channel_index(channel_names, ele)       #perform string comparison between 'channels of interest' and 'channel names', and extract index of interest
#             decoded_ele_string_indices.append(s)                    #build internal list
#         list_of_indices.append(decoded_ele_string_indices)          #add internal list (i.e. a scan) to master list
#     return list_of_indices
# 
# #intiallyt for find_ele_in_h5s()
#         c_indices = [get_elem_indices(ChOIs, file['/MAPS/channel_names']) for file in samp['XBIC_h5s']]
#         v_indices = [get_elem_indices(ChOIs, file['/MAPS/channel_names']) for file in samp['XBIV_h5s']]
#         
#         sample_dict.setdefault(c_indices)
#         key = samp['Name']
#         
#         sample_dict.setdefault(key, scan_dict)
#     
# # this function uses the element indices from the master_index_list to extract the 2D fitted data arrays from the H5 file
# # it also build a master list that contains the 2D numpy arrays of interest, rather than just the indices
# def extract_maps(H5s, list_of_lists):
#     maps = []                                                       #initialize master list
#     for H5, channel_indices in zip(H5s, list_of_lists):
#         scan_maps = []                                              #initialize internal (single scan) list
#         XRF_fits = H5['/MAPS/XRF_fits']                             #navigate to structure containing all fitted XRF data
#         for element_index in channel_indices:
#             map_of_interest = XRF_fits[element_index,:,:]           #use element index to extract map of interest
#             scan_maps.append(map_of_interest)                       #build internal list
#         maps.append(scan_maps)                                      #add internal list (i.e. a scan) to master list
#     return maps
#     
# # if i do keep split structure, leave all functions alone and move unto absorption correction
# # if i do not keep split structure:
#     # modify eiDefs.cts_to_elect() to combine XBIC and XBIV maps into one key:value location in master sample dict
#     # modify rumH.find_ele_inh5s() back to combining all the scan ele_indices into one list
# # maintaining separation pro: plotting XBIC vs. XBIV may be easier...
# # maintaining separation con: ele_indices are buried in a complicated structure 
#     # that i'll need to work with when applying absorption correction code...
# # DO I NEED TO SEPARATE XBIC AND XBIV...? could i use if statements in defs_electrical_investigation.py???
# 
# ## list structure comments for apply_ele_iios() in rummage_thru_H5.py##
# # c = [[(ele/iio) for iio,ele in zip(samp['2017_12_ele_iios'],ele_set)] for ele_set in samp['XBIC_ele_maps'][0:3]]
#     # this produces list structure: [ [-,-], [-,-], [-,-] ] , len = 3
#     
# # c2 = [[(ele/iio) for iio,ele in zip(samp['2019_03_ele_iios'], samp['XBIC_ele_maps'][3])]]
#     # this produces list structure: [ [-,-] ] , len = 1
#     # can add to [ [-,-], [-,-], [-,-] ] to make [ [-,-], [-,-], [-,-], [-,-] ]
#     # len = 4
#     
# # c3 = [[(ele/iio) for iio,ele in zip(samp['2019_03_ele_iios'],ele_set)] for ele_set in samp['XBIC_ele_maps'][3]]
#     # this produces list structure: [-,-] , len = 2 as samp['XBIC_ele_maps'][3] is only a single item
#     # if added to [ [-,-], [-,-], [-,-] ] resulting structure would be [ [-,-], [-,-], [-,-], -,- ] , len = 5
# 
# # never use c3; if more than one scan from a separate beamtime is to be processed,
#     # change c2 into the form of c, and be sure to slice list according to corresponding positions in sample dict
# =============================================================================

### NOTES: d_clustering.py ###

import numpy as np
from sklearn.cluster import KMeans
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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
# cluster scatters
plt.figure()
plt.scatter(cu_clust_zero, XBIC_from_clusters_of_cu[0]) 
plt.ylim(0, 4E-8)
plt.xlim(0)
plt.scatter(cu_clust_one, XBIC_from_clusters_of_cu[1]) 
plt.ylim(0, 4E-8)
plt.xlim(0)
plt.scatter(cu_clust_two, XBIC_from_clusters_of_cu[2]) 
plt.ylim(0, 4E-8)
plt.xlim(0)
plt.figure()
plt.scatter(cu_arr, XBIC_arr) 
plt.ylim(0, 4E-8)
plt.xlim(0)
# heatmaps
plt.figure()
ax = sns.heatmap(cu_map, square = True)
ax.invert_yaxis()
plt.figure()
ay = sns.heatmap(A, square = True)
ay.invert_yaxis()
plt.figure()
ay = sns.heatmap(XBIC_map, square = True)
ay.invert_yaxis()

### NOTES: e_statistics.py

# for all three samples, compare the correlation of XBIC to Cd, Te, Zn, and Cu using:
# with standaraizations
# without standardization
# with gaussian applied to Cu
# without gaussian applied to Cu

## comments during development ##
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



# use for standardization 
# compare results of standardized and non-standardized bivariate comparisons
    # note, relative differences within dataset (i.e. the heatmap)
    # do not change after standardization; the quatities change so they may be compared across scales
scaler = skpp.StandardScaler()
reshape_maps = []
std_maps = []
    
for r_m,z in zip(reshape_maps, std_maps):
    plt.figure()
    sns.distplot(r_m)
    sns.distplot(z)

# check standardization features
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.preprocessing as skpp

scaler = skpp.StandardScaler()
cu_stat_map = NBL3_2['elXBIC_corr'][0][0][:,:-2] # practice map, [area 1 : 2019_03][Cu]
stand_cu_stat_map = scaler.fit_transform(cu_stat_map)

map_shape = np.shape(NBL3_2['XBIC_maps'][0][:,:-2])
cu_stat_arr = cu_stat_map.reshape(-1,1)
stand_cu_stat_map_from_arr = scaler.fit_transform(cu_stat_arr)
stand_cu_stat_map_from_arr = stand_cu_stat_map_from_arr.reshape(map_shape)

plt.figure()
sns.heatmap(stand_cu_stat_map, square = True).invert_yaxis()
plt.figure()
sns.heatmap(stand_cu_stat_map_from_arr, square = True).invert_yaxis()


#ex_clust_map = NBL3_2['c_kclust_arrs'][0].labels_.reshape(map_shape)
#sns.heatmap(ex_clust_map, square = True).invert_yaxis()
