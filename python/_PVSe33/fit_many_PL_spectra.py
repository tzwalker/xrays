# -*- coding: utf-8 -*-
"""
Trumann
Tue Feb 16 07:41:12 2021

this program imports a PL map from a wdf file
fits and substracts a baseline from the spectrum in each pixel
fits the baseline-subtracted spectrum to a gaussian function
and plots the peak position or peak amplitude of the gaussian fit
as a function of X-Y position

a custom module, 'baseline_algorithms', is needed for the baseline subtraction
"""

import sys
DEF_PATH = r'C:\Users\Trumann\xrays\python'
sys.path.append(DEF_PATH)

from renishawWiRE import WDFReader
import matplotlib.pyplot as plt
#import numpy as np
from baseline_algorithms import arpls


IN_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\PL'
FNAME = r'\20210213 PVSe33 redo 2 - PVSe33.3_2 Au Side_PL_map0.wdf'

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

# get spectrum from single pixel
spec0 = spectra[10,9,:]
plt.plot(spec0, label='spec0')

baseline_arpls = arpls(spec0, 1e6, 0.001)
intensity_arpls = spec0 - baseline_arpls
plt.plot(intensity_arpls, label='arpls')

plt.legend()
