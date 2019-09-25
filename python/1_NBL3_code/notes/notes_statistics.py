### NOTES: e_statistics.py
# for all three samples, compare the correlation of XBIC to Cd, Te, Zn, and Cu using:
# with standaraizations
# without standardization
# with gaussian applied to Cu
# without gaussian applied to Cu

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

## revising array structure
import numpy as np
#NBL3_3['c_stat_arrs'][scan][channel]; navigation syntax
scan264_stats = NBL3_3['c_stat_arrs'][0]
scan264_stats1 = NBL3_3['c_stat_arrs'][0][1]
c = np.concatenate((scan264_stats, scan264_stats1), axis=1) # --> works

arr = np.concatenate(scan264_stats, axis = 1) 
# --> works better, just make list then concatenate whole list! no list of lists
# i've been using kmeans incorrectly... 
    # my samples are captures by the spatial indices, 
    # however, my features for one sample are much more than one
test_stat_arr = NBL3_2['c_stat_arrs'][0]
test_stand_arr = NBL3_2['c_stand_arrs'][0]
outliers_of_Cu_channel = np.where(test_stand_arr[:,1]>3)
reduced_stand_arr = test_stand_arr[np.where(test_stand_arr[:,1]<3)] # --> this is the desired output
# 20190909: critical dependency: the reduced arrays created by e_statistics.reduce_arrs 
   # vary in length depending on how many elemental channels are included
       # therefore, the array that ends up being fit using kmeans is dependent
   # on the size of the reduced array; this dependency is not acceptable error corrected
