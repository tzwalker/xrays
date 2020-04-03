import standardize_map as sm
import background_subtraction as bs
from scipy.ndimage import gaussian_filter as gf
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

i = NBL33.scan258[3,:,:-2]
v = NBL33.scan261[3,:,:-2]
#%%
istand = sm.standardize_map(i)
vstand = sm.standardize_map(v)

i0 = bs.background_subtraction(istand,25)
v0 = bs.background_subtraction(vstand,25)

i1 = gf(i0,sigma=1)
v1 = gf(v0,sigma=1)


# simple linear regression
x = istand.ravel().reshape(-1,1)
y = vstand.ravel().reshape(-1,1)
MODELR = LinearRegression()
model = MODELR.fit(x, y)
ypred = model.predict(x)

# plot images 
fig, (ax0,ax1) = plt.subplots(1,2)
plt.tight_layout(w_pad=-2)
sns.heatmap(i1, square=True, ax=ax1,cbar=False,cmap='Purples_r')
ax1.invert_yaxis()
ax1.set_axis_off()

sns.heatmap(v1, square=True, ax=ax0, cbar=False, cmap='Purples_r')
ax0.invert_yaxis()
ax0.set_axis_off()

# =============================================================================
# # plot with histogram margins #
# # Set up the axes with gridspec
# fig = plt.figure(figsize=(5,5))
# grid = plt.GridSpec(4, 4, hspace=0.2, wspace=0.2)
# main_ax = fig.add_subplot(grid[-3:, :-1])
# x_hist = fig.add_subplot(grid[0, :-1], xticklabels=[], xticks=[])
# y_hist = fig.add_subplot(grid[-3:, 3], yticklabels=[], yticks=[])
# # main plot axis
# #main_ax.hexbin(x,y, mincnt=1, cmap='Greys', gridsize=(50,20))
# main_ax.scatter(x,y,s=2, c='#808080')
# main_ax.plot(x, ypred, color='#FF0000', linestyle='--', linewidth=2)
# main_ax.set_xlim([np.min(x), np.max(x)])
# main_ax.set_ylim([np.min(y), np.max(y)])
# 
# x_hist.hist(x, 40, orientation='vertical', color='gray')
# y_hist.hist(y, 40, orientation='horizontal', color='gray')
# print(model.coef_[0][0], model.intercept_[0])
# =============================================================================

