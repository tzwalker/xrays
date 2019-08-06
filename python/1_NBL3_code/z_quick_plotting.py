import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

samp = NBL3_2
scan_i = 3     # --> index of scan 
x_variable = 1 # --> 0:XBIC 1:Cu 2:Cd
y_variable = 0 # --> 0:XBIC 1:Cu 2:Cd
#z_variable = 2

test_models = samp['c_kmodels'][scan_i] # --> XBIC, Cu, and Cd arrays for scan422
labels = test_models.labels_
test_data = samp['c_redStand_arrs'][scan_i]
x = test_data[:, x_variable]
y = test_data[:, y_variable]
#z = test_data[:, z_variable]

#fig, (ax1, ax2) = plt.subplots(1, 2)
#fig.suptitle('Scatter and Map '+ samp['Name'] + ' ' + str(samp['XBIC_scans'][scan_i]))

fig, ax0 = plt.subplots()
ax0 = plt.scatter(x, y, c = labels)
plt.title(samp['Name'] + ' scan ' + str(samp['XBIC_scans'][scan_i]))

fig, ax1 = plt.subplots()
ax1 = sns.distplot(x)
plt.title(samp['Name'] + ' scan ' + str(samp['XBIC_scans'][scan_i]))

fig, ax3 = plt.subplots()
ax3 = plt.imshow(samp['elXBIC_corr'][scan_i][x_variable-1], cmap=plt.get_cmap('hot'), origin = 'lower')
plt.title(samp['Name'] + ' ' + str(samp['XBIC_scans'][scan_i]))