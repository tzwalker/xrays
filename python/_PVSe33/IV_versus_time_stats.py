"""
coding: utf-8

tzwalker
Mon Aug  2 13:11:03 2021

this program is meant to open and retrieve IV parameters
from raw .txt files shared by NREL (EColegrove)

the objective is to get the IV parameters for each cell of a minimodule
over a 500hr period of aging

the sample set is PVSe33; the minimodule is PVSe33.4

essentially, there are four cells, and each cell has a timestamp from 0hr
to 500hr


"""


import pandas as pd
import numpy as np

# import file
PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\IV data - vs time'

cells = ['1', '2', '3', '4']
timestamps = ['0', '0.5hr', '1.5hr', '3hr', '6hr',
              '22hr', '44.5hr', '87hr', '158hr', '254hr',
              '350hr', '500hr']

majorIV_time = []
majorIV_err_time = []
minorIV_time = []
minorIV_err_time = []
for timestamp in timestamps:
    # initialize list to hold IV params at a given timestamp
    majorIV = []
    minorIV = []
    for cell in cells:
        FILE = r'\PVSe33.4_{c}_{s}.txt'.format(c=cell, s=timestamp)
        F = PATH+FILE
        
        rows_to_keep = list(range(4,14))
        
        data = pd.read_csv(F, delimiter='\t', skiprows = lambda x: x not in rows_to_keep)
        
        # split data into two data frames
            # data1 is major IV params (e.g., Voc, Jsc, Vmpp, Jmpp)
            # data2 is minoir IV params (e.g., Rseries, Rshunt)
            # the indices also remove the rows containign zeros
        data1 = data.iloc[:1, :]
        data2 = data.iloc[4:5, :-2]
        # rename data columns in 2nd dataset, for convenient reference
        data2.rename(columns=data.iloc[3], inplace = True)
        
        # convert column values from strings to float
        Data1 = data1.astype(np.float)
        Data2 = data2.astype(np.float)
        
        # access major IV parameters
        Voc = Data1.loc[0]['Voc (mV) ']
        Jsc = Data1.loc[0]['Raw Jsc (mA/cm^2) ']
        FillF = Data1.loc[0]['Meas. FF']
        Eff = Data1.loc[0]['One Sun Efficiency (%) ']
        array_majorIV = np.array([Voc, Jsc, FillF, Eff])
        # record params of cell
        majorIV.append(array_majorIV)

        
        # access minor IV parameters
        Vmpp = Data1.loc[0]['Vmpp (mV)']
        Jmpp = Data1.loc[0]['Jmpp (mA/cm2)']
        Rseries = Data2.loc[4]['R@Voc (Light)']
        Rshunt = Data2.loc[4]['R@Jsc (Light)']
        array_minorIV = np.array([Vmpp, Jmpp, Rseries, Rshunt])
        # record parms of cell
        minorIV.append(array_minorIV)
    
    # store values of all four cells at a given timestamp
    avg_majorIV_arr = np.array(majorIV)
    avg_minorIV_arr = np.array(minorIV)
    
    # calculate statistics over all four cells
    avg_majorIV = np.mean(majorIV, axis = 0)
    std_majorIV = np.std(majorIV, axis = 0)
    
    avg_minorIV = np.mean(minorIV, axis = 0)
    std_minorIV = np.std(minorIV, axis = 0)
    
    # record statistics of majorIV params
    majorIV_time.append(avg_majorIV)
    majorIV_err_time.append(std_majorIV)
    # record statistics of majorIV params
    minorIV_time.append(avg_minorIV)
    minorIV_err_time.append(std_minorIV)

# convert avg and std at each timestamp to numpy array
A = np.array(majorIV_time)
B = np.array(majorIV_err_time)

C = np.array(minorIV_time)
D = np.array(minorIV_err_time)

# alternate mean and std arrays so they have proper format
    # copy "a" and "b" into Origin
a = np.stack((A,B),2).reshape(A.shape[0],-1)

b = np.stack((C,D),2).reshape(C.shape[0],-1)
