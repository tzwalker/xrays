
# coding: utf-8

# In[1]:

import matplotlib.pyplot as plt # for general plotting
import matplotlib.cm as cm # for colorscales in 2D maps. Shown in https://matplotlib.org/examples/color/colormaps_reference.html
import h5py
import numpy as np
import datetime
from mpl_toolkits.axes_grid1 import make_axes_locatable


# In[2]:

def print_map_info(mapnr, element, xpixsize, ypixsize, xrange, yrange, mapmin, mapmax):
    """Print size information of XRF map"""
    print("Map nr: " + str(mapnr) + ", element " + element + ":")
    print("  Map min: " + str(mapmin) + " ug/cm2")
    print("  Map max: " + str(mapmax) + " ug/cm2")
    print("  Pixel size Y: " + str(xpixsize) + " um")
    print("  Pixel size Y: " + str(ypixsize) + " um")
    print("  Map size Y: " + str(xrange) + " um")
    print("  Map size Y: " + str(yrange) + " um")

def print_MAPS_H5_file_content(f):
    """Print groups of H5 files created by XRF measurements by MAPS"""
    for dataset in f: # Loop through all elements in the h5 file
        print("Groups in file:  " + dataset)
    g = f['/MAPS'] # This is the group with the relevant data in the h5 file
    channel_names = f['/MAPS/channel_names']
    print("Content of '/MAPS': ")
    for dataset in g: # Loop through all elements in g
        h = f['/MAPS/' + dataset]
        print(h)
    for element in channel_names:
        print(element)

    return 0

def scaletoflux(fluxmeas):
    """Select to which flux measurement shall be scaled to"""
    if fluxmeas == 'ds_ic': # scale data to ds_ic
        return 0
    elif fluxmeas == 'us_ic': # scale data to us_ic
        return 1
    elif fluxmeas == 'SRcurrent': # scale data to SRcurrent
        return 2
    else: # No scale indicator --> don't scale
        return -1

def e2i(channel_names, element):
    """Convert element to the index for a given measurement"""
    j = 0
    for i in channel_names:
        if i.decode('utf-8') == element:  # Need to decode the binary string i
            return j
        j += 1
    print("Element not found in 'channel_names', sorry for that!")
    return -1

def isnan(num):
    """Return true if the argument is NaN, otherwise return false"""
    return num != num


# In[3]:

datapath = "C:/MSdata/postdoc/studies/beamtimes/2017-03 APS 2-ID-D/fitimgLa.dat"
savepath  = "C:/MSdata/postdoc/studies/2017/2017-03 La material/map plotting python/fig"


# In[6]:

