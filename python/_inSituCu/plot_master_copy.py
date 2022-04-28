"""
coding: utf-8

tzwalker
Fri Aug 27 09:27:09 2021

this program is meant to plot extra cross section maps of in situ cross section
2021_11_2IDD

these maps all had different scan parameters, and a single scale bar is not adequate

these three scans had the same y center motor coordinate: 0.1862mm
but slightly different x center coordinates
img1 x center: 0.171500;
img2 x center: 0.172000;
img3 x center: 0.173000;

if i shift these with respect to img1, then they should be in same position

# scan238 img 1 has different resolution, 8.2  /41, 10.3 /31
# scan254 img 2 has different resolution, 8.2  /41, 10.5 /21
# scan524 img 3 has different resolution, 10.2 /51, 10.5 /21
just be careful when you apply ticklabels to these images

"""


import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker

img1 = Cu1b4c.maps[0][1,:,:]
img2 = Cu1b4c.maps[1][1,:,:]
img3 = Cu1b4c.maps[-1][1,:,:]

fig, (ax1,ax2,ax3) = plt.subplots(3,1,figsize=(3.5,2.5))
#ax1.figure()
ax1.imshow(img1, cmap='magma')
#plt.figure()
ax2.imshow(img2, cmap='magma')
#plt.figure()
ax3.imshow(img3, cmap='magma')
plt.tight_layout()

avg1 = np.mean(img1)


