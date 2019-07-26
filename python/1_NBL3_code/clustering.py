

# scan indices:
    # 0-2 --> 2019_03
    # 3 --> 2017_12
# element indices:
    # 0 --> Cu
    # 1 --> Cd
    # will add others if needed

from sklearn.cluster import KMeans
import sklearn.preprocessing as skpp
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

scaler = skpp.StandardScaler()
reshape_maps = []
std_maps = []

cu_map = NBL3_2['eXBIC_corr'][0][0] # practice map, [area 1 : 2019_03][Cu]
X = cu_map[:,:-2] # eliminate nan


Y = X.reshape(-1, 1) # array data to cluster each entry individually
reshape_maps.append(Y)
# compare the correlation of XBIC to Cd, Te, Zn, and Cu using:
# cluster/mask/correlate WITHOUT gaussian filter applied to XRF channels
# cluster/mask/correlate WITH gaussian filter applied to XRF channels

model = KMeans(init='k-means++', n_clusters=3, n_init=10)
model.fit(Y) # cluster array

Z = model.labels_
A = Z.reshape(np.shape(X)) # for cluster map

dict_of_cu_map_cluster_indices = {str(i): np.where(Z == i)[0] for i in range(model.n_clusters)}

XBIC_map = NBL3_2['XBIC_maps'][0]
X2 = XBIC_map[:,:-2] # eliminate nan
Y2 = X2.reshape(-1, 1) # array data to identify indices matching with those in cluster labels

XBIC_from_clusters_of_cu = []
for index_list in dict_of_cu_map_cluster_indices.values():
    matched_values_in_XBIC = np.take(Y2, index_list)
    XBIC_from_clusters_of_cu.append(matched_values_in_XBIC)


def ClusterIndicesNumpy(clustNum, labels_array): #numpy 
    return np.where(labels_array == clustNum)[0]

cu_clust_zero = Y[ClusterIndicesNumpy(0,model.labels_)]
cu_clust_one = Y[ClusterIndicesNumpy(1,model.labels_)]
cu_clust_two = Y[ClusterIndicesNumpy(2,model.labels_)]

plt.figure()
plt.scatter(cu_clust_zero, XBIC_from_clusters_of_cu[0]) 
plt.ylim(0, 4E-8)
plt.xlim(0)

plt.figure()
plt.scatter(cu_clust_one, XBIC_from_clusters_of_cu[1]) 
plt.ylim(0, 4E-8)
plt.xlim(0)

plt.figure()
plt.scatter(cu_clust_two, XBIC_from_clusters_of_cu[2]) 
plt.ylim(0, 4E-8)
plt.xlim(0)

# =============================================================================
# for items in dict_of_cu_map_cluster_indices.values():
#     print(items)
#     
# [   6    7    9 ... 9981 9984 9989]
# [   0    2   13 ... 9995 9996 9997]
# [   1    3    4 ... 9992 9993 9998]
# =============================================================================

plt.figure()
ax = sns.heatmap(cu_map, square = True)
ax.invert_yaxis()
plt.figure()
#ay = sns.distplot(A, square = True)
#ay.invert_yaxis()



# USE #
# =============================================================================
# import numpy as np
# def get_index_in_user_ele_list(s, E):
#     for i, e in enumerate(E):
#         if s == e[0:2]:
#             ele_i = i
#     return ele_i
# 
# def make_ele_arrays(e_i, samps):
#     for samp in samps:
#         clust_arrays = []
#         for scan in samp['eXBIC_corr']:
#             ele_map = scan[ele_i]
#             X = ele_map[:,:-2]
#             Y = X.reshape(-1,1)
#             model = KMeans(init='k-means++', n_clusters=3, n_init=10)
#             array = model.fit(Y)
#             
#             
#     return list_of_clustered_arrays
# 
# def get_ele_mask(samples, e, eles):
#     ele_i = get_index_in_user_ele_list(e, eles)
#     make_ele_arrays(ele_i, samples)
#     
#     return
# =============================================================================

# standardize all data for bivariate comparisons


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


