"""
coding: utf-8
Trumann
Thu Feb 17 15:51:36 2022

this program is for post analysis of data from 2021_10_BL21
Z:\BertoniLab\Synchrotron Data\2021_10_BL2-1\raw_data\CSET82p3_80C_2_scan
Z:\BertoniLab\Synchrotron Data\2021_10_BL2-1\raw_data\CSET82p3_roomtemp_final_xrd_scan1.xye

be sure to run "plot_XRD_as_heatmap_SSRL.py" before this program

it is meant to fit the (111) peak position using the data in variable "z"

see references
https://stackoverflow.com/questions/52502896/how-can-i-fit-a-good-lorentzian-on-python-using-scipy-optimize-curve-fit

http://emilygraceripka.com/blog/16

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq, curve_fit

z1 = z.copy()
# get diffraction pattern
y = z1[:,13]

# zoom in on (111) peak
# this range was found by plotting intensity versus index
# manually finding the indices for the peak
# then accessing the "theta_arr" variable using those indices
#plt.plot(theta_arr[1100:1150],y[1100:1150])

xData = theta_arr.copy()
xData = xData[1100:1150]

yData = z1[1100:1150,0]
yData = yData / max(yData)

#%%
'''this cell was used for testing different functions'''
def lorentzian( x, x0, a, gam ):
    return a * gam**2 / ( gam**2 + ( x - x0 )**2)

def multi_lorentz( x, params ):
    off = params[0]
    paramsRest = params[1:]
    assert not ( len( paramsRest ) % 3 )
    return off + sum( [ lorentzian( x, *paramsRest[ i : i+3 ] ) for i in range( 0, len( paramsRest ), 3 ) ] )

def res_multi_lorentz( params, xData, yData ):
    diff = [ multi_lorentz( x, params ) - y for x, y in zip( xData, yData ) ]
    return diff

generalWidth = 1

yDataLoc = yData
startValues = [ max( yData ) ]
counter = 0

while max( yDataLoc ) - min( yDataLoc ) > .1:
    counter += 1
    if counter > 10: ### max 20 peak...emergency break to avoid infinite loop
        break
    minP = np.argmin( yDataLoc )
    minY = yData[ minP ]
    x0 = xData[ minP ]
    startValues += [ x0, minY - max( yDataLoc ), generalWidth ]
    
    popt, ier = leastsq( res_multi_lorentz, startValues, args=( xData, yData ) )
    yDataLoc = [ y - multi_lorentz( x, popt ) for x,y in zip( xData, yData ) ]

testData = [ multi_lorentz(x, popt ) for x in xData ]

fig = plt.figure()
ax = fig.add_subplot( 1, 1, 1 )
ax.plot( xData, yData )
ax.plot( xData, testData )
plt.show()



def _3Lorentzian(x, amp1, cen1, wid1):
    return (amp1*wid1**2/((x-cen1)**2+wid1**2))

def _1gaussian(x, amp, x0, sig):
    return amp / (sig * np.sqrt(2 * np.pi)) * np.exp(-(x-x0)**2 / (2*sig**2))

amp1 = 1
cen1 = 15.85
sigma1 = 5
popt, pcov = curve_fit(_3Lorentzian, xData, yData, p0=[amp1, cen1, sigma1])

popt1, pcov1 = curve_fit(_1gaussian, xData, yData, p0=[amp1, cen1, sigma1])

fit_curve = _3Lorentzian(xData, *popt)
fit_curve1 = _1gaussian(xData, *popt1)

plt.plot(xData,yData, label='data')
plt.plot(xData,fit_curve, label='Lorentz fit')
plt.plot(xData,fit_curve1, label='Gaussian fit')
plt.legend()

#%%
'''this cell was used to perform the fitting for each curve'''

def _1gaussian(x, amp, x0, sig):
    return amp / (sig * np.sqrt(2 * np.pi)) * np.exp(-(x-x0)**2 / (2*sig**2))

z1 = z.copy()

# zoom in on (111) peak
#plt.plot(theta_arr[1100:1150],y[1100:1150])

xData = theta_arr.copy()
xData = xData[1100:1150]

# initial guesses 
amp1 = 1
cen1 = 15.85
sigma1 = 1

peak_positions = []
fit_curves = []
data_curves = []
for pattern in z1.T:
    # crop out 2theta range of peak
    yData = pattern[1100:1150]
    # normalize data
    yData = yData / max(yData)
    data_curves.append(yData)
    # fit curves
    popt1, pcov1 = curve_fit(_1gaussian, xData, yData, p0=[amp1, cen1, sigma1])
    peak_position = popt1[1]
    peak_positions.append(peak_position)
    # store solution
    fit_curve = _1gaussian(xData, *popt1)
    fit_curves.append(fit_curve)

fit_curves = np.array(fit_curves).T
data_curves = np.array(data_curves).T

plt.scatter(times, peak_positions)

