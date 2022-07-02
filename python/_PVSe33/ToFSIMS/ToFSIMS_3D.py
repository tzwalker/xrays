# -*- coding: utf-8 -*-
"""

Trumann
Fri Jun 10 16:04:37 2022

this program is meant to try and reconstruct the data cubes from the 
ToF SIMS measurements

it uses Se as an example

"""

'''
this cell constructs slices using a surface (e.g., imshow) for each depth step
'''
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from skimage import io
tof0 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Se_maps.tif"
# import ToF-SIMS image
TOF = io.imread(tof0)

data = TOF.copy().astype('int')
#a = data[30,:,:]
#data = np.random.randint(0,6,size=(49,512,512))
#data = np.random.random(size=(49,512,512))

# create a Normalize object with the correct range
norm = colors.Normalize(vmin=0, vmax=3)
# normalized_data contains values between 0 and 1
normalized_data = norm(data)

x = y = np.arange(0, 512, 1)
z = np.arange(30,40,1)

# here are the x,y and respective z values
X, Y = np.meshgrid(x*0.145, y*0.145) # calibration included

# create the figure, add a 3d axis, set the viewing angle
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(15,60)

for depth in z:
    Z = depth*0.145*np.ones(X.shape) # clibration included
    i = normalized_data[depth,:,:]
    ax.plot_surface(X,Y,Z,facecolors=cm.viridis(i))

ax.set_xlabel('X (um)')
ax.set_ylabel('Y (um )')
ax.set_zlabel('Z (um)')

# create a scalar mappable to create an appropriate colorbar
sm = cm.ScalarMappable(cmap=cm.viridis, norm=norm)
fig.colorbar(sm)

#%%
'''
this cell tried to plot a yz slice or yz integration
'''
from matplotlib.colors import LogNorm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from skimage import io

tof0 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Se_maps.tif"
# import ToF-SIMS image
TOF = io.imread(tof0)
# import data
data = TOF.copy().astype('int')
# integrate along y direction
yz = data.sum(axis=2)

tof1 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Se_maps.tif"
# import ToF-SIMS image
TOF1 = io.imread(tof1)
# import data
data1 = TOF1.copy().astype('int')
# integrate along y direction
yz1 = data1.sum(axis=2)

# =============================================================================
# fig , ax1 = plt.subplots()
# ax1.imshow(yz[:,200:300],norm=LogNorm(vmin=0.01, vmax=5000),cmap='Greys_r')
# 
# fig , ax2 = plt.subplots()
# ax2.imshow(yz1[:55,200:300], norm=LogNorm(vmin=0.01, vmax=5000),cmap="Reds_r")
# plt.tight_layout()
# =============================================================================


fig , ax1 = plt.subplots()
ax1.imshow(yz[:,200:300],vmin=0, vmax=1000)

fig , ax2 = plt.subplots()
ax2.imshow(yz1[:55,200:300], vmin=0, vmax=1000)
plt.tight_layout()

#%%
'''
this cell attemptes to plot the data cube in 3D; it is an old attempt
'''

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from skimage import io
import numpy as np

tof0 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Se_maps.tif"
# import ToF-SIMS image
TOF = io.imread(tof0)

x = y = np.arange(0, 512, 1)
z = 20
i = TOF[z,:,:]

# here are the x,y and respective z values
X, Y = np.meshgrid(x, y)
Z = z*np.ones(X.shape)

# create the figure, add a 3d axis, set the viewing angle
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(90,60)

# here we create the surface plot, but pass V through a colormap
# to create a different color for each patch
im = ax.plot_surface(X, Y, Z, facecolors=cm.viridis(i))
fig.colorbar(im)