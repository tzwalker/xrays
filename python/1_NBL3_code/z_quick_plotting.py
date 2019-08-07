import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



def plot_nice_stats(samp, scan, x, y, axis_label_sizes):
    x_data = samp['c_redStand_arrs'][scan][:,x_channel]
    y_data = samp['c_redStand_arrs'][scan][:,y_channel]
    data_models = samp['c_kmodels'][scan] # --> XBIC, Cu, and Cd arrays for scan422
    labels = data_models.labels_
    
    fig, ax0 = plt.subplots()
    ax0 = sns.scatterplot(x_data, y_data, s = 15, hue = labels, palette = "Set1")

    # figure level
    plt.xlabel('Stand. ' + elements_in[x-1] + ' (a.u.)', fontsize=axis_label_sizes)
    plt.ylabel('Stand. XBIC (a.u.)', fontsize=axis_label_sizes)
    #plt.title(samp['Name'] + ' scan ' + str(samp['XBIC_scans'][scan]))
    # axis level
    ax0.tick_params(labelsize = 14)                     #formats size of ticklabels
    return #plt.show(fig)


samp = TS58A
scan = 0     # --> index of scan 
x_channel = 1 # --> 0:XBIC 1:Cu 2:Cd
y_channel = 0 # --> 0:XBIC 1:Cu 2:Cd
label_sizes = 16
plot_nice_stats(samp, scan_i, x_channel, y_channel, label_sizes)

#z = test_data[:, z_variable]

#fig, (ax1, ax2) = plt.subplots(1, 2)
#fig.suptitle('Scatter and Map '+ samp['Name'] + ' ' + str(samp['XBIC_scans'][scan_i]))



# =============================================================================
# fig, ax1 = plt.subplots()
# ax1 = sns.distplot(x)
# plt.title(samp['Name'] + ' scan ' + str(samp['XBIC_scans'][scan_i]))
# =============================================================================
