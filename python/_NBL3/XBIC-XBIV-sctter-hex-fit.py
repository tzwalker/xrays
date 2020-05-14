"""
coding: utf-8

tzwalker
Wed May 13 16:28:24 2020

for XBIC XBIV correlations after alignment (using translations_and...maps.py)
fit the data and plot using histograms in the margins

make XBIV the y value and img0, make xbic the x value and img1
"""
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

x = Y.ravel()
y = X.ravel()

x = x.reshape(-1,1)
y = y.reshape(-1,1)

#scaler = StandardScaler()
#x = scaler.fit_transform(xshaped)
#y=scaler.fit_transform(yshaped)

# manual regression #
MODELR = LinearRegression()
model = MODELR.fit(x, y)
ypred = model.predict(x)

# setup histograms in margins #
fig = plt.figure(figsize=(5,5))
grid = plt.GridSpec(4, 4, hspace=0.2, wspace=0.2)
main_ax = fig.add_subplot(grid[-3:, :-1])
x_hist = fig.add_subplot(grid[0, :-1], xticklabels=[], xticks=[])
y_hist = fig.add_subplot(grid[-3:, 3], yticklabels=[], yticks=[])


# plot #
#main_ax.hexbin(x,y, mincnt=1, cmap='Greys', gridsize=(50,20))
main_ax.scatter(x,y,s=1, c='#808080')
main_ax.plot(x, ypred, color='red', linestyle='--', linewidth=1)
main_ax.set_xlim([np.min(x), np.max(x)])
main_ax.set_ylim([np.min(y), np.max(y)])

x_hist.hist(x, 40, orientation='vertical', color='gray')
y_hist.hist(y, 40, orientation='horizontal', color='gray')

slope = model.coef_[0][0]
intercept= model.intercept_[0]
r2 = model.score(x,y)

stats = np.array((slope,intercept,r2)).reshape(1,3)
print("m={:.2e},\nb={:.2e},\nr2={:.3f}".format(slope,intercept,r2))
