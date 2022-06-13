# -*- coding: utf-8 -*-
"""

Trumann
Tue Jun  7 08:54:08 2022

this program is meant to analyze ToF-SIMS images 

"""

'''
this cell will match area the ToF SIMS area to the EBSD area
    imports, integrated, and rotates

sort of preparation for registration

'''
import cv2
from skimage import io,transform
import matplotlib.pyplot as plt
import numpy as np

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

PATH_TOF = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Cl_maps.tif"

# import ToF-SIMS image
TOF = io.imread(PATH_TOF)

# take average from top 3 depth slices, excluding first slice
# averaging give float array
# summing give integer array
# a float array is needed for image transforms
# the integer array can be 
TOF_slice = TOF[1:4,:,:].mean(axis=0)
#TOF_slice = TOF[0,:,:].astype('float64')


# alter image to match EBSD in EBSD_v1.py
img = rotate_image(TOF_slice, 90)   # rotate image
img = np.flipud(img)                # flip along horizontal axis
img = rotate_image(img, -3)         # rotate altered image

# crop image to about same dimension as EBSD
img = img[75:425,100:450]

# check 
fig, ax = plt.subplots()
ax.imshow(img, vmax=0.5)
ax.axis("off")
ax.set_aspect(0.9)

#%%
'''
this cell will integrate the Se channel across its depth

want to check Se againt cross-section Se XRF and dynmiac Se SIMS

'''
from skimage import io
import numpy as np
import matplotlib.pyplot as plt

tof0 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Se_maps.tif"
# import ToF-SIMS image
TOF = io.imread(tof0)
# average of each slice
p = TOF.mean(axis=(1,2))
# total in each slice
pp = TOF.sum(axis=(1,2))
# depth calibration
d = np.arange(0,5.39,0.11) # um

tof500 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Se_maps.tif"
# import ToF-SIMS image
TOF1 = io.imread(tof500)
# average of each slice
p1 = TOF1.mean(axis=(1,2))
# total in each slice
p11 = TOF1.sum(axis=(1,2))
# depth calibration
d1 = np.arange(0,7.56,0.135) # um

fig, ax = plt.subplots()
ax.plot(d, p, label='0hr')
ax.plot(d1, p1, label='500hr')
plt.legend()


#%%
'''
this cell attemptes to plot the data cube in 3D
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

#%%
# create some fake data
x = y = np.arange(-4.0, 4.0, 0.02)
# here are the x,y and respective z values
X, Y = np.meshgrid(x, y)
Z = np.sinc(np.sqrt(X*X+Y*Y))
# this is the value to use for the color
V = np.sin(Y)

# create the figure, add a 3d axis, set the viewing angle
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(45,60)

# here we create the surface plot, but pass V through a colormap
# to create a different color for each patch
ax.plot_surface(X, Y, Z, facecolors=cm.Oranges(V))

#%%
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

x   = np.linspace(1,5,100)
y1  = np.ones(x.size)
y2  = np.ones(x.size)*2
y3  = np.ones(x.size)*3
z   = np.sin(x/2)

plt.figure()
ax = plt.subplot(projection='3d')
ax.imshow(x, y1, z, color='r')
ax.plot(x, y2, z, color='g')
ax.plot(x, y3, z, color='b')


