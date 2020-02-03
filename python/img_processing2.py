import matplotlib.pyplot as plt
import numpy as np

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

a = np.concatenate((x,y), axis=1)
a = np.array(sorted(a, key=lambda x:x[0]))
fit = np.polyfit(a[:,0], a[:,1], 1)
fit_sort = [i*fit[0] + fit[1] for i in a[:,0]]

# =============================================================================
# from sklearn.linear_model import LinearRegression
# MODELR = LinearRegression(); FITTING = MODELR.fit(x, y); ypred = FITTING.predict(x)
# from sklearn.metrics import mean_squared_error
# print(FITTING.coef_[0][0], FITTING.intercept_[0])
# 
# #x_ext = np.linspace(-3,3,np.size(x))
# #x_ext = x_ext.reshape(-1,1)
# #y_ext = FITTING.coef_[0][0]*x_ext+FITTING.intercept_[0]
# #y_ext = y_ext.reshape(-1,1)
# =============================================================================
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

#%%
# NICE HEXBIN PLOT WITH HISTOGRAMS: SETUP #
# overlay simple linear regression line #
fig = plt.figure(figsize=(5,5))
grid = plt.GridSpec(4, 4, hspace=0.2, wspace=0.2)
main_ax = fig.add_subplot(grid[-3:, :-1])
x_hist = fig.add_subplot(grid[0, :-1], xticklabels=[], xticks=[])
y_hist = fig.add_subplot(grid[-3:, 3], yticklabels=[], yticks=[])
# plot #
main_ax.hexbin(x,y, mincnt=1, cmap='Greys', gridsize=(50,20))
#main_ax.scatter(x,y,s=2, c='#808080')
main_ax.plot(x, ypred, color='#0f0f0f', linestyle='--', linewidth=3)
main_ax.set_xlim([np.min(x), np.max(x)])
main_ax.set_ylim([np.min(y), np.max(y)])
x_hist.hist(x, 40, orientation='vertical', color='gray')
y_hist.hist(y, 40, orientation='horizontal', color='gray')
TXT_PLACE = [-1,2]
TXT_PLACE = [0,2]
main_ax.text(TXT_PLACE[0], TXT_PLACE[1], "m={0:.3g}, b={1:.3g}".format(
        FITTING.coef_[0][0], FITTING.intercept_[0]))
