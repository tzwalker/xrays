# -*- coding: utf-8 -*-
"""

Trumann
Thu Mar 31 20:17:36 2022


this program opens ToF SIMS ASCIIs from Steve Harvey (NREL)

data were taken from shared Box folder; downloaded to

Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS

"""

import numpy as np

f = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\33.3.2_tomog_ (7) - Cl-.txt"

data = np.loadtxt(f)
indices = data[:,0:3].copy().astype('int')
values = data[:,3].copy()

res = np.zeros((49,512,512),float)

res[indices[:,2],indices[:,0],indices[:,1]] = values

import matplotlib.pyplot as plt

slices = [0,10,20,30,40]
for s in slices:
    image = res[s,:,:]
    plt.figure()
    plt.imshow(image)

