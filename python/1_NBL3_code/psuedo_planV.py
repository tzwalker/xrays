import numpy as np
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.preprocessing as skpp

### NOTES: b_h5_in_elect_scale.py ###
# =============================================================================
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
# #intially for find_ele_in_h5s()
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
# =============================================================================
# ## debugging masking definitions
# def get_index_in_user_ele_list(s, E):               # copied from d_clustering.py
#     for i, e in enumerate(E):                       
#         if s == e[0:2]:                             # test first two characters of ele
#             ele_i = i                               # use index of matched ele in 'elements' list
#     return ele_i
# 
# def get_ele_maps(samp_dict, scan_i, corr_channels, user_channels):
#     ele_maps = []
#     for ch in corr_channels:
#         ele_i = get_index_in_user_ele_list(ch, user_channels) # this index should match the index of the given element in the list 'elements'
#         e_map = samp_dict['elXBIC_corr'][scan_i][ele_i][:,:-2] # remove nan columns to match shape of kclust_arrs
#         ele_maps.append(e_map)
#     return ele_maps
# 
# def apply_mask(samps, channels_to_correlate, channels_inputed_by_user):
#     for samp in samps:
#         correlated_channels_in_ea_scan = []
#         for scan_i, (c_model, v_model) in enumerate(zip(samp['c_kclust_arrs'], samp['v_kclust_arrs'])):
#             stat_XBIC_map = samp['XBIC_maps'][scan_i][:,:-2] # assign matching elect map, remove nan columns
#             to_be_stat_maps = get_ele_maps(samp, scan_i, channels_to_correlate, channels_inputed_by_user)
#             # print(np.shape(stat_XBIC_map))
#             # print(np.shape(to_be_stat_maps[0])) # good, shapes of these arrays match eachother
#             # combine ele and elect lists
#             to_be_stat_maps.insert(0, stat_XBIC_map) # maintain XBIC map in correct index position (0)
#             # list comp for loop to reshape each array into one column
#             stat_arrs = [m.reshape(-1,1) for m in to_be_stat_maps] # these arrays are of appropriate len
#             # build clust dicts from model
#             C_dict_clust_indices_of_clust_ele = {str(clust_num): np.where(c_model.labels_ == clust_num)[0] for clust_num in range(c_model.n_clusters)}
#             # np.take application, (n clusters) * (n_correlate_ele + 1) = length of this list
#             other_map_clusters = [[np.take(other_map, index_list) for index_list in C_dict_clust_indices_of_clust_ele.values()] for other_map in stat_arrs]
#             # structure of above list follows [['XBIC for each cluster'], ['ele1 for each cluster'], ...]
#             correlated_channels_in_ea_scan.append(other_map_clusters)
#         key = 'C_kclust_masked' 
#         samp.setdefault(key, correlated_channels_in_ea_scan)        # make samp dict entry
#         samp['C_kclust_masked'] = correlated_channels_in_ea_scan    # update entry if needed
#     return other_map_clusters
# 
# ## used masking defintions
# def make_IV_mask_arrays(samps, N):
#     for samp in samps:
#         # cluster XBIC scans first
#         c_clust_arrays = []
#         for i, scan in enumerate(samp['XBIC_maps']):
#             stat_c_map = scan[:,:-2]                # remove nans
#             c_arr = stat_c_map.reshape(-1,1)        # array data for proper clustering
#             model = KMeans(init='k-means++', n_clusters=N, n_init=10) # setup model
#             scn_clst_arr = model.fit(c_arr)         # cluster
#             c_clust_arrays.append(scn_clst_arr)     # build mask arrays for each scan
#         key = 'c_kclust_arrs'
#         samp.setdefault(key, c_clust_arrays)        # make arrays
#         samp['c_kclust_arrs'] = c_clust_arrays      # update arrays
#         # cluster XBIV maps
#         v_clust_arrays = []
#         for i, scan in enumerate(samp['XBIV_maps']):
#             stat_v_map = scan[:,:-2]                # remove nans
#             v_arr = stat_v_map.reshape(-1,1)        # array data for proper clustering
#             model = KMeans(init='k-means++', n_clusters=N, n_init=20) # setup model
#             scn_clst_arr = model.fit(v_arr)         # cluster
#             v_clust_arrays.append(scn_clst_arr)     # build mask arrays for each scan
#         key = 'v_kclust_arrs' 
#         samp.setdefault(key, c_clust_arrays)        # make arrays
#         samp['v_kclust_arrs'] = v_clust_arrays      # update arrays
#     return 
# 
# def get_index_in_user_ele_list(s, E):
#     for i, e in enumerate(E):
#         if s == e[0:2]:                             # test first two characters of ele
#             ele_i = i                               # use index of matched ele in 'elements' list
#     return ele_i
# def make_ele_mask_arrays(ele_i, samps, N):
#     for samp in samps:
#         # cluster ele in XBIC maps first
#         c_clust_arrays = []
#         for scan in samp['elXBIC_corr']:
#             ele_map = scan[ele_i]                   # get element map for mask
#             stat_ele_map = ele_map[:,:-2]           # remove nans
#             ele_arr = stat_ele_map.reshape(-1,1)    # array data for proper clustering
#             model = KMeans(init='k-means++', n_clusters=N, n_init=10)
#             scn_clst_arr = model.fit(ele_arr)       # cluster
#             c_clust_arrays.append(scn_clst_arr)
#         key = 'c_kclust_arrs'
#         samp.setdefault(key, c_clust_arrays)        # make arrays
#         samp['c_kclust_arrs'] = c_clust_arrays      # update arrays
#         # cluster ele in XBIV maps
#         v_clust_arrays = []
#         for scan in samp['elXBIV_corr']:
#             ele_map = scan[ele_i]                   # get element map for mask
#             stat_ele_map = ele_map[:,:-2]           # remove nans
#             ele_arr = stat_ele_map.reshape(-1,1)    # array data for proper clustering
#             model = KMeans(init='k-means++', n_clusters=N, n_init=10)
#             scn_clst_arr = model.fit(ele_arr)       # cluster
#             v_clust_arrays.append(scn_clst_arr)
#         key = 'v_kclust_arrs'
#         samp.setdefault(key, v_clust_arrays)
#         samp['v_kclust_arrs'] = v_clust_arrays      # update arrays
#     return 
# def get_mask(samples, mask, eles, N):
#     if mask == 'XBIC' or mask == 'XBIV':
#         make_IV_mask_arrays(samples, N)
#         print('this is the electrical  mask loop')
#     else:
#         ele_i = get_index_in_user_ele_list(mask, eles)
#         make_ele_mask_arrays(ele_i, samples, N)
#         print('this is the element mask loop')
#     return
# # make mask
# cu_map = NBL3_2['eXBIC_corr'][0][0] # practice map, [area 1 : 2019_03][Cu]
# stat_cu_map = cu_map[:,:-2] # eliminate nan
# cu_arr = stat_cu_map.reshape(-1, 1) # array data to cluster each entry individually
# model = KMeans(init='k-means++', n_clusters=3, n_init=10)
# model.fit(cu_arr) # cluster array
# 
# Z = model.labels_
# A = Z.reshape(np.shape(stat_cu_map)) # for cluster map
# # other map to mask to
# XBIC_map = NBL3_2['XBIC_maps'][0]
# stat_XBIC_map = XBIC_map[:,:-2] # eliminate nan columns
# XBIC_arr = stat_XBIC_map.reshape(-1, 1) # array data to identify indices matching with those in cluster labels
# # to find actual values of clusters in other maps
# dict_of_cu_map_cluster_indices = {str(i): np.where(Z == i)[0] for i in range(model.n_clusters)}
# XBIC_from_clusters_of_cu = []
# for index_list in dict_of_cu_map_cluster_indices.values():
#     matched_values_in_XBIC = np.take(XBIC_arr, index_list)
#     XBIC_from_clusters_of_cu.append(matched_values_in_XBIC)
# 
# cu_clust_zero = cu_arr[ClusterIndicesNumpy(0,model.labels_)]
# cu_clust_one = cu_arr[ClusterIndicesNumpy(1,model.labels_)]
# cu_clust_two = cu_arr[ClusterIndicesNumpy(2,model.labels_)]
# 
# ## from home file
# # USER input: enter 'XBIV', 'XBIC', or any element in 'elements_in'
# number_of_clusters = 3
# mask_channel = 'Cu'  # XRF line need not be included, but if it is no error will rise
# d_clustering.get_mask(samples, mask_channel, elements_in, number_of_clusters)
# # USER input:  XRF line need not be included, but if it is no error will rise
#     # note masks are automatically applied to 'XBIC/V' channels
#     # do not include 'XBIC/V' in 'correlate_elements' list
#     # position eles in same manner as in ele_in, for use in stadardize_channels()
#         # should make this more flexible in the future, but for now this is will have to do
# correlate_elements = ['Cu', 'Cd'] 
# # calling the mask on the element used to make the mask 
#     # captures the actaul quantities within each cluster (output of kmeans model is just labels)
# e_statistics.apply_mask(samples, correlate_elements, elements_in)
# =============================================================================


