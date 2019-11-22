### import image and experiment ###
from skimage import io, filters
from skimage.segmentation import watershed, mark_boundaries
import numpy as np
image = TS58A['XBIC_maps'][5][2,:,:-2]
#io.imshow(image, cmap='Greens_r')
edges = filters.sobel(image)
#io.imshow(edges, cmap='Greys_r')
segments = watershed(edges, markers=100, compactness=0.001)
boundaries = mark_boundaries(edges, segments, color=(1, 0, 0), mode='inner',  background_label=5,outline_color=None)
io.imshow(boundaries)
#nan_boundaries = boundaries.copy()
#nan_boundaries[nan_boundaries==0] = np.nan
#io.imshow(nan_boundaries)
#%%
### from interent; see py seg techniques in bookmarks
pic = plt.imread('1.jpeg')/255  # dividing by 255 to bring the pixel values between 0 and 1
print(pic.shape)
plt.imshow(pic)
pic_n = pic.reshape(pic.shape[0]*pic.shape[1], pic.shape[2])
pic_n.shape
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5, random_state=0).fit(pic_n)
pic2show = kmeans.cluster_centers_[kmeans.labels_]
cluster_pic = pic2show.reshape(pic.shape[0], pic.shape[1], pic.shape[2])
plt.imshow(cluster_pic)
#%%
image = TS58A['XBIC_maps'][5][3,:,:-2]
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
from skimage import feature
blurred = gaussian_filter(image, sigma=3)
plt.imshow(image, origin='lower')

# =============================================================================
# edges1 = feature.canny(blurred, sigma=2)
# fig, (ax0,ax1) = plt.subplots(1,2)
# ax0.imshow(blurred)
# ax1.imshow(edges1, cmap=plt.cm.gray)
# =============================================================================
#%%
# attempting to copy Math's result #
img = TS58A['XBIC_maps'][5][3,:,:-2]

from skimage.segmentation import slic, mark_boundaries
import numpy as np; import matplotlib.pyplot as plt
img = np.float64(img)
edges = slic(img, n_segments=100, compactness=50, sigma=0)
bm = mark_boundaries(img, edges, color=(1, 1, 0))
fig, (ax0, ax1) = plt.subplots(1,2)
ax0.imshow(img, origin='lower', cmap='viridis')
ax1.imshow(bm[:,:,0], origin='lower', cmap='viridis')

