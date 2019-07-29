

# scan indices:
    # 0-2 --> 2019_03
    # 3 --> 2017_12
# element indices:
    # 0 --> Cu
    # 1 --> Cd
    # will add others if needed
import numpy as np
from sklearn.cluster import KMeans
import sklearn.preprocessing as skpp
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


reshape_maps = []

cu_map = NBL3_2['eXBIC_corr'][0][0] # practice map, [area 1 : 2019_03][Cu]
stat_cu_map = cu_map[:,:-2] # eliminate nan


cu_arr = stat_cu_map.reshape(-1, 1) # array data to cluster each entry individually
# for all three samples, compare the correlation of XBIC to Cd, Te, Zn, and Cu using:
# with standaraizations
# without standardization
# with gaussian applied to Cu
# without gaussian applied to Cu

model = KMeans(init='k-means++', n_clusters=3, n_init=10)
model.fit(cu_arr) # cluster array

Z = model.labels_
A = Z.reshape(np.shape(stat_cu_map)) # for cluster map

dict_of_cu_map_cluster_indices = {str(i): np.where(Z == i)[0] for i in range(model.n_clusters)}

XBIC_map = NBL3_2['XBIC_maps'][0]
stat_XBIC_map = XBIC_map[:,:-2] # eliminate nan
XBIC_arr = stat_XBIC_map.reshape(-1, 1) # array data to identify indices matching with those in cluster labels

XBIC_from_clusters_of_cu = []
for index_list in dict_of_cu_map_cluster_indices.values():
    matched_values_in_XBIC = np.take(XBIC_arr, index_list)
    XBIC_from_clusters_of_cu.append(matched_values_in_XBIC)


def ClusterIndicesNumpy(clustNum, labels_array): #numpy 
    return np.where(labels_array == clustNum)[0]

cu_clust_zero = cu_arr[ClusterIndicesNumpy(0,model.labels_)]
cu_clust_one = cu_arr[ClusterIndicesNumpy(1,model.labels_)]
cu_clust_two = cu_arr[ClusterIndicesNumpy(2,model.labels_)]

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

### heatmaps
plt.figure()
ax = sns.heatmap(cu_map, square = True)
ax.invert_yaxis()
plt.figure()
ay = sns.heatmap(A, square = True)
ay.invert_yaxis()
plt.figure()
ay = sns.heatmap(XBIC_map, square = True)
ay.invert_yaxis()


# use for standardization 
# compare results of standardized and non-standardized bivariate comparisons
    # note, relative differences within dataset (i.e. the heatmap)
    # do not change after standardization; the quatities change so they may be compared across scales
scaler = skpp.StandardScaler()
std_maps = []
# =============================================================================
#     
#     Z = scaler.fit_transform(Y)
#     std_maps.append(Z)
#     standardized_map = Z.reshape(np.shape(X))
#     
#     plt.figure()
#     sns.heatmap(cu_map, square = True)
#     plt.figure()
#     sns.heatmap(standardized_map, square = True)
#     
# for r_m,z in zip(reshape_maps, std_maps):
#     plt.figure()
#     sns.distplot(r_m)
#     sns.distplot(z)
# =============================================================================

import numpy as np
map_shape = np.shape(NBL3_2['XBIC_maps'][0][:,:-2])
np.shape(NBL3_2['c_kclust_arrs'][0])

np.shape(NBL3_2['c_kclust_arrs'][0].labels_)

ex_clust_map = NBL3_2['c_kclust_arrs'][0].labels_.reshape(map_shape)
sns.heatmap(ex_clust_map, square = True).invert_yaxis()