"""
coding: utf-8
Trumann
Thu Feb 17 17:14:25 2022

be sure to run "plot_XRD_as_heatmap_SSRL.py" before this program
run last cell in "XRD_fit_111_peak.py" before this program

this program is used to make a nice plot of peak position vs time

"""

import matplotlib.pyplot as plt

label_size = 14

fig, ax = plt.subplots()

plt.scatter(times, peak_positions, marker='s', color='k')

plt.xlabel('Time (hr)', size=label_size)
ax.xaxis.set_tick_params(labelsize=label_size)
plt.ylabel('2\u03B8 (\u00B0)', size=label_size)
ax.yaxis.set_tick_params(labelsize=label_size)

# i've decided it's probably just better to export to Origin
# copy the "times" and "peak_positions" variable to make the scatter plot

#%%
'''use this cell to plot the fit against the data curve'''

time_idx = [0,4,8,13]

for idx in time_idx:
    plt.figure()
    plt.plot(xData,data_curves[:,idx], label='data: {t}hr'.format(t=times[idx]))
    plt.plot(xData,fit_curves[:,idx], label='Gaussian fit')
    plt.legend()