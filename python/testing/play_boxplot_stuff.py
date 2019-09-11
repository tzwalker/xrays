# -*- coding: utf-8 -*-
"""
Trumann
Wed Sep 11 11:46:27 2019
"""

# plot a bunch of boxplots...
# =============================================================================
# def plot_more_boxes(model, key, scans):
#     for samp, samp_name in zip(samples, samp_names):
#         for scan in scans:
#             clust_labs = samp[model][scan].labels_
#             data = [samp[key][scan][:,i] for i, ele in enumerate(samp[key][scan].T)] # this format is necessary for boxplots
#             plot_clust_boxes(clusts, clust_labs, data, scan, samp_name)
#     return
# 
# def plot_clust_boxes(clust_nums, clust_labs, data, scan, sam):
#     fig, axs = plt.subplots(len(data),1)
#     plt.tight_layout()
#     clusters_for_each_channel = []
#     for channel in data: # data is a list; each item is a column from the original numpy arr
#         cluster_list = [channel[np.where(clust_labs == clust)[0]] for clust in clust_nums]
#         clusters_for_each_channel.append(cluster_list)
#     for i, clusters in enumerate(clusters_for_each_channel):
#         bp_dict = axs[i].boxplot(clusters, showfliers=False)
#         for line in bp_dict['medians']:
#             med = line.get_ydata()                  # get median value array
#             xpoint, ypoint = line.get_xydata()[1]   # get plot coordinates of median
#             # annotate this position with median as string
#             axs[i].annotate(xy=(xpoint,ypoint), 
#                s=' ' + "{:.4g}".format(med[0]), 
#                horizontalalignment='left') # add text with formatting
#         axs[i].title.set_text(boxplot_names[i])
#     #plt.savefig(r'C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190904 clustering and boxplots\noflier_{sample}_area{sc}'.format(sample=sam, sc=scan))
#     return
# #samp_names = ['NBL3_2', 'NBL3_3', 'TS58A']
# #boxplot_names = ['reduced xbic', 'reduced cu','reduced cd','reduced te']
# #plot_more_boxes(model, data_key, scans)
# def clust_scatter_matrix(cluster_data, elements):
#     cols = elements.insert(0, 'xbic')
#     df = pd.DataFrame(cluster_data[0], columns = cols) # make for loop to go over each cluster in cluster_data
#     pd.plotting.scatter_matrix(df, alpha = 0.2)
#     return
# def return_cluster_unique_lists(cluster_data):
#     
#     medians = [np.median(cluster, axis=0) for cluster in cluster_data]
#     arr_medians = np.array(medians).T # for convenience of max/min identification between clusters
#     
#     indices_of_median_maxes = []
#     indices_of_median_mins = []
#     for channel in medians:
#         index_of_median_maxes = channel.index(max(channel)) #--> really "cluster containing median max"
#         index_of_median_mins = channel.index(min(channel))  #--> really "cluster containing median min"
#         indices_of_median_maxes.append(index_of_median_maxes)
#         indices_of_median_mins.append(index_of_median_mins)
#     
#     # these lists trade off, producing a unique identifier for a given combo in the max XBIC cluster
#     indices_test_cluster0 = [i for i, cluster in enumerate(indices_of_median_maxes) if cluster == 0]
#     indices_test_cluster1 = [i for i, cluster in enumerate(indices_of_median_maxes) if cluster == 1]
#     indices_test_cluster2 = [i for i, cluster in enumerate(indices_of_median_maxes) if cluster == 2]
#     return 
# =============================================================================

### basic boxplots of raw data 
# =============================================================================
# cu_maps = [samp['elXBIC_corr'][scan][0][:,:-2] for samp in samples]
# xbic_maps = [samp['XBIC_maps'][scan][:,:-2] for samp in samples]
# 
# cu_data = [samp['elXBIC_corr'][scan][0][:,:-2].ravel() for samp in samples]
# xbic_data = [samp['XBIC_maps'][scan][:,:-2].ravel() for samp in samples]
#     
# x_boxlabs = [samp['Name'] for samp in samples]
# 
# fig, axs = plt.subplots(1,2)
# plt.tight_layout()
# axs[0].imshow(cu_maps[2], origin='lower')
# axs[1].imshow(xbic_maps[2], origin='lower')
# 
# plt.figure()
# plt.boxplot(cu_data)
# plt.xticks([1, 2, 3], x_boxlabs)
# plt.suptitle('Thickness corrected Cu')
# plt.figure()
# plt.boxplot(xbic_data)
# plt.xticks([1, 2, 3], x_boxlabs)
# plt.suptitle('XBIC')
# =============================================================================