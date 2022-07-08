# -*- coding: utf-8 -*-
"""

Trumann
Wed Jul  6 18:06:31 2022

this program gets the Cu line profiles exported from MAPS
and formats them into a data array that is easily imported into Origin

"""

import pandas as pd
import numpy as np

ASCII_PATH =  r'C:\Users\Trumann\Dropbox (ASU)\2_insitu_Cu_cross_section\output' 

#scans = [240,245,256,272,280,300,318,342,354] # y181.7
#scans = [243,248,258,276,284,304,322,346,358] # y190.2

#scans = [368,380,392,404,429,459,489,525] # y181.7 after bias
scans = [372,384,396,408,433,463,493,529] # y190.2 after bias

xrf = []
for scan in scans:
    scn = str(scan)
    file = r'\line2idd_0{s}.h5.csv'.format(s=scn)
    file = ASCII_PATH+file
    df = pd.read_csv(file, usecols = [1,6])
    arr = np.array(df)
    xrf.append(arr[:,1])
xrf = np.array(xrf)

energy = arr[:,0].reshape(1,-1)
energy = energy*1000

merge = np.concatenate((energy, xrf), 0)
merge = merge.T

out = r'C:\Users\Trumann\Dropbox (ASU)\2_insitu_Cu_cross_section\XANES_at_y190.2_afterbias.csv'
np.savetxt(out, merge, delimiter=',')

scan_names_for_origin = np.array(scans).reshape(1,-1)



