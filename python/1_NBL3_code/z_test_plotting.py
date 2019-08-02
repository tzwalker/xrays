import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import numpy as np

scan_i = 0      # --> index of scan 
x_variable = 1 # --> 0:XBIC 1:Cu 2:Cd
y_variable = 0 # --> 0:XBIC 1:Cu 2:Cd
samp = NBL3_2
#from os import path
#outpath = r"C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190801 cluster investigation"

test_models = samp['c_kmodels'][scan_i] # --> XBIC, Cu, and Cd arrays for scan422
labels = test_models.labels_
test_data = samp['c_stand_arrs'][scan_i]
x = test_data[:, x_variable]
y = test_data[:, y_variable]

# =============================================================================
# fig = plt.figure()
# hexbin = sns.jointplot(x, y, kind ='hex', color = 'grey')
# plt.title(samp['Name'] + ' ' + str(samp['XBIC_scans'][scan_i]))
# #filename = 'hex ' + samp['Name'] + ' ' + str(samp['XBIC_scans'][scan_i]) + '.png'
# #hexbin.savefig(outpath + filename)
# =============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Scatter and Map '+ samp['Name'] + ' ' + str(samp['XBIC_scans'][scan_i]))

ax1.scatter(x, y, c = labels)
#plt.title()
#filename = 'scat ' + samp['Name'] + ' ' + str(samp['XBIC_scans'][scan_i]) + '.png'
#fig.savefig(path.join(outpath, filename))

ax2.imshow(samp['elXBIC_corr'][scan_i][0])
#plt.title(samp['Name'] + ' ' + str(samp['XBIC_scans'][scan_i]))
#filename = 'heat ' + samp['Name'] + ' ' + str(samp['XBIC_scans'][scan_i]) + '.png'
#fig.savefig(path.join(outpath, filename))

# stackoverflow attempts
# =============================================================================
# x = np.linspace(0, 15, 151)
# y = np.linspace(0, 15, 151)
# 
# my_data = NBL3_2['XBIC_maps'][3]
# df_map = pd.DataFrame(my_data, index = y, columns = x) 
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

# smasking scatterplots #

# =============================================================================
# #models_arrs = NBL3_3['c_kclust_arrs']#[scan][model]
# #no_nan_arrs = NBL3_3['c_stat_arrs']#[scan][channel]
# masked = NBL3_2['C_kclust_masked']#[scan][channel][cluster]
# #k_stats_stand = NBL3_3['c_kclust_arrs_stand']#[scan][channel][cluster]
# 
# xbicMap0_cl0 = masked[0][2][0]
# xbicMap0_cl1 = masked[0][2][1]
# xbicMap0_cl2 = masked[0][2][2]
# combined_arr_max = np.array([max(xbicMap0_cl0), max(xbicMap0_cl1), max(xbicMap0_cl2)])
# combined_arr_min = np.array([min(xbicMap0_cl0), min(xbicMap0_cl1), min(xbicMap0_cl2)])
# ymax = np.max(combined_arr_max) *1.1
# ymin = np.min(combined_arr_min) *0.9
# 
# cuMap0_cl0 = masked[0][1][0]
# cuMap0_cl1 = masked[0][1][1]
# cuMap0_cl2 = masked[0][1][2]
# 
# plt.figure()
# sns.jointplot(cuMap0_cl0, xbicMap0_cl0, kind = 'hex')#, x_bins = 3, x_ci = 'sd')
# sns.jointplot(cuMap0_cl1, xbicMap0_cl1, kind = 'hex')#, x_bins = 4, x_ci = 'sd')
# sns.jointplot(cuMap0_cl2, xbicMap0_cl2, kind = 'hex')#, x_bins = 4, ci = None)
# 
# sns.distplot(cuMap0_cl0)
# #plt.ylim(ymin, ymax)
# #plt.xlim(0)
# =============================================================================
