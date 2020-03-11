'''
created: Fri Aug 16 14:49:13 2019
author: Trumann
'''
import plot_defs as PLT
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
SAMP = NBL3_2; SCAN =0; CHAN = 1
DATA_KEY = 'XBIC_corr'
LABELS = [24,22,18, 30,30] #[axis_title, axis_ticks, Xaxis_tick_interval, Yaxis_tick_interval]

colors = [(0, 0, 0), (0.5, 0, 0), (1, 0, 0)]  # R -> G -> B
cmap_name = 'imgj_reds'
# Create the colormap
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=255)
# use this function to plot area-density, corrected elemental maps
    # feature integer equals the index of the elmenent as seen in 'elements'
PLT.plot_nice_2Dmap(SAMP, DATA_KEY, SCAN, CHAN, LABELS, 'Oranges_r', '\u03BCg/cm'+ r'$^{2}$') 


#%%
# use this function to plot standardized maps for cross-sample comparison
# NOTE: run data transformation before this funciton to get the right dict keys
    # (adds nan columns)
    # feature_idx
SAMP = TS58A; SCAN = 1; CHAN = 0
DATA_KEY = 'XBIC_maps'
PLT.from_stand_to_stand_map(SAMP, SCAN, DATA_KEY, CHAN, 'magma', 'Stand. XBIC')

#PLT.map_to_hist(samp, scan, axis_label_sizes, 'elXBIC_corr', 1, 50)
#%%
# use to plot kmenas clusters in x and y #
samp = NBL3_3
h5_key = 'XBIC_h5s'
data_key = 'XBIC_maps'
model_key = 'XBICkmeans_trials'
scan = 0; ktrial= 0; feature = 0 
# 'feature' is to easily get shape of original map;
    # the same mask will apply to all features --> changes features should have no effect on the cluster map shown as 
h5 = samp[h5_key][scan]
original_map = samp[data_key][scan][feature,:,:-2]
model = samp[model_key][scan][ktrial,:]
# use this function to plot nice cluster maps
    # USE THIS FUNCTION ONLY IF WHOLE STAT ARRAY IS THIS INPUT TO home_clustering.kmeans_trials()
    # i.e. no XBIC_slim
import plot_defs as PLT
PLT.plot_cluster_map(h5, original_map, model, 3)


#%%
# NICE HEXBIN PLOT WITH HISTOGRAMS: SETUP #
fig = plt.figure(figsize=(5,5))
grid = plt.GridSpec(4, 4, hspace=0.2, wspace=0.2)
main_ax = fig.add_subplot(grid[-3:, :-1])
x_hist = fig.add_subplot(grid[0, :-1], xticklabels=[], xticks=[])
y_hist = fig.add_subplot(grid[-3:, 3], yticklabels=[], yticks=[])
# plot #
main_ax.hexbin(x,y, mincnt=1, cmap='Greys', gridsize=(50,20))
#main_ax.scatter(x,y,s=2, c='#808080')
main_ax.plot(x, ypred, color='#0f0f0f', linestyle='--', linewidth=3)
main_ax.set_xlim([np.min(x), np.max(x)])
main_ax.set_ylim([np.min(y), np.max(y)])
x_hist.hist(x, 40, orientation='vertical', color='gray')
y_hist.hist(y, 40, orientation='horizontal', color='gray')
TXT_PLACE = [-1,2]
TXT_PLACE = [0,2]
main_ax.text(TXT_PLACE[0], TXT_PLACE[1], "m={0:.3g}, b={1:.3g}".format(
        FITTING.coef_[0][0], FITTING.intercept_[0]))

def export_to_ImgJ(path, sample, scan_idx, shaped_data, ch_idx, color, name, 
                             dpi, resize_fact, save):
    plot=sample[shaped_data][scan_idx][ch_idx,:,:-2]
    fig = plt.figure(frameon=False)
    fig.set_size_inches(plot.shape[1]/(dpi*resize_fact), plot.shape[0]/(dpi*resize_fact))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(plot, cmap=color)
    if save == 1:
        fname = r'\{samp}_scan{num}_{ele}.png'.format(
                samp=sample['Name'], 
                num=str(sample['XBIC_scans'][scan_idx]), 
                ele=name)
        directory= path+fname
        plt.savefig(directory, dpi=(dpi * resize_fact))
    else: pass
    return

PATH = r'Z:\Trumann\XRF images\py_exports_bulk\NBL3_3\scan491'
NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Mo', 'Zn']
CMAPS = ['magma', 'Oranges_r', 'Blues_r', 'Greens_r', 'Reds_r', 'Greys_r']
SAMPLE= NBL3_3; SCAN = 4; CHAN = 0
# export to imagej #
export_to_ImgJ(PATH, SAMPLE, SCAN, 'XBIC_maps', CHAN, CMAPS[CHAN], NAMES[CHAN],
                         dpi=96, resize_fact=0.5, save=0)