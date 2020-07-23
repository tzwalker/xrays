"""
coding: utf-8

tzwalker
Tue Jul  7 17:05:57 2020

this program is meant for analyses of the aligned
XBIV scans produced using 
'_first_solar/XBIC-XBIV-translate-and-deltas.py'

before serious correlations are preformed, the XRF data should be
corrected for absorption
XBIC
20C: scan0323
40C: scan0327
60C: scan0332
80C: scan0339
100C: scan344

XBIV
20C: scan0321
40C: scan0325
60C: scan0330
80C: scan0337
100C: scan0342

"""
import numpy as np
import matplotlib.pyplot as plt

# specificy path to csvs
PATH_IN = r'C:\Users\triton\Dropbox (ASU)\1_FS_operando\XBIC_XBIV aligned image csvs'
scans = [321,325,330,337,342]
scans1 = [str(s) for s in scans]

# import XBIV maps
imgs = []
for S in scans1:
    FNAME = r'\FS3_scan{SCN}_XBIV.csv'.format(SCN=S)
    IMG = np.genfromtxt(PATH_IN+FNAME, delimiter=',')
    imgs.append(IMG)

# import Se maps
Se_maps = []
for S in scans1:
    FNAME = r'\FS3_scan{SCN}_Se.csv'.format(SCN=S)
    IMG = np.genfromtxt(PATH_IN+FNAME, delimiter=',')
    Se_maps.append(IMG)

# compute delta XBIV maps
dels = [X - Y for X, Y in zip(imgs[1:], imgs[0:])]
dels1 = [(X/np.median(X)) / (Y/np.median(Y)) for X,Y in zip(imgs[1:], imgs[0:])]


#%%
'''Se distirbutions and/or maps and/or histograms'''

# plot Se histograms over a temperature range
labels = ['25','40','60','80','100']
colors = ['k', 'b', 'g', 'r','c']
Se_hist = []
for i,m in enumerate(Se_maps):
    DATA = m.ravel()
    Se_hist.append(DATA)
    print(np.median(DATA))
    pt_75 = np.percentile(DATA,75)
    pt_25 = np.percentile(DATA,25)
    err = pt_75 - pt_25
    print(err)
    print()
    #plt.figure()
    #plt.hist(DATA, bins=50,histtype='step', color=colors[i], label=labels[i])
    #plt.legend(prop={'size': 10})
    #plt.xlim([0.5,1.5])
    #plt.ylim([0,3000])
Se_hist_out = np.array(Se_hist)
Se_hist_out = Se_hist_out.T
PATH_OUT = r'C:\Users\triton\Dropbox (ASU)\1_FS_operando'
FNAME = r'\SevTemp_arrays_for_hist.csv'
#np.savetxt(PATH_OUT+FNAME, Se_hist_out, delimiter=',')
#%%
'''
retrieving percentile masks over temp
and plotting histograms of good and bad areas
'''
# get 20th and 80th percentiles of XBIV at 25C
thres_lo = np.percentile(imgs[0], 20)
thres_hi = np.percentile(imgs[0], 80)

# make integer mask
mask_lo = imgs[0]<=thres_lo
mask_hi = imgs[0]>=thres_hi
mask_lo = mask_lo.astype(int)
mask_hi = mask_hi.astype(int)


# apply mask to an image (use 'Se_maps' or 'imgs')
XBIV_lo = [m*mask_lo for m in imgs]
XBIV_hi = [m*mask_hi for m in imgs]

# find distributions of 20th percentile and 80th percentile XBIV
lo_XBIV_arr = []
for m in XBIV_lo:
    m_copy = m[np.where(m!=0)]
    lo_XBIV_arr.append(m_copy)
    #plt.hist(m_copy.ravel(), bins=50,histtype='step')
lo_XBIV_arr = np.array(lo_XBIV_arr)
lo_XBIV_arr = lo_XBIV_arr.T

hi_XBIV_arr = []
for m in XBIV_hi:
    m_copy = m[np.where(m!=0)]
    hi_XBIV_arr.append(m_copy)
    #plt.hist(m_copy.ravel(), bins=50,histtype='step')
hi_XBIV_arr = np.array(hi_XBIV_arr)
hi_XBIV_arr = hi_XBIV_arr.T

PATH_OUT = r'C:\Users\triton\Dropbox (ASU)\1_FS_operando'
FNAME = r'\arrays_for_hist_loXBIVvTemp.csv'
#np.savetxt(PATH_OUT+FNAME, lo_XBIV_arr, delimiter=',')
FNAME = r'\arrays_for_hist_hiXBIVvTemp.csv'
#np.savetxt(PATH_OUT+FNAME, hi_XBIV_arr, delimiter=',')
#%%
'''2D FFT of XBIV maps'''
DATA = imgs[4]
data_fft = np.fft.fft2(DATA)#, s=None, axes=(-2, -1), norm=None)
# invert, center, then square the transform
data_shft = np.fft.fftshift(data_fft)**2
# take modulus of inverted, centered square
data_abs = np.abs(data_shft)

data_log = np.log(data_abs)
plt.imshow(data_log)
amp = np.real(data_fft)
#https://en.wikipedia.org/wiki/Absolute_value#Complex_numbers
#%%
'''1D FFT of XBIV map'''

data = imgs[0][0,:]#.sum(axis=1) # for summing rows

# compute fast, discrete Fourier transform
fft = np.fft.fft(data)
# compute frequency bins accroding to sample step
n = data.size
um_step = 0.150
freq = np.fft.fftfreq(n, d=um_step)

# without shifting zero freq component to center of spectrum
modulus_noshft = np.abs(fft)

# with shifting zero freq component to center of spectrum
modulus_shft = np.abs(np.fft.fftshift(fft))

# freq vs. noshft <--> shft plot (with discontinuity)
# freq vs. shft <--> noshft plot (with discontinuity)

# make freq vs. noshft array
# get only one half of mirror
freq1 = freq[0:int(n/2)].reshape(-1,1)
mod = modulus_noshft[0:int(n/2)].reshape(-1,1)

# freq1 vs. mod will give a plot that has the same spatial coordinates
# as what is seen in Michael's paper

# invert, center, then square the transform
data_shft = np.fft.fftshift(data_fft)**2
# take modulus of inverted, centered square
data_abs = np.abs(data_shft)
data_log = np.log(data_abs)

ax0.plot(row)
ax0.set_xlim([0,np.size(row)])

ax1.plot(data_log)
#ax1.set_ylim([-10,10])