### NOTES: e_statistics.py
# =============================================================================
# # for all three samples, compare the correlation of XBIC to Cd, Te, Zn, and Cu using:
# # with standaraizations
# # without standardization
# # with gaussian applied to Cu
# # without gaussian applied to Cu
# 
# # use for standardization 
# # compare results of standardized and non-standardized bivariate comparisons
#     # note, relative differences within dataset (i.e. the heatmap)
#     # do not change after standardization; the quatities change so they may be compared across scales
# scaler = skpp.StandardScaler()
# reshape_maps = []
# std_maps = []
# for r_m,z in zip(reshape_maps, std_maps):
#     plt.figure()
#     sns.distplot(r_m)
#     sns.distplot(z)
# # check standardization features
# scaler = skpp.StandardScaler()
# cu_stat_map = NBL3_2['elXBIC_corr'][0][0][:,:-2] # practice map, [area 1 : 2019_03][Cu]
# stand_cu_stat_map = scaler.fit_transform(cu_stat_map)
# 
# map_shape = np.shape(NBL3_2['XBIC_maps'][0][:,:-2])
# cu_stat_arr = cu_stat_map.reshape(-1,1)
# stand_cu_stat_map_from_arr = scaler.fit_transform(cu_stat_arr)
# stand_cu_stat_map_from_arr = stand_cu_stat_map_from_arr.reshape(map_shape)
# 
# plt.figure()
# sns.heatmap(stand_cu_stat_map, square = True).invert_yaxis()
# plt.figure()
# sns.heatmap(stand_cu_stat_map_from_arr, square = True).invert_yaxis()
# 
# ## revising array structure
# import numpy as np
# #NBL3_3['c_stat_arrs'][scan][channel]; navigation syntax
# scan264_stats = NBL3_3['c_stat_arrs'][0]
# scan264_stats1 = NBL3_3['c_stat_arrs'][0][1]
# c = np.concatenate((scan264_stats, scan264_stats1), axis=1) # --> works
# 
# arr = np.concatenate(scan264_stats, axis = 1) 
# # --> works better, just make list then concatenate whole list! no list of lists
# # i've been using kmeans incorrectly... 
#     # my samples are captures by the spatial indices, 
#     # however, my features for one sample are much more than one
# test_stat_arr = NBL3_2['c_stat_arrs'][0]
# test_stand_arr = NBL3_2['c_stand_arrs'][0]
# outliers_of_Cu_channel = np.where(test_stand_arr[:,1]>3)
# reduced_stand_arr = test_stand_arr[np.where(test_stand_arr[:,1]<3)] # --> this is the desired output
# =============================================================================


