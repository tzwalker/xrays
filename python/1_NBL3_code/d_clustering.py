from sklearn.cluster import KMeans
import samp_dict_grow
import numpy as np

def find_clusters(samps, N):
    for samp in samps:
        # model needs to be *inside* list comp loop to avoid overwriting previous models
        # make list containing the kmeans model for each scan
        c_scan_models = [KMeans(init='k-means++', n_clusters=N, n_init=10).fit(scan_arrs) for scan_arrs 
                         in samp['c_stand_arrs']]
        v_scan_models = [KMeans(init='k-means++', n_clusters=N, n_init=10).fit(scan_arrs) for scan_arrs 
                         in samp['v_stand_arrs']]
        samp_dict_grow.build_dict(samp, 'c_kmodels', c_scan_models)
        samp_dict_grow.build_dict(samp, 'v_kmodels', v_scan_models)
    return
#find_clusters(samples, 3)

## masking definitions... a little too convoluted and probably not
    # accurate application of clustering
# =============================================================================
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
# 
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
# 
# 
# def get_mask(samples, mask, eles, N):
#     if mask == 'XBIC' or mask == 'XBIV':
#         make_IV_mask_arrays(samples, N)
#         print('this is the electrical  mask loop')
#     else:
#         ele_i = get_index_in_user_ele_list(mask, eles)
#         make_ele_mask_arrays(ele_i, samples, N)
#         print('this is the element mask loop')
#     return
# =============================================================================


