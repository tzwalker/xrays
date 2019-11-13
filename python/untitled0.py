# -*- coding: utf-8 -*-
"""
Trumann
Mon Nov 11 12:02:21 2019
"""

path = r'Z:\Trumann\XRF images\py_exports_bulk\TS58A_scan439_txt_images'
fgb = r'\possible_baseline_gbs2.txt'
fcurr = r'\Composite-0001.txt'; fcu = r'\Composite-0002.txt'
fcd = r'\Composite-0002.txt'; fte = r'\Composite-0003.txt'

import numpy as np
gbs = np.loadtxt(path+fgb)
gb_idxs = np.where(gbs!=0)

import matplotlib.pyplot as plt

xbic = TS58A['XBIC_corr'][3][0,:,:-2]
cu = TS58A['XBIC_corr'][3][1,:,:-2]

avg_xbic = np.mean(xbic)
avg_xbic_masked = np.mean(xbic[np.where(gbs!=0)])

x_cu = np.loadtxt(path+fcu)
y_curr = np.loadtxt(path+fcurr)

x = x_cu[gb_idxs]
y = y_curr[gb_idxs]

import seaborn as sns
sns.jointplot(x, y, kind='hex')

#plt.imshow(cu)
