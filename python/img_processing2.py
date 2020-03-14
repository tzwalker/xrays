'''
20200313
generate scatter plot and slopes for a set of two variables
to get bar graph seen in PVSC Fig. 3
i manully entered the slope output from this program into Origin
'''
import numpy as np
from standardize_map import standardize_map
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# abstract #
def check_mask(map_from_a_scan, mask__of_scan):
    plt.imshow(map_from_a_scan)
    plt.imshow(mask_plot, cmap='Greys')
    return
SAMP = NBL33
SAMP_NAME = 'NBL33'
SCAN_IDX = 6
SCAN_NUM = str(SAMP.scans[SCAN_IDX])

SYS_PATH = r'Z:\Trumann\XRF images\py_exports_interface'
# change mask: "bound_0in_1out_mask" | "cores_0in_mask"
MASK_PATH = r'\{sam}\scan{scn}\cores_0in_mask.txt'.format(sam=SAMP_NAME, 
               scn=SCAN_NUM)
FULL_PATH = SYS_PATH + MASK_PATH
mask = np.loadtxt(FULL_PATH)

# fitted images #
X = SAMP.maps[SCAN_IDX][1,:,:-2]
Y = SAMP.maps[SCAN_IDX][2,:,:-2]

# to plot transparent mask
mask_plot = np.ma.masked_where(mask == 0, mask) 
check_mask(X, mask_plot)

# standardized maps #
X1 = standardize_map(X)
Y1 = standardize_map(Y)

# standardized data points in the mask pixels
Xmask=X1[np.where(mask!=0)]
Ymask=Y1[np.where(mask!=0)]

# prep for fitting #
x=Xmask.ravel().reshape(-1,1)
y=Ymask.ravel().reshape(-1,1)

MODELR = LinearRegression()
FITTING = MODELR.fit(x, y)
ypred = FITTING.predict(x)

#output fit slope
print(FITTING.coef_[0][0], FITTING.intercept_[0])
#output slope error
print(np.sqrt(mean_squared_error(x,y)))

#%%
### make scatter plot ###
# consider output the arrays to csv to plot in Origin

# to get better dashed line fit #
a = np.concatenate((x,y), axis=1)
a = np.array(sorted(a, key=lambda x:x[0]))
fit = np.polyfit(a[:,0], a[:,1], 1)
fit_sort = [i*fit[0] + fit[1] for i in a[:,0]]

fig, ax = plt.subplots(figsize=(5,5))
#ax.hexbin(x,y,mincnt=1,cmap='Greys',gridsize=(50,20))
ax.plot(a[:,0], fit_sort, 'k-', dashes=[5,5], linewidth=3)
ax.scatter(x,y,s=3, color='gray')

# nice plot with regression line #
plt.axis('square')
plt.xlim([-3,3]); plt.ylim([-3,3])
ax.tick_params(axis='both', direction='in', which='major', labelsize=14, length=7, width=1)
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')  
plt.xlabel('Stand. Copper (a.u.)', fontsize=18)
plt.ylabel('Stand. XBIC (a.u.)', fontsize=18)