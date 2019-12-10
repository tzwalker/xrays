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
import sklearn.preprocessing as sklp
from skimage import io
scaler = sklp.StandardScaler()
# this dictionary contains the sample (interface) scan idx that was analyzed in ImageJ #
# for fast reference, but may be useful later #
#IMG_J_GROUPS = {"base": [TS58A, 1], "hiT": [NBL3_2, 0], "hiCu": [NBL3_3, 0]}

SAMP = TS58A; SCAN = 1; CHAN=1; CHECK_MASK=1
IMG_PATH = r'Z:\Trumann\XRF images\py_exports_interface\{sample}\scan{scan_idx}'.format(sample=SAMP['Name'], scan_idx=SAMP['XBIC_scans'][SCAN])
MASKFILE = IMG_PATH + r'\bound_0in_2out_mask.txt' # <-- CORES OR BOUNDARIES 
mask = np.loadtxt(MASKFILE)
mask_plot = np.ma.masked_where(mask == 0, mask) # to plot transparent mask

NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Mo', 'Zn']
CMAPS = ['magma', 'Oranges_r', 'Greens_r', 'Blues_r', 'Reds_r', 'Greys_r']
# check mask #
if CHECK_MASK == 1:
    img = SAMP['XBIC_maps'][SCAN][CHAN,:,:-2]
    img_filt = gfilt(img, sigma=1)
    plt.imshow(img, cmap=CMAPS[CHAN])
    plt.imshow(mask_plot, cmap='cool')
else: pass
#%%
PLOT_SWITCH=4
XCHAN = 2; YCHAN = 0
# raw, pix-by-pix correlation #
if PLOT_SWITCH == 0:
    xchan = SAMP['XBIC_maps'][SCAN][XCHAN,:,:-2]; ychan = SAMP['XBIC_maps'][SCAN][YCHAN,:,:-2] 
    x = xchan.ravel().reshape(-1,1); y = ychan.ravel().reshape(-1,1)

# gaussian filtered, pix-by-pix correlation #
if PLOT_SWITCH == 1:
    xchan = SAMP['XBIC_maps'][SCAN][XCHAN,:,:-2]; ychan = SAMP['XBIC_maps'][SCAN][YCHAN,:,:-2] 
    xfilt = gfilt(xchan, sigma=1); yfilt = gfilt(ychan, sigma=1)
    x = xfilt.ravel().reshape(-1,1); y = yfilt.ravel().reshape(-1,1)
# gaussian filtered, masked pix-pix correlation #
if PLOT_SWITCH == 2:
    xchan = SAMP['XBIC_maps'][SCAN][XCHAN,:,:-2]; ychan = SAMP['XBIC_maps'][SCAN][YCHAN,:,:-2] 
    xfilt = gfilt(xchan, sigma=1); yfilt = gfilt(ychan, sigma=1)
    xmasked = xfilt[np.where(mask!=0)]; ymasked = yfilt[np.where(mask!=0)]
    x = xmasked.reshape(-1,1); y = ymasked.reshape(-1,1)
TXT_PLACE=[0.35*np.max(x), 0.97*np.max(y)]
# for XBIC vs. XRF comparisons #
if PLOT_SWITCH==3:
    xchan = SAMP['XBIC_maps'][SCAN][XCHAN,:,:-2]; ychan = SAMP['XBIC_maps'][SCAN][YCHAN,:,:-2] 
    xfilt = gfilt(xchan, sigma=1)
    xmasked = xfilt[np.where(mask!=0)]; ymasked = yfilt[np.where(mask!=0)]
    xshaped = xmasked.reshape(-1,1); yshaped = ymasked.reshape(-1,1)
    scaler = sklp.StandardScaler()
    x = scaler.fit_transform(xshaped); y=scaler.fit_transform(yshaped)
    TXT_PLACE = [-1,2]

# use enhanced image from IMageJ #
if PLOT_SWITCH==4:
    XIMG_FILE = r'Z:\Trumann\XRF images\py_exports_interface\{sample}\scan{scan_idx}\{channel}.tif'.format(
            sample=SAMP['Name'], scan_idx=SAMP['XBIC_scans'][SCAN], channel=NAMES[XCHAN])
    ximg = io.imread(XIMG_FILE)
    
    YIMG_FILE = r'Z:\Trumann\XRF images\py_exports_interface\{sample}\scan{scan_idx}\{channel}.tif'.format(
            sample=SAMP['Name'], scan_idx=SAMP['XBIC_scans'][SCAN], channel=NAMES[YCHAN])
    yimg= io.imread(YIMG_FILE)
    CHECK_ENHANCED_MASK = 1
    # check mask #
    if CHECK_ENHANCED_MASK == 1:
        fig, (ax0, ax1) = plt.subplots(1,2)
        ax0.imshow(ximg, cmap=CMAPS[XCHAN])
        ax0.imshow(mask_plot, cmap='cool')
        ax1.imshow(yimg, cmap=CMAPS[YCHAN])
        ax1.imshow(mask_plot, cmap='cool')
    else: pass
    
    XMASKED = ximg[np.where(mask!=0)]; YMASKED = yimg[np.where(mask!=0)]
    xshaped = XMASKED.reshape(-1,1); yshaped = YMASKED.reshape(-1,1)
    x = scaler.fit_transform(xshaped); y=scaler.fit_transform(yshaped)

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
#main_ax.hexbin(x,y, mincnt=1, cmap='Greys', gridsize=(50,20))
main_ax.scatter(x,y,s=2, c='#808080')
main_ax.plot(x, ypred, color='#0f0f0f', linestyle='--', linewidth=3)
main_ax.set_xlim([np.min(x), np.max(x)])
main_ax.set_ylim([np.min(y), np.max(y)])
x_hist.hist(x, 40, orientation='vertical', color='gray')
y_hist.hist(y, 40, orientation='horizontal', color='gray')
TXT_PLACE = [0,2]
main_ax.text(TXT_PLACE[0], TXT_PLACE[1], "m={0:.3g}, b={1:.3g}".format(model.coef_[0][0],model.intercept_[0]))

#%%
# comparing background substractions: ImageJ vs. python
from skimage import io
import scipy.ndimage as scim
from skimage.morphology import ball
import matplotlib.pyplot as plt

# comparison before python correction #
imgj = io.imread(r'Z:\Trumann\XRF images\py_exports_interface\NBL3_2\scan422\XBIC.tif')
imgp = NBL3_2['XBIC_maps'][0][0,:,:-2]
fig, (ax0,ax1) = plt.subplots(1,2)
ax0.imshow(imgp)
ax1.imshow(imgj)

# python correction# 
s = ball(15) # Create 3D ball structure
h = int((s.shape[1] + 1) / 2) # Take only the upper half of the ball
s = s[:h, :, :].sum(axis=0) # Flat the 3D ball to a weighted 2D disc
s = (1 * (s - s.min())) / (s.max()- s.min()) # Rescale weights into 0-1
# Use im-opening(im,ball) (i.e. white tophat transform) (see original publication)
imgp_corr = scim.white_tophat(imgp, structure=s)
fig, (ax0,ax1) = plt.subplots(1,2)
ax0.imshow(imgp)
ax1.imshow(imgp_corr)