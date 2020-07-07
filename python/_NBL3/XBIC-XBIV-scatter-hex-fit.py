"""
coding: utf-8

tzwalker
Wed May 13 16:28:24 2020

for XBIC XBIV correlations after alignment 
    (aligned using "XBIC-XBIV-translate-and-deltas.py")

fit the data and plot using histograms in the margins

in this file X is the XBIC map and Y is the XBIV map
    -this is the opposite of what is seen in "XBIC-XBIV-translate-and-deltas.py"
    -this is because, when aligning, the XBIV map was used as the reference img
    -for correlations, XBIC was chosen as the reference
"""
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
#from scipy.ndimage import gaussian_filter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
PATH_IN = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\XBIC_XBIV aligned image csvs'
XBIC_FNAME = r'\NBL32_scan416_XBIC.csv'
XBIV_FNAME = r'\NBL32_scan419_XBIV.csv'

# import aligned csvs
#X = pd.read_csv(PATH_IN + XBIC_FNAME)
#Y = pd.read_csv(PATH_IN + XBIV_FNAME)
# for different channels
X = NBL33.scan264[4,:,:-2]
Y = NBL33.scan264[2,:,:-2]
x = X.ravel()
y = Y.ravel()

# for changing pandas df into numpy arr
#x = np.array(X)
#y = np.array(Y)

x = x.reshape(-1,1)
y = y.reshape(-1,1)

#scaler = StandardScaler()
#x = scaler.fit_transform(x)
#y = scaler.fit_transform(y)

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
main_ax.hexbin(x,y, mincnt=1, cmap='inferno', gridsize=(50,20))
#main_ax.scatter(x,y,s=1, c='#808080')
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
