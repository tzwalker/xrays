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
import matplotlib.pyplot as plt
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb, watershed
from skimage.segmentation import mark_boundaries

cu = TS58A['XBIC_maps'][5][1,:,:-2]
te = TS58A['XBIC_maps'][5][3,:,:-2]

fig, (ax0,ax1) =plt.subplots(1,2)
ax0.imshow(cu)
ax1.imshow(te)

cu_dub = cu.astype('float64')
cd_dub = te.astype('float64')
segments_00 = felzenszwalb(cu_dub, scale=100, sigma=1.5, min_size=200)
segments_01 = felzenszwalb(cd_dub, scale=100, sigma=1.5, min_size=100)
fig, (ax0,ax1) = plt.subplots(1,2)
ax0.imshow(cu); ax0.imshow(mark_boundaries(cu_dub, segments_00), alpha=0.5)
ax1.imshow(cd); ax1.imshow(mark_boundaries(cd_dub, segments_01), alpha=0.5)
plt.tight_layout()

scu = sobel(cu)
scd = sobel(te)
segments_02 = watershed(scu, markers=100, compactness=0.001)
segments_03 = watershed(scd, markers=100, compactness=0.001)
fig, (ax2,ax3) = plt.subplots(1,2)
arr= mark_boundaries(scu, segments_02); arr1 = mark_boundaries(scd, segments_03)
arr[arr==0] = np.nan; arr1[arr1==0] = np.nan
ax2.imshow(arr)
ax3.imshow(arr1)
plt.tight_layout()