### NOTES: z_plotting.py, spacing axes
import seaborn as sns
import pandas as pd
from scipy.ndimage.filters import gaussian_filter
from skimage.filters import sobel
import numpy as np
import matplotlib.pyplot as plt

## ticklabel formating
# how to figure out what the proper indeices to plot are...?
# the integer in xticklabels represents every 'n' index to be plotted
    # e.g. xtixklabels = 50 --> 0, 50, 150 all plotted
    # the list x_real has actual numbers that map to the indices... but how does that help me...   
    # could use mod?
# find where first whole number is in x_real!
  # get index of this number... 
  # when would whole number not exist...? 
      # when the width of the axis is not evenly split by the resolution
      # e.g. np.linspace(0,16,38)
  # HOWEVER: the first and last number, as they are int, are guaranteed
      # to be whole, therefore, the above approach will always find a whole number index
      # and will plot either the bounds of the axes, or every whole number that exists in the linear space!

practice_axis_list = list(practice_axis)

max(practice_axis_list)
Out[152]: 1484.7

min(practice_axis_list)
Out[153]: 1469.7

max(practice_axis_list) - min(practice_axis_list)
Out[154]: 15.0

np.linspace(0, max(practice_axis_list) - min(practice_axis_list),5)
Out[155]: array([ 0.  ,  3.75,  7.5 , 11.25, 15.  ])

np.linspace(0, max(practice_axis_list) - min(practice_axis_list), len(practice_axis_list))
Out[156] 
array([ 0.  ,  0.15,  0.3 ,  0.45,  0.6 ,  0.75,  0.9 ,  1.05,  1.2 ,
        1.35,  1.5 ,  1.65,  1.8 ,  1.95,  2.1 ,  2.25,  2.4 ,  2.55,
        2.7 ,  2.85,  3.  ,  3.15,  3.3 ,  3.45,  3.6 ,  3.75,  3.9 ,
        4.05,  4.2 ,  4.35,  4.5 ,  4.65,  4.8 ,  4.95,  5.1 ,  5.25,
        5.4 ,  5.55,  5.7 ,  5.85,  6.  ,  6.15,  6.3 ,  6.45,  6.6 ,
        6.75,  6.9 ,  7.05,  7.2 ,  7.35,  7.5 ,  7.65,  7.8 ,  7.95,
        8.1 ,  8.25,  8.4 ,  8.55,  8.7 ,  8.85,  9.  ,  9.15,  9.3 ,
        9.45,  9.6 ,  9.75,  9.9 , 10.05, 10.2 , 10.35, 10.5 , 10.65,
       10.8 , 10.95, 11.1 , 11.25, 11.4 , 11.55, 11.7 , 11.85, 12.  ,
       12.15, 12.3 , 12.45, 12.6 , 12.75, 12.9 , 13.05, 13.2 , 13.35,
       13.5 , 13.65, 13.8 , 13.95, 14.1 , 14.25, 14.4 , 14.55, 14.7 ,
       14.85, 15.  ])

# stack overflow attempts
x = np.linspace(0, 15, 151)
y = np.linspace(0, 15, 151)

my_data = NBL3_2['XBIC_maps'][3]
df_map = pd.DataFrame(my_data, index = y, columns = x) 
plt.figure()
ax = sns.heatmap(df_map, square = True, xticklabels  = 20, yticklabels = 20)
ax.invert_yaxis()

fmtr = tkr.StrMethodFormatter('{x:.0f}')
ax.xaxis.set_major_formatter(fmtr)
fmtr = tkr.StrMethodFormatter("{x:.0f}")
locator = tkr.MultipleLocator(50)
fstrform = tkr.FormatStrFormatter('%.0f')

#plt.gca().xaxis.set_major_formatter(fmtr)
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(fstrform)
plt.show()

## for 3D plots, be sure to change matplotlib backend from 'inline' to 'qt'
ax = Axes3D(fig, rect=[0, 0, .95, 1]) 
ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('Cu')
ax.set_ylabel('XBIC')
ax.set_zlabel('Cd')
# Set rotation angle to 30 degrees
ax.view_init(azim=0)
for angle in range(0, 360):
    ax.view_init(60, angle)
    plt.draw()
    plt.show()
    plt.pause(0.001)
    
## masked scatterplots 
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

