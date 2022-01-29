"""
coding: utf-8
Trumann
Fri Jan 28 10:59:02 2022
"""
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt(r"C:\Users\Trumann\xrays\python\data.txt")

# threshold image copy (need to copy to avoid overwriting original image)
data1 = data.copy()

bound = np.percentile(data1, 80)
data1[data1<bound] = np.nan
plt.figure()
plt.imshow(data1)

data2 = data.copy()
data2[data2 < bound] = 0
plt.figure()
plt.imshow(data2)

a = np.random.random((101,99))

data1 = a.copy()

bound = np.percentile(data1, 80)
data1[data1<bound] = np.nan
plt.figure()
plt.imshow(data1, interpolation='nearest') # --> answer from StackOverflow
#plt.gca().set_facecolor('black')

data2 = a.copy()
data2[data2 < bound] = 0
plt.figure()
plt.imshow(data2)