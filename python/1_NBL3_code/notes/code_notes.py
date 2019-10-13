### f_corr_pearsons.py
#samp = NBL3_2
#scans = [0,1,2]
#model = 'c_kmodels'
#data_key = 'c_reduced_arrs'
# column index of channel in which you wish to search for max or min medians
#channel_of_interest = 0 
# input 'high' or 'low' to get cluster with highest or lowest values among the clusters
    # not configured to find relative performance of 'medium' clusters
#clusters_of_interest = 'high'
# returns 3D pearson correlation coeff matrix for each scan
    # based off the highest or lowest cluster of the given feature
    # example of process:
        # find cluster with highest xbic value for a given scan (channel_of_interest = 0)
        # calculate correlation matrix between the elements and xbic in that cluster
        # repeat for the length of 'scans'
        
# two compenents to finding cluster data
# example: 'high' xbic cluster
    # compenent 1: the channel you want to 
# focus_channel --> 'high' xbic finds medians of feature, i.e. the column in all_channel_medians
# focus_cluster finds row of cluster...

# clustering performed with reduced_stand arrays, but map retrieved from reduced_normal-unit
    # no error thrown because both arrays are same length
    # but need to check if there's a difference in the mask produced
        # need to check using arrs as reduced cannot be shaped easily
    # RESULT: clustering mask seemed identical when only using a single cluster channel
#--> taking Cu, Cd, Te, and Mo (skipped Zn) in bad geometry scans
    # these beamtimes were run at 12.7 keV, and therefore have more XRF channels
    
#a[:, indices[:,None], indices] # --> in 3d array, get specified row and column indices
    
# find elements and return normalized maps of elements using numpy; note this turned out not to be as flexible
    #as lists, in that the order of the elements must be ordered that same as in the h5 file)


### quick plotting roughness lines ###
# labels for legend are automatically genrated
# =============================================================================
# label_nums = roughnesses * 100
# label_list = []
# for num in label_nums:
#     b = int(num)
#     c = str(b)
#     d = '+/- ' + c + '%'
#     label_list.append(d)
# 
# # note these list lengths must be greater than or equal to the steps in 'roughnesses'
# color_list = ['r', 'b', 'g', 'c', 'm', 'r', 'b', 'g', 'c']
# line_list = ['--', '--','--','--', '--', '-.', '-.', '-.', '-.']
# # plot
# fig, ax = plt.subplots()
# plt.plot(no_rough_in_um, no_rough_iio, 'k', label = 'No roughness')
# for rough_down, rough_up, l, c, lab in zip(ele_rough_iios_down, ele_rough_iios_up, line_list, color_list, label_list):
#     plt.plot(no_rough_in_um, rough_down, linestyle = l, color = c, label = lab)
#     plt.plot(no_rough_in_um, rough_up, linestyle = l, color = c)
# # axis settings
# plt.xlabel('CdTe Thickness (um)', fontsize = 16)
# plt.ylabel('% ' + ele + ' Signal', fontsize = 16)
# ax.tick_params(axis = 'both', labelsize = 14) 
# plt.ylim([0, 1.0])
# plt.grid()
# ax.legend()
# plt.legend(prop={'size': 14})
# plt.show()
# =============================================================================