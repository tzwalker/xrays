"""
coding: utf-8

tzwalker
Tue Nov  3 20:47:58 2020

calculating absorption through soda lime glass

sigma (i.e. capture cross section) seen here is calculated from 
"Soda Lime Glass Absorption Estimate.xlsx""

see that file for details on the calculation
"""
import numpy as np

rho = 2.53          #g/cm3
sigma = 11.24126622 #cm2/g

mu = rho*sigma

depth = np.linspace(0,0.3,301) # 10um steps

iio = np.exp(-mu*depth)

import matplotlib.pyplot as plt
depth_in_mm = depth*10
plt.figure()
plt.plot(depth_in_mm, iio)