def plotmap(fullpath, savename, element, fluxnorm, fitnorm):
    """Plot a H5 files created by XRF measurements by MAPS"""
    
    """Important settings"""
    savepng = True
    savepdf = True
    savetxt = True
    plotting= False
    respng = 500 # Resolution for png images in dpi
    respdf = 500 # Resolution for png images in dpi

    """Load file and relevant h5 groups"""
    f = h5py.File(fullpath, 'r')
    # f = h5py.File(r"C:\MSdata\postdoc\studies\beamtimes\2017-03 APS 2-ID-D\img.datfit\2idd_0256.h5", 'r')
    # print_MAPS_H5_file_content(f)
    channel_names = f['/MAPS/channel_names']  # Names of fitted channels such as 'Cu', 'TFY', 'La_L'
    scaler_names = f['/MAPS/scaler_names']  # Names of scalers such as 'SRcurrent', 'us_ic', 'ds_ic', 'deadT', 'x_coord'
    scalers = f['/MAPS/scalers']  # Scaler values for [scaler, x, y]
    XRF_fits = f['/MAPS/XRF_fits']  # Quantified channel [channel, x, y]
    XRF_fits_quant = f['/MAPS/XRF_fits_quant']  # Number of cts per ug/cm2 [???, ???, channel]
    XRF_roi = f['/MAPS/XRF_roi']  # Quantified channel [channel, x, y]
    XRF_roi_quant = f['/MAPS/XRF_roi_quant']  # Number of cts per ug/cm2 [???, ???, channel], to be used as sum ROI in maps instead of XRF_fits_quant
    x_axis = f['/MAPS/x_axis']  # x position of pixels  [position in um]
    y_axis = f['/MAPS/y_axis']  # y position of pixels  [position in um]

    """Select to which flux measurement shall be scaled to"""
    fluxnormmatrix = scalers[1, :, :];  fluxnormmatrix[:, :] = 1  # Matrix of scalers size but all 1 for no normalization
    if fluxnorm == 'ds_ic':  # scale data to ds_ic
        fluxnormindex = 0; fluxnormmatrix = scalers[fluxnormindex, :, :]
    elif fluxnorm == 'us_ic':  # scale data to us_ic
        fluxnormindex = 1; fluxnormmatrix = scalers[fluxnormindex, :, :]
    elif fluxmeas == 'SRcurrent':  # scale data to SRcurrent
        fluxnormindex = 2; fluxnormmatrix = scalers[fluxnormindex, :, :]

    """Select XRF element of interest"""
    elementindex = e2i(channel_names, element)

    """Select which fitting to be used for quantification"""
    if fitnorm == 'roi':  # Normalization with fitted data --> is default if fit works fine
        fitnormvalue = XRF_roi_quant[fluxnormindex, 0, elementindex]
        rawmatrix = XRF_roi[elementindex, :, :]
    elif fitnorm == 'fit':  # Normalization with ROI fitted --> To be used when maps creates a problem with the quantification
        fitnormvalue = XRF_fits_quant[fluxnormindex, 0, elementindex]
        rawmatrix = XRF_fits[elementindex, :, :]

    """Calculate quantified element matrix in ug/cm2"""
    m = rawmatrix / fluxnormmatrix / fitnormvalue
    # # t = ds / us  # Transmittance: ds_ic normalized to us_ic

    """Preparation for proper map scaling"""
    xrange = max(x_axis) - min(x_axis)
    xpixsize = xrange / len(x_axis)
    yrange = max(y_axis) - min(y_axis)
    ypixsize = yrange / len(y_axis)
    """Remove column with nan"""
    m = m[:, 0:len(x_axis)-1]
    yrange = yrange - ypixsize
    x = np.arange(-xrange / 2 + xpixsize / 2, xrange / 2, xpixsize)
    y = np.arange(-yrange / 2 + ypixsize / 2, yrange / 2, ypixsize)
     # print_map_info(mapnr, element, xpixsize, ypixsize, xrange, yrange, mapmin, mapmax)
    matrixm = np.asmatrix(m) # needed to evaluate min & max

    """Replace NaN in center of map (if part of dead line) with average value of two neighboring lines (problem with map 89)"""
    for i in range(0, len(m), 1):
        for j in range(0, len(m[0]), 1):
            if(isnan(m[i, j])):
                print("NaN @ i: " + str(i) + ", j: " + str(j))
                m[i, j] = (m[i-1, j] + m[i+1, j]) / 2

    """Plot raw map"""
    xsize = 5 # Size of figure in inches
    f, ax = plt.subplots(1, 1, figsize=(xsize, xsize * xrange / yrange))
    ax1 = plt.subplot(1, 1, 1)
    ax1.set_aspect(xrange / yrange)
    plt.pcolor(y, x, m, cmap=cm.afmhot, vmin=0, vmax=matrixm.max())
    plt.xlabel("X position  $(\mu m)$")
    plt.ylabel("Y position  $(\mu m)$")
    ax2 = plt.gca()
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(cax=cax)
    cax.set_ylabel('Area density of La  $(\mu g/cm^2)$', rotation=90)
    plt.tight_layout()
    if plotting == True:
        plt.show()
    if savetxt == True:
        np.savetxt(savename + ".asc", m, fmt='%1.4e')
    if savepdf == True:
        plt.savefig(savename + ".pdf", dpi=respdf)
    if savepng == True:
        plt.savefig(savename + ".png", dpi=respng)
    plt.close()

    """Plot masked map"""
    nx = m.shape[0]  # Number of x values of the ROI
    ny = m.shape[1]  # Number of x values of the ROI
    # masknoise = np.zeros((nx, ny))
    cutoff = 10
    mnonoise = np.ma.masked_where(m <  cutoff, m)
    f, ax = plt.subplots(1, 1, figsize=(xsize, xsize * xrange / yrange))
    ax1 = plt.subplot(1, 1, 1)
    ax1.set_aspect(xrange / yrange)
    plt.pcolor(y, x, mnonoise, cmap=cm.afmhot, vmin=0, vmax=matrixm.max())
    plt.xlabel("X position  $(\mu m)$")
    plt.ylabel("Y position  $(\mu m)$")
    ax2 = plt.gca()
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(cax=cax)
    cax.set_ylabel('Area density of La  $(\mu g/cm^2)$', rotation=90)
    plt.tight_layout()
    if plotting == True:
        plt.show()
    if savetxt == True:
        np.savetxt(savename + "_nonoise.asc", np.ma.filled(mnonoise, 0), fmt='%1.4e')
    if savepdf == True:
        plt.savefig(savename + "_nonoise.pdf", dpi=respdf)
    if savepng == True:
        plt.savefig(savename + "_nonoise.png", dpi=respng)
    plt.close()
    
    """Plot mask"""
    maskbool = ~np.ma.getmask(mnonoise)
    maskint = maskbool.astype(int)    
    f, ax = plt.subplots(1, 1, figsize=(xsize, xsize * xrange / yrange))
    ax1 = plt.subplot(1, 1, 1)
    ax1.set_aspect(xrange / yrange)
    plt.pcolor(y, x, maskint, cmap=cm.afmhot, vmin=0, vmax=1)
    plt.xlabel("X position  $(\mu m)$")
    plt.ylabel("Y position  $(\mu m)$")
    ax2 = plt.gca()
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(cax=cax)
    cax.set_ylabel('Black: No La, White: With La', rotation=90)
    plt.tight_layout()
    if plotting == True:
        plt.show()
    if savetxt == True:
        np.savetxt(savename + "_bool.asc", maskint, fmt='%1d')
    if savepdf == True:
        plt.savefig(savename + "_bool.pdf", dpi=respdf)
    if savepng == True:
        plt.savefig(savename + "_bool.png", dpi=respng)
    plt.close()
        
    return 0


