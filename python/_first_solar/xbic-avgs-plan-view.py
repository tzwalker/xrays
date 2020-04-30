"""
coding: utf-8

tzwalker
Sun Apr 19 18:21:43 2020

this is file is meant for various tasks that are part of processing
the XBIV/C vs Temp data of the FS3 2019_06_2IDD
see docstring of each sub-script for purpose
"""

"""parsing,reading,andextracting SIFT translation from ImageJ"""
import xml.etree.ElementTree as ET
XML_PATH = r'C:\Users\triton\FS3_2019_06_operando\for_imageJ\output'
XML_FILE = r'\scan325_XBIV.xml'
XML = XML_PATH + XML_FILE

doc = ET.parse(XML)
root = doc.getroot()

# get xy translation from XML file exported
# using ImageJ plugin Register Virtual Stack Slices
print(root[0].attrib['data']) 


        
# =============================================================================
# # note: voltage is primarily affected by temperature, not current
#     # for DoE report, want to plot voltage histogram of same area from 25-100C
# """export plan-view maps as arrays for histograms in OriginLab"""
# import numpy as np
# 
# eh_maps = [scan[0,:,:-2] for scan in FS3.maps]
# eh_arr = [array.ravel() for array in eh_maps]
# arrs = np.array(eh_arr).T
# fname = r"\XBIVvTemp_scans321_325_330_337_342_hist.csv"
# path = r'C:\Users\triton\FS3_2019_06_operando'
# out = path + fname
# np.savetxt(out, arrs, delimiter=",")
# 
# =============================================================================
# =============================================================================
# """checking normal stats of xbic maps"""
# #xbic_maxs = [np.max(array[0,:,:-2]) for array in xbicscans]
# xbic_avgs = [np.mean(array) for array in xbic_maps]
# #maxes = np.array(xbic_maxs)
# avgs = np.array(xbic_avgs)
# p = [25,50,75] # percentiles
# xbic_percentiles = [np.percentile(array, p) for array in xbic_maps]
# percentiles = np.array(xbic_percentiles)
# #merge = np.concatenate((maxes.reshape(-1,1),avgs.reshape(-1,1)), axis=1)
# # see ppt notes for maxes and mins of XBIC for same area from 25-100C
# =============================================================================