### NOTES: z_plotting.py, spacing axes
# =============================================================================
# ## ticklabel formating
# # how to figure out what the proper indeices to plot are...?
# # the integer in xticklabels represents every 'n' index to be plotted
#     # e.g. xtixklabels = 50 --> 0, 50, 150 all plotted
#     # the list x_real has actual numbers that map to the indices... but how does that help me...   
#     # could use mod?
# # find where first whole number is in x_real!
#   # get index of this number... 
#   # when would whole number not exist...? 
#       # when the width of the axis is not evenly split by the resolution
#       # e.g. np.linspace(0,16,38)
#   # HOWEVER: the first and last number, as they are int, are guaranteed
#       # to be whole, therefore, the above approach will always find a whole number index
#       # and will plot either the bounds of the axes, or every whole number that exists in the linear space!
# 
# practice_axis_list = list(practice_axis)
# 
# max(practice_axis_list)
# Out[152]: 1484.7
# 
# min(practice_axis_list)
# Out[153]: 1469.7
# 
# max(practice_axis_list) - min(practice_axis_list)
# Out[154]: 15.0
# 
# np.linspace(0, max(practice_axis_list) - min(practice_axis_list),5)
# Out[155]: array([ 0.  ,  3.75,  7.5 , 11.25, 15.  ])
# 
# np.linspace(0, max(practice_axis_list) - min(practice_axis_list), len(practice_axis_list))
# Out[156]: 
# array([ 0.  ,  0.15,  0.3 ,  0.45,  0.6 ,  0.75,  0.9 ,  1.05,  1.2 ,
#         1.35,  1.5 ,  1.65,  1.8 ,  1.95,  2.1 ,  2.25,  2.4 ,  2.55,
#         2.7 ,  2.85,  3.  ,  3.15,  3.3 ,  3.45,  3.6 ,  3.75,  3.9 ,
#         4.05,  4.2 ,  4.35,  4.5 ,  4.65,  4.8 ,  4.95,  5.1 ,  5.25,
#         5.4 ,  5.55,  5.7 ,  5.85,  6.  ,  6.15,  6.3 ,  6.45,  6.6 ,
#         6.75,  6.9 ,  7.05,  7.2 ,  7.35,  7.5 ,  7.65,  7.8 ,  7.95,
#         8.1 ,  8.25,  8.4 ,  8.55,  8.7 ,  8.85,  9.  ,  9.15,  9.3 ,
#         9.45,  9.6 ,  9.75,  9.9 , 10.05, 10.2 , 10.35, 10.5 , 10.65,
#        10.8 , 10.95, 11.1 , 11.25, 11.4 , 11.55, 11.7 , 11.85, 12.  ,
#        12.15, 12.3 , 12.45, 12.6 , 12.75, 12.9 , 13.05, 13.2 , 13.35,
#        13.5 , 13.65, 13.8 , 13.95, 14.1 , 14.25, 14.4 , 14.55, 14.7 ,
#        14.85, 15.  ])
# 
# # stack overflow attempts
# x = np.linspace(0, 15, 151)
# y = np.linspace(0, 15, 151)
# 
# my_data = NBL3_2['XBIC_maps'][3]
# df_map = pd.DataFrame(my_data, index = y, columns = x) 
# plt.figure()
# ax = sns.heatmap(df_map, square = True, xticklabels  = 20, yticklabels = 20)
# ax.invert_yaxis()
# 
# fmtr = tkr.StrMethodFormatter('{x:.0f}')
# ax.xaxis.set_major_formatter(fmtr)
# fmtr = tkr.StrMethodFormatter("{x:.0f}")
# locator = tkr.MultipleLocator(50)
# fstrform = tkr.FormatStrFormatter('%.0f')
# 
# #plt.gca().xaxis.set_major_formatter(fmtr)
# plt.gca().xaxis.set_major_locator(locator)
# plt.gca().xaxis.set_major_formatter(fstrform)
# plt.show()
# 
# ## for 3D plots, be sure to change matplotlib backend from 'inline' to 'qt'
# ax = Axes3D(fig, rect=[0, 0, .95, 1]) 
# ax.w_xaxis.set_ticklabels([])
# ax.w_yaxis.set_ticklabels([])
# ax.w_zaxis.set_ticklabels([])
# ax.set_xlabel('Cu')
# ax.set_ylabel('XBIC')
# ax.set_zlabel('Cd')
# # Set rotation angle to 30 degrees
# ax.view_init(azim=0)
# for angle in range(0, 360):
#     ax.view_init(60, angle)
#     plt.draw()
#     plt.show()
#     plt.pause(0.001)
#     
# ## masked scatterplots 
# #models_arrs = NBL3_3['c_kclust_arrs']#[scan][model]
# #no_nan_arrs = NBL3_3['c_stat_arrs']#[scan][channel]
# masked = NBL3_2['C_kclust_masked']#[scan][channel][cluster]
# #k_stats_stand = NBL3_3['c_kclust_arrs_stand']#[scan][channel][cluster]
# 
# xbicMap0_cl0 = masked[0][2][0]
# xbicMap0_cl1 = masked[0][2][1]
# xbicMap0_cl2 = masked[0][2][2]
# combined_arr_max = np.array([max(xbicMap0_cl0), max(xbicMap0_cl1), max(xbicMap0_cl2)])
# combined_arr_min = np.array([min(xbicMap0_cl0), min(xbicMap0_cl1), min(xbicMap0_cl2)])
# ymax = np.max(combined_arr_max) *1.1
# ymin = np.min(combined_arr_min) *0.9
# 
# cuMap0_cl0 = masked[0][1][0]
# cuMap0_cl1 = masked[0][1][1]
# cuMap0_cl2 = masked[0][1][2]
# 
# plt.figure()
# sns.jointplot(cuMap0_cl0, xbicMap0_cl0, kind = 'hex')#, x_bins = 3, x_ci = 'sd')
# sns.jointplot(cuMap0_cl1, xbicMap0_cl1, kind = 'hex')#, x_bins = 4, x_ci = 'sd')
# sns.jointplot(cuMap0_cl2, xbicMap0_cl2, kind = 'hex')#, x_bins = 4, ci = None)
# 
# sns.distplot(cuMap0_cl0)
# #plt.ylim(ymin, ymax)
# #plt.xlim(0)
# =============================================================================

