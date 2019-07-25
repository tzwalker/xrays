# scan indices:
    # 0-2 --> 2019_03
    # 3 --> 2017_12
# element indices:
    # 0 --> Cu
    # 1 --> Cd
    # will add others if needed

from sklearn.cluster import KMeans
import numpy as np
  
cu_map = NBL3_3['XBIC_ele_maps'][0][0] # practice map
X = cu_map[:,:-2] # eliminate nan
Y = X.reshape(-1, 1) # array data to cluster each entry individually


model = KMeans(init='k-means++', n_clusters=3, n_init=10).fit(Y) # cluster array

Z = model.labels_
A = Z.reshape(101,99)

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure()
ax = sns.heatmap(cu_map, square = True)
ax.invert_yaxis()
plt.figure()
ay = sns.heatmap(A, square = True)
ay.invert_yaxis()
# =============================================================================
# #{i: np.where(k_means.labels_ == i)[0] for i in range(k_means.n_clusters)}
# 
# k_means_labels = k_means.labels_
# k_means_cluster_centers = k_means.cluster_centers_
# k_means_labels_unique = np.unique(k_means_labels)
# 
# ##############################################################################
# # Plot result
# 
# colors = ['#4EACC5', '#FF9C34', '#4E9A06']
# plt.figure()
# #plt.hold(True)
# for k, col in zip(range(3), colors):
#     my_members = k_means_labels == k
#     cluster_center = k_means_cluster_centers[k]
#     plt.plot(X[my_members, 0], X[my_members, 1], 'w',
#             markerfacecolor=col, marker='.')
#     plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
#             markeredgecolor='k', markersize=6)
# plt.title('KMeans')    
# 
# plt.show()
# =============================================================================
