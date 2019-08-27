# -*- coding: utf-8 -*-
"""
kineticcross
Mon Aug 26 17:49:23 2019
"""
import numpy as np
import matplotlib.pyplot as plt
#from z_stand_arr import from_stand_to_stand_map

xbic_map =  NBL3_3['c_stand_arrs'][0][:,0]
cu_map =    NBL3_3['c_stand_arrs'][0][:,1]

wanted_indices = np.where(xbic_map > 2)

thres_cu_map = cu_map[wanted_indices]

thres_xbic_map = xbic_map[wanted_indices]

plt.figure()
data = [thres_cu_map, thres_xbic_map]
plt.boxplot(data)
#plt.boxplot(cu_map.reshape(-1,1))
