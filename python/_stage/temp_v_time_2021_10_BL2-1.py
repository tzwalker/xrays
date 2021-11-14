"""
coding: utf-8

tzwalker
Fri Nov  5 10:58:40 2021

this program get the temperature vs time data from 2021_10_BL2-1 beamrun

for simplicity, the timer values for XRD scans (multiples of 5) are excluded

only the timer values for the IV scans are plotted here

the point is to show the temperature over the whole experiment time
the time of an XRD scan (15min) is insignificant 
compared to the whole experiment time (35hrs)

"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# define path to metadata files
DATA_PATH = r"Z:\BertoniLab\Synchrotron Data\2021_10_BL2-1\raw_data"

# define scan range you want to search through
    # every 5th scan is 141 XRD array...
    # scans in between is 41 IV array
c = np.array(list(range(20,551,1)))
 
# exclude XRD scan indices
scan_idxs = np.delete(c, np.arange(0, c.size, 5))

times = []
temps = []
for scan_idx in scan_idxs:
    FNAME = r"\CSET82p3_80C_2_scan{s}.csv".format(s=str(scan_idx))
    DATA_str = DATA_PATH+FNAME
    data = pd.read_csv(DATA_str,skiprows=0)
    time = data["    Timer"].values # get timer values
    temp = data["    CTEMP"].values # get temperature values
    times.append(time)
    temps.append(temp)
    #print('processing '+ FNAME)

# convert list to array
times_arr = np.array(times)
temps_arr = np.array(temps)

# order the array by time value
times_flat = times_arr.flatten()
temps_flat = temps_arr.flatten()

# convert timer seconds to minutes
times_hr = (times_flat - times_flat[0]) / 3600

# plot data
fig, ax = plt.subplots()
ax.plot(times_hr,temps_flat)

plt.xlabel('Time (hr)')
plt.ylabel('Temperature (\u00B0C)')

OUT_PATH = r"C:\Users\triton\Dropbox (ASU)\0_stage design\supplementary"
FNAME = r"\2021_10_BL2-1_temp_v_time.png"
plt.savefig(OUT_PATH+FNAME, format='png', dpi=300, bbox_inches='tight', pad_inches = 0)