### NOTES: z_img_processing.py
# =============================================================================
# 
#     # pix by pix product
#     product = cu_gradient * zn_gradient
#     # geometric mean of gradients
#     gmean = np.sqrt(product)
# =============================================================================
fig, (ax0,ax1) = plt.subplots(nrows=1,ncols=2)
plt.tight_layout()
sns.heatmap(samp_maps[0],square=True, ax=ax0, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
sns.heatmap(grad_matrix, square=True, ax=ax1,xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
sns.heatmap(grad_matrix[1], square=True, ax=ax2,xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()

for index, Map in enumerate(samp_maps):
    fig, (ax0, ax1) = plt.subplots(nrows=1,ncols=2)
    gradient_map = calc_grad_map(Map)
    sns.heatmap(Map, square=True, ax=ax0, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
    sns.heatmap(gradient_map, square=True, ax=ax1, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()

# gaussian filter of (shaped) standardized data
cu_stand = cu_stand.reshape(np.shape(gauss_map))
gauss_of_cu_stand = gaussian_filter(cu_stand, sigma=2)
zn_stand = zn_stand.reshape(np.shape(gauss_map))
gauss_of_zn_stand = gaussian_filter(zn_stand, sigma=2)

# threshold percentile of gradient map
cu_gradient_75quart_thres = np.percentile(cu_gradient_no_edge, percentile)
zn_gradient_75quart_thres = np.percentile(zn_gradient_no_edge, percentile)
# find pixels in gradient map within a given percentile
cu_mask = np.where(cu_gradient >= cu_gradient_75quart_thres, 1,0) # retains shape
zn_mask = np.where(zn_gradient >= zn_gradient_75quart_thres, 1,0)
# find where gradient maps mismatch --> quantifies the error in saying g.bs are where the gradients lie??
a_mismatched_map = np.where(cu_mask == zn_mask, 1, 0)
# parameter to minimize mismatch
mismatch = a_mismatched_map.sum()
print(percentile, mismatch, round(mismatch/init_mismatch, 3))

fig, (ax0, ax1, ax2) = plt.subplots(nrows=1,ncols=3)
plt.tight_layout()
ax0.imshow(cu_mask, origin='lower', cmap='Greys_r')
ax1.imshow(zn_mask, origin='lower', cmap='Greys_r')
ax2.imshow(a_mismatched_map, origin='lower', cmap='Greys_r')
#if mismatch < init_mismatch:
    #best_percentile = percentile
# for each pixel in the masks, if values match, record pixel coordinates for indexing into real data arrays, plot on scatter
#calculatign Sobel gradient; identifying edges of images
   # works well for XBIC, not so well for Cu and Cd, which contain noise (see consolidated notes)
   # next step: apply gaussian filter to XRF, then find edges (or alter Sobel kernels, ,if possible)

     # --> matches pixels in the gradient maps that are above a certaiin percentile... make bulk stats of number of matches among the various areas scanned

### never used; for applying filter to every loaded
    # XRF channel in every scan
    # problematic if channel has large variances (ex. Cd or Mo)
def gauss_filtXRF(samps, ele_index, data_in_keys, data_out_keys):
    for samp in samps:
        c_filt_maps = []
        for scan in samp[data_in_keys[0]]:
            ele_map = scan[ele_index][:,:-2] # element map without nan columns (not compatible with filter)
            ele_arr = ele_map.ravel()   # array for stats
            sig = 3*np.var(ele_arr)     # define degree of filtering
            filt_map = gaussian_filter(ele_map, sigma=sig) # apply filter to map
            c_filt_maps.append(filt_map)
        build_dict(samp, data_out_keys[0], c_filt_maps)
        v_filt_maps = []
        for scan in samp[data_in_keys[1]]:
            ele_map = scan[ele_index][:,:-2] # element map without nan columns (not compatible with filter)
            ele_arr = ele_map.ravel()   # array for stats
            sig = 3*np.var(ele_arr)     # define degree of filtering
            filt_map = gaussian_filter(ele_map, sigma=sig) # apply filter to map
            v_filt_maps.append(filt_map)
        build_dict(samp, data_out_keys[1], v_filt_maps)
    return

### experimenting with xbic xbiv alignment
# cannot be used when kclustering is called on reduced arrays
def quick_label_check(original_map, model):
    clust_map = model.labels_.reshape(np.shape(original_map))
    plt.imshow(clust_map, origin='lower')
    return
### view difference between mask generated from clusters with filtered vs. non-filtered XRF channel
    # filtered (single, Cu) XRF channel; applied clustering algorithim 
    # refer to consolidated notes for some results: mostly no difference for good maps
cu = NBL3_2['elXBIC'][2][0][:,:-2]
model = NBL3_2['c_kmodels'][2]
quick_label_check(cu, model)

cu_arr = cu_map.ravel()
# check maps
fig, axs = plt.subplots(1,2)
axs[0].imshow(ele_map)
# ravel filtered map
filt_arr = filt_map.ravel()
filt_arr = filt_arr.reshape(-1,1)
# cluster filtered map
model = KMeans(init='k-means++', n_clusters=3, n_init=10) 
filt_clust = model.fit(filt_arr)
# check clusters
filt_clust_map = filt_clust.labels_.reshape(np.shape(ele_map))
axs[1].imshow(filt_clust_map, cmap='Greys')
plt.figure()
sns.distplot(ele_arr, bins=50)


# get the maps
xbic = NBL3_3['XBIC_maps'][0][:,:-2] ; xbic_sob = sobel(xbic)
#xbiv = NBL3_2['elXBIC'][1][2][:,:-2] ; xbiv_sob = sobel(xbiv)

quick_label_check(xbic, NBL3_2['c_kmodels'][0])
# map check
fig, (ax0,ax1) = plt.subplots(1,2)
plt.tight_layout()
ax0.imshow(xbic, origin='lower')
ax1.imshow(xbiv, origin='lower')

plt.figure()
fig1, (ax1,ax2) = plt.subplots(1,2)
plt.tight_layout()
ax1.imshow(xbic_sob, origin='lower')
ax2.imshow(xbiv_sob, origin='lower')

# if necessary, filter map; sobel maps as well
xbic_filt = gaussian_filter(xbic, sigma=1) 
xbiv_filt = gaussian_filter(xbiv, sigma=1) 

# map check


# correlation check
plt.figure()
plt.scatter(xbic_sob,xbiv_sob, s=3)
plt.xlim([np.min(xbic_sob), np.max(xbic_sob)])
plt.ylim([np.min(xbiv_sob), np.max(xbiv_sob)])

### plotting 2-feature cluster map for a sample
map1 = NBL3_2['elXBIC'][0][1]
map2 =  NBL3_2['elXBIC'][0][3]
labels = NBL3_2['c_kmodels'][0].labels_
label_map = np.reshape(labels, (101,99))



def custom_format_ticks(axes_object_labels, string_type):
    txt_labs = [label.get_text() for label in axes_object_labels]
    ticking = [string_type.format(float(txt)) for txt in txt_labs]
    return ticking

def get_real_coordinates(axis_list):
    data_coord = list(axis_list)
    axis_width = max(data_coord) - min(data_coord)
    axis_resolution = np.linspace(0, axis_width, len(data_coord))
    round_steps = [round(i,3) for i in axis_resolution]
    return round_steps

y_width = np.linspace(0, 15, 101)
x_width = np.linspace(0, 15, 99)
y = [round(i,3) for i in y_width]
x = [round(i,0) for i in x_width]
label_map = pd.DataFrame(label_map, index = y, columns = x)

fig, ax0 = plt.subplots()
#plt.tight_layout()
cbar_ticks = np.linspace(min(labels), max(labels), max(labels)+1)
ax0 = sns.heatmap(label_map, square = True, cmap='Greys', cbar_kws={"shrink": 1, "ticks":cbar_ticks}, xticklabels = 20, yticklabels = 20)

# figure level
plt.xlabel('X (\u03BCm)', fontsize=16)
plt.ylabel('Y (\u03BCm)', fontsize=16)
# axis level
ax0.tick_params(labelsize = 14)                     #formats size of ticklabels
x_labls = custom_format_ticks(ax0.get_xticklabels(), '{:g}')
y_labls = custom_format_ticks(ax0.get_yticklabels(), '{:g}')         #formats tick label strings without ".0"
ax0.set_xticklabels(x_labls)                        #set the tick labels
ax0.set_yticklabels(y_labls, rotation = 0)          #set the ticklabels and rotate (if needed)
ax0.invert_yaxis()                                  #invert the yaxis after formatting is complete

#fig.colorbar(ax0).ax0 <--> plt.gcf().axes[-1]
cbar_ax = plt.gcf().axes[-1]                        #gets colorbar of current figure object, behaves as second y axes object
# colorbar label settings
cbar_ax.set_ylabel('Cluster', fontsize = 16, 
                   rotation = -90, labelpad = 20)    #label formatting
cbar_ax.tick_params(labelsize=12)                   #tick label formatting
cbar_ax.yaxis.get_offset_text().set(size=12)        #format colorbar offset text
#z_labls = custom_format_ticks(cbar_ax.get_yticklabels(), '{:g}')
#sns.heatmap(map1, square = True, ax = ax1, cbar_kws={"shrink": 0.50}, xticklabels = 20, yticklabels = 20).invert_yaxis()
#sns.heatmap(map2, square = True, ax = ax2, cbar_kws={"shrink": 0.50}, xticklabels = 20, yticklabels = 20).invert_yaxis()
