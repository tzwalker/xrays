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

# compute delta XBIV maps
dels = [X - Y for X, Y in zip(imgs[1:], imgs[0:])]

# =============================================================================
# # plot delta XBIV maps quickly
# for D in dels:
#     plt.figure()
#     plt.imshow(D, cmap='RdYlGn')
# =============================================================================

'''Se distirbutions and/or maps and/or histograms'''
# import Se maps
Se_maps = []
for S in scans1:
    FNAME = r'\FS3_scan{SCN}_Se.csv'.format(SCN=S)
    IMG = np.genfromtxt(PATH_IN+FNAME, delimiter=',')
    Se_maps.append(IMG)

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
np.savetxt(PATH_OUT+FNAME, Se_hist_out, delimiter=',')
#%%
'''
retrieving and plotting percentile masks overtime
histograms of good and bad areas
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
np.savetxt(PATH_OUT+FNAME, lo_XBIV_arr, delimiter=',')
FNAME = r'\arrays_for_hist_hiXBIVvTemp.csv'
np.savetxt(PATH_OUT+FNAME, hi_XBIV_arr, delimiter=',')

Se_hiXBIV = Se_maps[TempAndMap_IDX]*mask
Se_loXBIV = Se_maps[TempAndMap_IDX]*mask

Se_hiXBIV_c = Se_hiXBIV.copy()
Se_hiXBIV_c[Se_hiXBIV_c == 0] = np.nan

Se_loXBIV_c = Se_loXBIV.copy()
Se_loXBIV_c[Se_loXBIV_c == 0] = np.nan

plt.hist(Se_loXBIV_c.ravel(), bins=50,histtype='step')
plt.hist(Se_hiXBIV_c.ravel(), bins=50,histtype='step')
plt.xlim([0.5,1.5])
plt.ylim([0,600])






