import matplotlib.pyplot as plt
import numpy as np
# code used to plot scatter plot figure in PVSC2020 abstract #
def check_mask(switch):
# check mask #
    if switch == 1:
        img = SAMP['XBIC_maps'][SCAN][CHAN,:,:-2]
        plt.imshow(img)
        plt.imshow(mask_plot, cmap='Greys')
    else: pass
    return

SAMP = NBL3_3; SCAN = 0; CHAN=3
#maskpath = r'‪C:\Users\Trumann\cores_0in_mask.txt' #bound_0in_1out_mask,cores_0in_mask
maskpath = r'C:\Users\Trumann\cores_0in_mask.txt'
mask = np.loadtxt(maskpath)
mask_plot = np.ma.masked_where(mask == 0, mask) # to plot transparent mask
check_mask(1)

import sklearn.preprocessing as sklp
scaler = sklp.StandardScaler()
XCHAN = 1; YCHAN = 0
# raw, pix-by-pix correlation #
X = SAMP['XBIC_maps'][SCAN][XCHAN,:,:-2]; Y = SAMP['XBIC_maps'][SCAN][YCHAN,:,:-2]
Xmask = X[np.where(mask!=0)]; Ymask = Y[np.where(mask!=0)]
x = Xmask.ravel().reshape(-1,1); y = Ymask.ravel().reshape(-1,1)
x = scaler.fit_transform(x); y=scaler.fit_transform(y)
# to get better dashed line fit #
a = np.concatenate((x,y), axis=1)
a = np.array(sorted(a, key=lambda x:x[0]))
fit = np.polyfit(a[:,0], a[:,1], 1)
fit_sort = [i*fit[0] + fit[1] for i in a[:,0]]

from sklearn.linear_model import LinearRegression
MODELR = LinearRegression(); FITTING = MODELR.fit(x, y); ypred = FITTING.predict(x)
from sklearn.metrics import mean_squared_error
print(FITTING.coef_[0][0], FITTING.intercept_[0])

#x_ext = np.linspace(-3,3,np.size(x))
#x_ext = x_ext.reshape(-1,1)
#y_ext = FITTING.coef_[0][0]*x_ext+FITTING.intercept_[0]
#y_ext = y_ext.reshape(-1,1)

#%%
fig, ax = plt.subplots(figsize=(5,5))
#ax.hexbin(x,y,mincnt=1,cmap='Greys',gridsize=(50,20))
ax.plot(a[:,0], fit_sort, 'k-', dashes=[5,5], linewidth=3)
ax.scatter(x,y,s=3, color='gray')

# nice simplae hexbin with regression line #
plt.axis('square')
plt.xlim([-3,3]); plt.ylim([-3,3])
ax.tick_params(axis='both', direction='in', which='major', labelsize=14, length=7, width=1)
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')  
plt.xlabel('Stand. Copper (a.u.)', fontsize=18)
plt.ylabel('Stand. XBIC (a.u.)', fontsize=18)

print(np.sqrt(mean_squared_error(x,y)))

