# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 09:18:57 2018

@author: Trumann

This script will import the scans of interest from the raw data directories (hopefully). 

PLEASE READ:
  
  Make sure all destination and source directories have read/write permissions enabled.
  
  Make sure your directories are correct. Network directories must have full network path, not the
    'mapped' drive letter Windows or the native OS assigns to the network drive; e.g. \\server\server
    
    folders must already exist in the destination
    
  Scan position must match point position in the scans/points list!!!
  
"""

import shutil

#enter scans you want and corrosponding points in the scan IN SAME ORDER
scans = ['333', '334', '335','336','337','338','339','340','341','342','343','344']
points = [121, 121, 101, 101, 101, 101, 101, 101, 101, 101, 101, 121]

MDAsource = r'\\en4093310.ecee.dhcp.asu.edu\BertoniLab\Lab\Synchrotron Data\2019_03_2IDD\mda'
MDAdest = r'C:\Users\Trumann\Desktop\2019_03_2IDD_BIAS\mda'

H5source = r'\\en4093310.ecee.dhcp.asu.edu\BertoniLab\Lab\Synchrotron Data\2018_07_2IDD\img.dat'
H5dest = r'C:\Users\Trumann\Desktop\2019_03_2IDD_BIAS\img.dat'

flysource = r'\\en4093310.ecee.dhcp.asu.edu\BertoniLab\Lab\Synchrotron Data\2019_03_2IDD\flyXRF'
flydest = r'C:\Users\Trumann\Desktop\2019_03_2IDD_BIAS\flyXRF'

for scan in scans:
    findMDA = r"\2idd_0" +scan + ".mda"
    findH5 = r"\2idd_0" + scan + ".h5"
    shutil.copyfile(MDAsource + findMDA, MDAdest + findMDA)
    shutil.copyfile(H5source + findH5, H5dest + findH5)
for scan, point in zip(scans, points):  
  for p in range(point):
    findfly = r"\2idd_0{a}_2iddXMAP__{b}.nc".format(a=scan, b=p)
    shutil.copyfile(flysource + findfly, flydest + findfly)
