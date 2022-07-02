"""
coding: utf-8

tzwalker
Wed Feb  3 10:07:35 2021

for complete single spectrum example, see single spectrum code in
'Z:\BertoniLab\Lab\Setups and data\Renishaw\pyCode to read wdfs'
"""

from renishawWiRE import WDFReader
import matplotlib.pyplot as plt
import numpy as np


IN_PATH = r'Z:\Trumann\Renishaw\20210304 PVSe33'
FNAME = r'\PVSe33.4_3 Au side PL spectrum0.wdf'

# import wdf file
filename = IN_PATH+FNAME
reader = WDFReader(filename)
reader.print_info()

# get x-axis of spectral data
    # keep in mind the units you specified for the measurement
    # here the measurement was made using the eV as the x-axis
energy = reader.xdata

# get the spectral data from the map; has form (y_pixel, x_pixel, intensity)
spectra = reader.spectra

plt.plot(energy, spectra)
plt.xlabel('Energy (eV)')
plt.ylabel('Intensity (.)')

OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\PL\spectra'
OUT_NAME = r'\20210213 PVSe33 redo 2 - PVSe33.3_2 Au Side_PL_spot03.csv'
OUT = OUT_PATH + OUT_NAME
out_data = np.vstack([energy,spectra]).T
#np.savetxt(OUT, out_data, delimiter=',')


