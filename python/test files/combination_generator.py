# -*- coding: utf-8 -*-
"""
Trumann
Wed Sep 11 11:47:08 2019
"""

# other heatmap option...
# =============================================================================
# from z_plot_supplement import heatmap, annotate_heatmap
# 
# fig, ax = plt.subplots()
# im, cbar = heatmap(avg_corr, cols, cols, ax=ax,
#                    cmap="coolwarm", cbarlabel="Pearson Correlation Coeff.")
# texts = annotate_heatmap(im, valfmt="{x:.3f}")
# fig.tight_layout()
# plt.show()
# =============================================================================

# make combination counter
# =============================================================================
# z_cluster_data = get_cluster_data(samp, scans, model, data_key, cluster_number)
# z_medians = [np.median(cluster, axis=0) for cluster in z_cluster_data]
# z_medians_arr = np.array(z_medians)
# z_cluster_index_where_max_med_exists = np.argmax(z_medians_arr, axis=0)
# z_cluster_index_where_min_med_exists = np.argmin(z_medians_arr, axis=0)
# =============================================================================

# combination psuedo-generator
# =============================================================================
# test_combo_labels = list(range(len(elements)+1)) #--> change these to the indices 0,1,2,3 ; or however many channels you have
# from itertools import chain, combinations # use this to generate the possible combinations
# def all_subsets(ss):
#     combos = [combinations(ss, x) for x in range(0,len(ss)+1)]
#     return chain(*combos)
# subsets = all_subsets(test_combo_labels)
# print(subsets)
# =============================================================================