from sklearn.cluster import KMeans
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
from skimage import io, filters, feature
from skimage.segmentation import slic, mark_boundaries, watershed
import numpy as np
# kmeans clustering 5-dimensional image (x,y, R,G,B); see online bookmarks #
pic = plt.imread('1.jpeg')/255  # dividing by 255 to bring the pixel values between 0 and 1
print(pic.shape)
plt.imshow(pic)
pic_n = pic.reshape(pic.shape[0]*pic.shape[1], pic.shape[2])
pic_n.shape

kmeans = KMeans(n_clusters=5, random_state=0).fit(pic_n)
pic2show = kmeans.cluster_centers_[kmeans.labels_]
cluster_pic = pic2show.reshape(pic.shape[0], pic.shape[1], pic.shape[2])
plt.imshow(cluster_pic)

#%%
# simple img processing tests #
image = TS58A['XBIC_maps'][5][3,:,:-2]

blurred = gaussian_filter(image, sigma=3)
plt.imshow(image, origin='lower')

edges1 = feature.canny(blurred, sigma=2)
fig, (ax0,ax1) = plt.subplots(1,2)
ax0.imshow(blurred)
ax1.imshow(edges1, cmap=plt.cm.gray)

#%%
# attempting to copy Math's result #
img = TS58A['XBIC_maps'][5][3,:,:-2]
img = np.float64(img)
edges = slic(img, n_segments=100, compactness=50, sigma=0)
bm = mark_boundaries(img, edges, color=(1, 1, 0))
fig, (ax0, ax1) = plt.subplots(1,2)
ax0.imshow(img, origin='lower', cmap='viridis')
ax1.imshow(bm[:,:,0], origin='lower', cmap='viridis')

edges = filters.sobel(img)
segments = watershed(edges, markers=100, compactness=0.001)
boundaries = mark_boundaries(edges, segments, color=(1, 0, 0), mode='inner',  background_label=5,outline_color=None)
io.imshow(boundaries)

#%%
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.ndimage import gaussian_filter as gfilt
from sklearn.linear_model import LinearRegression
# =============================================================================
# def plot_mask(map1, map2, mask_path, mask_type):
#     mask_txt = mask_path + r'\mask_{mtype}.txt'.format(mtype=mask_type)
#     mask = np.loadtxt(mask_txt)
#     mask1 = np.ma.masked_where(mask == 0, mask) # to plot transparent mask
#     selection_idxs = np.where(mask==0)
#     map1_filt = gfilt(map1, sigma=1)
#     vals1 = map1_filt[selection_idxs]
#     vals2 = map2[selection_idxs]
#     
#     fig, (ax0,ax1) = plt.subplots(1,2)
#     plt.tight_layout()
#     ax0.imshow(map1_filt); ax0.imshow(mask1)
#     ax1.imshow(map2); ax1.imshow(mask1)
#     plt.figure()
#     plt.hexbin(vals1, vals2, mincnt=1, cmap='Greys')
#     return mask
# 
# img = TS58A['XBIC_maps'][1][3,:,:-2]
# xbic = TS58A['XBIC_maps'][1][0,:,:-2]
# path = r'Z:\Trumann\XRF images\py_exports_interface\TS58A\scan386'
# m =  mask_corr(img, xbic, path, 'cores')
# =============================================================================
SAMP = NBL3_2; SCAN = 0; CHECK_MASK=1
file = r'Z:\Trumann\XRF images\py_exports_interface\{sample}\scan{scan_idx}\boundaries_outer_thick.txt'.format(
        sample=SAMP['Name'], scan_idx=SAMP['XBIC_scans'][SCAN])
mask = np.loadtxt(file)
mask_plot = np.ma.masked_where(mask == 0, mask) # to plot transparent mask

# check mask #
if CHECK_MASK == 1:
    img = SAMP['XBIC_maps'][SCAN][3,:,:-2]
    img_filt = gfilt(img, sigma=1)
    plt.imshow(img_filt, cmap='Greys_r')
    plt.imshow(mask_plot, cmap='cool')
else: pass
#%%
xchan = SAMP['XBIC_maps'][SCAN][2,:,:-2] 
ychan = SAMP['XBIC_maps'][SCAN][0,:,:-2] 

PLOT_SWITCH=2

# raw, pix-by-pix correlation #
if PLOT_SWITCH == 0:
    x = xchan.ravel().reshape(-1,1)
    y = ychan.ravel().reshape(-1,1)

# gaussian filtered, pix-by-pix correlation #
if PLOT_SWITCH == 1:
    xfilt = gfilt(xchan, sigma=1)
    yfilt = gfilt(ychan, sigma=1)
    x = xfilt.ravel().reshape(-1,1)
    y = yfilt.ravel().reshape(-1,1)
if PLOT_SWITCH == 2:
    xfilt = gfilt(xchan, sigma=1)
    yfilt = gfilt(ychan, sigma=1)
    xboundaries = xfilt[np.where(mask!=0)]
    yboundaries = yfilt[np.where(mask!=0)]
    x = xboundaries.reshape(-1,1)
    y = yboundaries.reshape(-1,1)
    
# manual regression #
MODELR = LinearRegression()
model = MODELR.fit(x, y)
ypred = model.predict(x)
# plot setup #
fig = plt.figure(figsize=(5,5))
grid = plt.GridSpec(4, 4, hspace=0.2, wspace=0.2)
main_ax = fig.add_subplot(grid[-3:, :-1])
x_hist = fig.add_subplot(grid[0, :-1], xticklabels=[], xticks=[])
y_hist = fig.add_subplot(grid[-3:, 3], yticklabels=[], yticks=[])
# plot #
main_ax.hexbin(x,y, mincnt=1, cmap='Greys', gridsize=(50,20))
main_ax.plot(x, ypred, color='#0f0f0f', linestyle='--', linewidth=3)
main_ax.set_xlim([np.min(x), np.max(x)])
main_ax.set_ylim([np.min(y), np.max(y)])
x_hist.hist(x, 40, orientation='vertical', color='gray')
y_hist.hist(y, 40, orientation='horizontal', color='gray')
main_ax.text(0.35*np.max(x), 0.97*np.max(y), "m={0:.3g}, b={1:.3g}".format(model.coef_[0][0],model.intercept_[0]))
