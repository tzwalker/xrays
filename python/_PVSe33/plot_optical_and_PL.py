"""
coding: utf-8

tzwalker
Wed Feb  3 09:49:31 2021

this program plots the optical image, area of the optical image, and
    the PL intensity as a function of x and y position for a single energy 
    (e.g. 1.51eV) 
this program uses the packages provided here:
    https://github.com/alchem0x2A/py-wdf-reader
it is highly recommended to install these packages through the Anaconda
    distirbution and use them inside the Spyder environment

"""

from renishawWiRE import WDFReader
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
 
IN_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\PL'
FNAME = r'\20210119 PVSe33.4_3SLAC PL MAP - Au side test2.wdf'

# import wdf file
filename = IN_PATH+FNAME
reader = WDFReader(filename)
reader.print_info()

### access spectral and optical image data
# get x-axis of spectral data
    # keep in mind the units you specified for the measurement
    # here the measurement was made using the eV as the x-axis
energy = reader.xdata
# specify the x-axis value you wish to plot
    # here the CdTe bandgap is 1.51 at room temperature (Fonthal, 1999)
Eg_CdTe = 1.51
# find the value in the x-axis that is closest to the specified x-axis value
E_idx = (np.abs(energy - Eg_CdTe)).argmin()

# get the spectral data from the map; has form (y_pixel, x_pixel, intensity)
spectra = reader.spectra

# get optical image
img = mpimg.imread(reader.img, format="jpg")

### specify mapping bounds for plotting
# get relative positions of the x and y motors
map_x = reader.xpos
map_y = reader.ypos
# specificy the bounds of the area that was measured
bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
# specify the bounds on the optical image
img_x0, img_y0 = reader.img_origins
img_w, img_h = reader.img_dimensions
bounds_photo = (img_x0, img_x0 + img_w, img_y0 + img_h, img_y0)
# specify bounds for map area plotted on optical image
bounds_of_map_in_photo = (map_x.min(), map_y.min())
map_w = reader.map_info["x_span"]
map_h = reader.map_info["y_span"]

### plot optical image, the area that was measured, and the PL map
plt.subplot(121)
plt.imshow(img, extent=bounds_photo)
r = plt.Rectangle(xy=bounds_of_map_in_photo, width=map_w, height=map_h, fill=False)
plt.gca().add_patch(r)

plt.subplot(122)
plt.imshow(spectra[:,:,E_idx], extent=bounds_map) 