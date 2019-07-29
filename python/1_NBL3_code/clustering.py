from sklearn.cluster import KMeans

def get_index_in_user_ele_list(s, E):
    for i, e in enumerate(E):
        if s == e[0:2]:
            ele_i = i
    return ele_i

def make_ele_mask_arrays(e_i, samps, N):
    for samp in samps:
        # cluster element of interest in XBIC maps
        c_clust_arrays = []
        for scan in samp['eXBIC_corr']:
            ele_map = scan[e_i]   # get element map for mask
            stat_ele_map = ele_map[:,:-2]      # remove nans
            ele_arr = stat_ele_map.reshape(-1,1)     # array data for proper clustering
            model = KMeans(init='k-means++', n_clusters=N, n_init=10)
            scn_clst_arr = model.fit(ele_arr)    # cluster
            c_clust_arrays.append(scn_clst_arr)
        key = 'c_kclust_arrs'
        samp.setdefault(key, c_clust_arrays)
        # do the same for voltage maps
        v_clust_arrays = []
        for scan in samp['eXBIV_corr']:
            ele_map = scan[e_i]   # get element map for mask
            stat_ele_map = ele_map[:,:-2]      # remove nans
            ele_arr = stat_ele_map.reshape(-1,1)     # array data for proper clustering
            model = KMeans(init='k-means++', n_clusters=N, n_init=10)
            scn_clst_arr = model.fit(ele_arr)    # cluster
            v_clust_arrays.append(scn_clst_arr)
        key = 'v_kclust_arrs'
        samp.setdefault(key, v_clust_arrays)
    return 

def make_IV_mask_arrays(samps, N):
    for samp in samps:
        # cluster element of interest in XBIC maps
        c_clust_arrays = []
        for i, scan in enumerate(samp['XBIC_maps']):
            stat_c_map = scan[:,:-2]      # remove nans
            c_arr = stat_c_map.reshape(-1,1)     # array data for proper clustering
            model = KMeans(init='k-means++', n_clusters=N, n_init=10)
            scn_clst_arr = model.fit(c_arr)    # cluster
            c_clust_arrays.append(scn_clst_arr)
        key = 'c_kclust_arrs'
        samp.setdefault(key, c_clust_arrays)
        # do the same for voltage maps
        v_clust_arrays = []
        for i, scan in enumerate(samp['XBIV_maps']):
            stat_v_map = scan[:,:-2]      # remove nans
            v_arr = stat_v_map.reshape(-1,1)     # array data for proper clustering
            model = KMeans(init='k-means++', n_clusters=N, n_init=10)
            scn_clst_arr = model.fit(v_arr)    # cluster
            v_clust_arrays.append(scn_clst_arr)
        key = 'v_kclust_arrs'
        samp.setdefault(key, c_clust_arrays)
    return 

def get_mask(samples, channel, eles, N):
    if channel == 'XBIC' or channel == 'XBIV':
        make_IV_mask_arrays(samples, N)
        print('this is the electrical  mask loop')
        
    else:
        ele_i = get_index_in_user_ele_list(channel, eles)
        make_ele_mask_arrays(ele_i, samples, N)
        
        print('this is the element mask loop')

    return


