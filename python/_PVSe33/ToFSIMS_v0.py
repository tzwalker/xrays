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

data = np.loadtxt(f,skiprows=10)[0:512]

# =============================================================================
# #data = data.reshape((512,512,49))
# 
# dat = data[:,:-1]
# 
# #dat = dat.reshape((512,512,49))
# 
# import pandas as pd
# 
# new = pd.DataFrame(data=data[1:,1:],index=data[1:,0],columns=data[0,1:])
# 
# new1 = pd.pivot(index=, columns, values)
# =============================================================================
