# -*- coding: utf-8 -*-
"""
Trumann
Wed Jan 29 13:34:11 2020

segmentation for XBIC maps as a function of temperature
Sample FS3_3: 2019_06_2IDD
XBIC
20C: scan0323
40C: scan0327
60C: scan0332
80C: scan0344
100C: scan344

use to plot nice maps from ASCII data exported from MAPS
enter scan path and number
define channel in function
define colormap of plot
"""
import plot_FS_defs as PLT


four_img = r'C:\Users\Trumann\Desktop\FS_data\FS3_2019_06_2IDD_stage\output\combined_ASCII_2idd_0344.h5.csv'
PLT.plot_nice2d_from_ascii(four_img, 'us_ic', 'magma')