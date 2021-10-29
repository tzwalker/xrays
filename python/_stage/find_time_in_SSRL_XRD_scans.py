"""
coding: utf-8

tzwalker
Thu Oct 28 15:54:07 2021

this script is meant to return the scan containing a 
time (s) closest to the time (s) specified by the user

meant to be used with data from 2021_10_BL2-1 beamtime
"Z:\BertoniLab\Synchrotron Data\2021_10_BL2-1\raw_data"


helps identify the scan index that needs to
have its detector images integrated

the whole point is to get a diffraction pattern and accurately assign 
to that diffraction pattern a time at 80C 

the sample temperature reach 80+/-5C at Timer column value = 7077 seconds, see:
"Z:\BertoniLab\Synchrotron Data\2021_10_BL2-1\raw_data\CSET82p3_80C_2_scan12.csv"
    this means (1) the scan index range shouldn't be below 12 if i want
    to search for when the sample was at 80C and (2) the time variable in this
    program needs to have 7077 seconds added to it
"""

import pandas as pd

def find_time(path,scan_range,user_time):
    for scan_idx in scan_idxs:
        FNAME = r"\CSET82p3_80C_2_scan{s}.csv".format(s=str(scan_idx))
        DATA_str = DATA_PATH+FNAME
        data = pd.read_csv(DATA_str,skiprows=0)
        array = data["    Timer"].values
        if array[0] < time_s < array[-1]:
            print('time is in '+ FNAME)
            break
        else:
            print('skipped '+ FNAME)
    return

# define time you want to search for
time = 0.50 # hours
time_s = time*60*60+7077 # seconds, units of data dile
    # 7077 factor is time of start of experiment

# define path to metadata files
DATA_PATH = r"Z:\BertoniLab\Synchrotron Data\2021_10_BL2-1\raw_data"

# define scan range you want to search through
scan_idxs = list(range(12,500,1))

find_time(DATA_PATH,scan_idxs,time)

# after running several iterations, i found:
    # 15min @ 80C in "\CSET82p3_80C_2_scan15.csv"
    # 30min @ 80C in "\CSET82p3_80C_2_scan20.csv"