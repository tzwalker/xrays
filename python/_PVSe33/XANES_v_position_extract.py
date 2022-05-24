# -*- coding: utf-8 -*-
"""

Trumann
Tue May 24 09:23:38 2022

this cell holds information for the Se XANES v position scans
done during 2021_07_2IDD - infinite cross section scans

the csvs were exported using ROI and "US_IC" normalization in MAPS
    only Se and us_ic channels were included
    
"""

PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\2021_07_2IDD_SeXRF\output'
FILE = r'\combined_ASCII_2idd_0121.h5.csv' # 0hr - inf
#FILE = r'\combined_ASCII_2idd_0152.h5.csv' # 500hr - inf

F = PATH+FILE

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv(F, sep=',', skiprows=2)
data.columns = ["x_idx", "y_idx", "Energy", "position", "us_ic", "Se_XRF"]


data_dict = data.set_index(['y_idx', 'position']).agg(list, 1).groupby(level=(0)).agg(list).transform(np.array).to_dict()

for position in data_dict.values():
    # access energy and Se intensity
    energy = position[:,1]
    energy = energy * 1000 # units into keV
    xrf = position[:,3]
    # combine energy and XRF array
    # insert debug pause to copy/paste into Origin
    copy_array = np.vstack((energy, xrf)).T
    plt.plot(energy, xrf)

#%%
"""
coding: utf-8

tzwalker
Tue Jan  4 09:29:32 2022

this cell holds information for the Cu XANES v position scans
done during 2021_11_2IDD

the csvs were exported using ROI and "US_IC" normalization in MAPS
    additional channels were included in the export so the columns and indices
    are slightly different than the above cell
"""

PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\2021_11_2IDD_CuXRF\output'
#FILE = r'\combined_ASCII_2idd_1099.h5.csv' # 0hr
#FILE = r'\combined_ASCII_2idd_1100.h5.csv' # 0hr
#FILE = r'\combined_ASCII_2idd_1211.h5.csv' # 500hr
FILE = r'\combined_ASCII_2idd_1212.h5.csv' # 500hr

F = PATH+FILE

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv(F, sep=',', skiprows=2)
data.columns = ["x_idx", "y_idx", "Energy", "position", "us_ic", "Cu_XRF", "s_i", "s_e", "s_a"]


data_dict = data.set_index(['y_idx', 'position']).agg(list, 1).groupby(level=(0)).agg(list).transform(np.array).to_dict()

for position in data_dict.values():
    # access energy and Se intensity
    energy = position[:,1]
    energy = energy * 1000 # units into keV
    xrf = position[:,3]
    # combine energy and XRF array
    # insert debug pause to copy/paste into Origin
    copy_array = np.vstack((energy, xrf)).T
    plt.plot(energy, xrf)
    


#%%
"""
coding: utf-8

tzwalker
Fri Jul 30 13:45:05 2021

this cell holds information for the Se XANES v position scans
done during 2021_07_2IDD - connected window/lamella cross section scans

the csvs were exported using ROI and "1" normalization in MAPS

"""

PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\output'
FILE = r'\combined_ASCII_2idd_0112.h5.csv' # 0hr
#FILE = r'\combined_ASCII_2idd_0145.h5.csv' # 500hr

F = PATH+FILE

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv(F, sep=',', skiprows=2)
data.columns = ["x_idx", "y_idx", "Energy", "position", "Se_XRF"]


data_dict = data.set_index(['y_idx', 'position']).agg(list, 1).groupby(level=(0)).agg(list).transform(np.array).to_dict()

for position in data_dict.values():
    # access energy and Se intensity
    energy = position[:,1]
    energy = energy * 1000 # units into keV
    xrf = position[:,2]
    # combine energy and XRF array
    # insert debug pause to copy/paste into Origin
    copy_array = np.vstack((energy, xrf)).T
    plt.plot(energy, xrf)