### NOTES: z_img_processing.py
# =============================================================================
# 
#     # pix by pix product
#     product = cu_gradient * zn_gradient
#     # geometric mean of gradients
#     gmean = np.sqrt(product)
# =============================================================================
# =============================================================================
# fig, (ax0,ax1) = plt.subplots(nrows=1,ncols=2)
# plt.tight_layout()
# sns.heatmap(samp_maps[0],square=True, ax=ax0, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
# sns.heatmap(grad_matrix, square=True, ax=ax1,xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
# sns.heatmap(grad_matrix[1], square=True, ax=ax2,xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
# 
# for index, Map in enumerate(samp_maps):
#     fig, (ax0, ax1) = plt.subplots(nrows=1,ncols=2)
#     gradient_map = calc_grad_map(Map)
#     sns.heatmap(Map, square=True, ax=ax0, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
#     sns.heatmap(gradient_map, square=True, ax=ax1, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
# =============================================================================

# =============================================================================
# # gaussian filter of (shaped) standardized data
# cu_stand = cu_stand.reshape(np.shape(gauss_map))
# gauss_of_cu_stand = gaussian_filter(cu_stand, sigma=2)
# zn_stand = zn_stand.reshape(np.shape(gauss_map))
# gauss_of_zn_stand = gaussian_filter(zn_stand, sigma=2)
# =============================================================================