# In[7]:

description = {
#     "175" : "s1_planview_HR_large",
#     "089" : "s5_planview_LR",
#     "091" : "s5_planview_HR_large",
#     "092" : "s5_planview_HR_small",
#     "160" : "s1_planview_LR",
#     "175" : "s1_planview_HR_large",
#     "176" : "s1_planview_HR",
#     "185" : "s15_planview_LR",
#     "186" : "s15_planview_HR_large",
#     "187" : "s15_planview_HR_small",
#     "196" : "s5c_planview_LR",
#     "197" : "s5c_planview_HR_large",
#     "198" : "s5c_planview_HR_small",
#     "209" : "s2.5_planview_LR",
#     "210" : "s2.5_planview_HR_large",
#     "212" : "s2.5_planview_HR_small",
#     "221" : "s10_planview_LR",
#     "222" : "s10_planview_HR_large",
#     "223" : "s10_planview_HR_small",
#     "234" : "s15_crosssection_HR_a",
#     "238" : "s15_crosssection_HR_b",
#     "257" : "s5c_crosssection_HR_a",
#     "259" : "s5c_crosssection_HR_b",
#     "273" : "s5_crosssection_HR_a",
#     "277" : "s5_crosssection_HR_b",
#     "289" : "s1_crosssection_HR_a",
#     "291" : "s1_crosssection_HR_b",
#     "301" : "s10_crosssection_HR_a"
}

"""Loop over all maps from 'description'"""
for key in description:
    print("Analyzing map no: ", key, " which is: ", description[key])
    timestart = datetime.datetime.now()
    plotmap(datapath+"/2idd_0"+key+".h5", savepath+"/"+description[key]+"_"+key, "La_L", "us_ic", "roi")
    timediff = datetime.datetime.now() - timestart
    print("   Time needed: ", timediff)


# In[ ]:



