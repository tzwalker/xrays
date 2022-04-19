# -*- coding: utf-8 -*-
"""

Trumann
Tue Apr 19 11:17:39 2022

run main-TS118_1A-ASCII.py
before this program

this program is meant to test 3D plotting and 2D guassian fitting
of the 'pit' in TS118_1A/2018_11_26IDC/scan197/

"""
import numpy as np

img = TS1181A.scan197[0,:,:]
data = img.copy()
data = data * 1e9

# Make data.
step = 0.5 # pixel size, um
r0 = 0 #start
rx = 30 #um
ry = 50 #um

X = np.array(list(range(0,61,1)))
Y = np.array(list(range(0,101,1)))

X, Y = np.meshgrid(X, Y)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Plot the surface.
surf = ax.plot_surface(X, Y, data, cmap='inferno',
                       linewidth=0, antialiased=False)

ax.view_init(elev=55., azim=-35)

#%%
# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)