# =============================================================================
# # threshold percentile of gradient map
# cu_gradient_75quart_thres = np.percentile(cu_gradient_no_edge, percentile)
# zn_gradient_75quart_thres = np.percentile(zn_gradient_no_edge, percentile)
# # find pixels in gradient map within a given percentile
# cu_mask = np.where(cu_gradient >= cu_gradient_75quart_thres, 1,0) # retains shape
# zn_mask = np.where(zn_gradient >= zn_gradient_75quart_thres, 1,0)
# # find where gradient maps mismatch --> quantifies the error in saying g.bs are where the gradients lie??
# a_mismatched_map = np.where(cu_mask == zn_mask, 1, 0)
# # parameter to minimize mismatch
# mismatch = a_mismatched_map.sum()
# print(percentile, mismatch, round(mismatch/init_mismatch, 3))
# 
# fig, (ax0, ax1, ax2) = plt.subplots(nrows=1,ncols=3)
# plt.tight_layout()
# ax0.imshow(cu_mask, origin='lower', cmap='Greys_r')
# ax1.imshow(zn_mask, origin='lower', cmap='Greys_r')
# ax2.imshow(a_mismatched_map, origin='lower', cmap='Greys_r')
# #if mismatch < init_mismatch:
#     #best_percentile = percentile
# # for each pixel in the masks, if values match, record pixel coordinates for indexing into real data arrays, plot on scatter
# calculatign Sobel gradient; identifying edges of images
#    # works well for XBIC, not so well for Cu and Cd, which contain noise (see consolidated notes)
#    # next step: apply gaussian filter to XRF, then find edges (or alter Sobel kernels, ,if possible)
#
#      # --> matches pixels in the gradient maps that are above a certaiin percentile... make bulk stats of number of matches among the various areas scanned
# =============================================================================


### stack overflow question, list compmrehension sorting...
# =============================================================================
# decoded_chans1 = ['A', 'B', 'C', 'D', 'H']
# user_chans1 = ['H', 'B', 'C']
# adj_index_list = [i for i,decoded_ch in enumerate(decoded_chans1) 
#                   for user_ch in user_chans1 
#                   if user_ch == decoded_ch]
# 
# adj_index_list = []
# for user_ch in user_chans1:
#     for i, decoded_ch in enumerate(decoded_chans1):
#         if user_ch == decoded_ch:
#             adj_index_list.append(i)
# =============================================================================
