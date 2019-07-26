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

dict_of_cu_map_cluster_indices = {i: np.where(model.labels_ == i)[0] for i in range(model.n_clusters)}

