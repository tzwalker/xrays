
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

# =============================================================================
# x = np.linspace(0, 15, 151)
# y = np.linspace(0, 15, 151)
# 
# heatmap = NBL3_2['XBIC_maps'][3]
# df_map = pd.DataFrame(heatmap, index = y, columns = x) 
# plt.figure()
# ax = sns.heatmap(df_map, square = True, xticklabels  = 20, yticklabels = 20)
# ax.invert_yaxis()
# 
# # =============================================================================
# # fmtr = tkr.StrMethodFormatter('{x:.0f}')
# # ax.xaxis.set_major_formatter(fmtr)
# # =============================================================================
# 
# 
# fmtr = tkr.StrMethodFormatter("{x:.0f}")
# locator = tkr.MultipleLocator(50)
# fstrform = tkr.FormatStrFormatter('%.0f')
# 
# #plt.gca().xaxis.set_major_formatter(fmtr)
# plt.gca().xaxis.set_major_locator(locator)
# plt.gca().xaxis.set_major_formatter(fstrform)
# plt.show()
# =============================================================================

# scatter plots #

#models_arrs = NBL3_3['c_kclust_arrs']#[scan][model]
#no_nan_arrs = NBL3_3['c_stat_arrs']#[scan][channel]
masked = NBL3_2['C_kclust_masked']#[scan][channel][cluster]
#k_stats_stand = NBL3_3['c_kclust_arrs_stand']#[scan][channel][cluster]

xbicMap0_cl0 = masked[0][2][0]
xbicMap0_cl1 = masked[0][2][1]
xbicMap0_cl2 = masked[0][2][2]
combined_arr_max = np.array([max(xbicMap0_cl0), max(xbicMap0_cl1), max(xbicMap0_cl2)])
combined_arr_min = np.array([min(xbicMap0_cl0), min(xbicMap0_cl1), min(xbicMap0_cl2)])
ymax = np.max(combined_arr_max) *1.1
ymin = np.min(combined_arr_min) *0.9

cuMap0_cl0 = masked[0][1][0]
cuMap0_cl1 = masked[0][1][1]
cuMap0_cl2 = masked[0][1][2]

plt.figure()
sns.jointplot(cuMap0_cl0, xbicMap0_cl0, kind = 'hex')#, x_bins = 3, x_ci = 'sd')
sns.jointplot(cuMap0_cl1, xbicMap0_cl1, kind = 'hex')#, x_bins = 4, x_ci = 'sd')
sns.jointplot(cuMap0_cl2, xbicMap0_cl2, kind = 'hex')#, x_bins = 4, ci = None)

sns.distplot(cuMap0_cl0)
#plt.ylim(ymin, ymax)
#plt.xlim(0)