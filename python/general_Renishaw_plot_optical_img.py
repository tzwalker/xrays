"""
coding: utf-8

tzwalker
Thu Feb 25 19:18:12 2021

this program plots the optical image, area of the optical image, and
    the PL intensity as a function of x and y position for a single energy 
    (e.g. 1.51eV) 
this program uses the packages provided here:
    https://github.com/alchem0x2A/py-wdf-reader
it is highly recommended to install these packages through the Anaconda
    distirbution and use them inside the Spyder environment
<<<<<<< HEAD:python/general_Renishaw_plot_optical_img.py
=======

primary filenames and Z:/ location:
    unstressed
		PL Au Side : 20210213 PVSe33 redo 2/PVSe33.3_2 Au Side_PL_map0
    20-hour stressed
		PL Au Side : 20210215 PVSe33.3_4SLAC/PL Au side map0.wdf 
    500-hour stressed
		PL Au Side : 20210203 PVSe33 redo/PL Au Side/PVSe334_3 - Au Side map 1
-the directories above reflect the directory on the Z:/ drive

-to input the file into this program, use the following adjusted directories:
    unstreseed
        PL Au side: 20210213 PVSe33 redo 2 - PVSe33.3_2 Au Side_PL_map0.wdf
    20-hour stressed
        20210215 PVSe33.3_4SLAC - PL Au side map0.wdf
    500-hour stressed
        PL Au side: 20210203 PVSe33 redo PL Au Side PVSe334_3 - Au Side map 1.wdf
>>>>>>> cd0bb28cd7db3132e353a8aae5252334dce683f2:python/_PVSe33/map_analysis_PL.py
"""



from renishawWiRE import WDFReader
import matplotlib.pyplot as plt
import numpy as np
 
<<<<<<< HEAD:python/general_Renishaw_plot_optical_img.py
IN_PATH = r'Z:\Trumann\Renishaw\20210119 PVSe33 SLAC - PL front and back'
FNAME = r'\PVSe33.4_3SLAC PL MAP - Au side test2.wdf'
=======
IN_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\PL'
FNAME = r'\20210213 PVSe33 redo 2 - PVSe33.3_2 Au Side_PL_map0.wdf'
>>>>>>> cd0bb28cd7db3132e353a8aae5252334dce683f2:python/_PVSe33/map_analysis_PL.py

# import wdf file
filename = IN_PATH+FNAME
reader = WDFReader(filename)
reader.print_info()

### access spectral and optical image data
# get x-axis of spectral data
    # keep in mind the units you specified for the measurement
    # here the measurement was made using the eV as the x-axis
energy = reader.xdata

# get the spectral data from the map; has form (y_pixel, x_pixel, intensity)
spectra = reader.spectra

'''
this cell acesses a wavenumber, raman shift, or energy of interest
and plots its intensity as a funciton of x and y
'''
# specify the x-axis value you wish to plot
    # here the CdTe bandgap is 1.51 at room temperature (Fonthal, 1999)
Eg_CdTe = 1.51
# find the value in the x-axis that is closest to the specified x-axis value
E_idx = (np.abs(energy - Eg_CdTe)).argmin()

# get relative positions of the x and y motors
map_x = reader.xpos
map_y = reader.ypos
# specificy the bounds of the area that was measured
bounds_map = [0, map_x.max() - map_x.min(), map_y.max() - map_y.min(), 0]
PL_map = spectra[:,:,E_idx]
plt.imshow(PL_map, extent=bounds_map)