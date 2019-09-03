import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter 
from skimage import filters
from scipy.ndimage import gaussian_filter
from scipy import stats

def make_plots(index1, index2, sig, switch):
    ele_1 = samp['elXBIC'][scan][index1][:,:-2]
    ele_2 = samp['elXBIC'][scan][index2][:,:-2]
    # gaussian filter of original data
    cu_gauss = gaussian_filter(ele_1, sigma=sig)                 # maintains shape
    zn_gauss = gaussian_filter(ele_2, sigma=sig)
    # gradients of gaussian filtered image
    cu_gradient = filters.sobel(cu_gauss)                       # maintains shape
    zn_gradient = filters.sobel(zn_gauss)
    # gradients without trimmed 'zero 'edges; prepping to find percentiles
    cu_gradient_no_edge = cu_gradient[np.nonzero(cu_gradient)] # returns raveled array
    zn_gradient_no_edge = zn_gradient[np.nonzero(zn_gradient)]
    
    # for overlaying plots ; generate the colors for your colormap
    color1 = colorConverter.to_rgba('c')
    color2 = colorConverter.to_rgba('c')
    # make the colormaps
    #cmap1 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap',['k','tab:orange'])
    cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap2',[color1,color2])
    #cmap1._init() # create lut array with rgba values
    cmap2._init() # create the _lut array, with rgba values
    # create your alpha array and fill the colormap with them
    # here it is progressive, but you can create whathever you want
    #alphas1 = np.linspace(0, 0.9, cmap1.N+3)
    alphas2 = np.linspace(0, 1.0, cmap2.N+3)
    #cmap1._lut[:,1] = alphas1
    cmap2._lut[:,-1] = alphas2
    
    if switch == 'raw':
        map_key = [ele_1, ele_2]
        x = map_key[0].ravel() ; xlab = 'raw ' + elements[index1]
        y = map_key[1].ravel() ; ylab = 'raw ' + elements[index2]
    elif switch=='just_gauss': 
        map_key = [cu_gauss, zn_gauss]
        x = map_key[0].ravel() ; xlab = elements[index1] + ' gauss filt sig={s}'.format(s=str(sig))
        y = map_key[1].ravel() ; ylab = elements[index2] + ' gauss filt sig={s}'.format(s=str(sig))
    elif switch=='filt_grad':
        map_key = [cu_gradient, zn_gradient]
        scatter_key = [cu_gradient_no_edge, zn_gradient_no_edge]
        x = scatter_key[0] ; xlab = elements[index1] + ' gradient filt sig={s}'.format(s=str(sig))
        y = scatter_key[1] ; ylab = elements[index2] + ' gradient filt sig={s}'.format(s=str(sig))
    
    fig, axs = plt.subplots(1,3)
    plt.tight_layout()
    axs[0].imshow(map_key[0], cmap='Oranges_r', origin='lower')
    axs[1].imshow(map_key[1], cmap='Blues_r', origin='lower')
    axs[2].imshow(map_key[0], cmap='Oranges_r', origin='lower')
    axs[2].imshow(map_key[1], cmap=cmap2, origin='lower')
    
    plt.figure()
    plt.scatter(x, y, s=3, color='#6B8E23')
    
    slope, intercept, r_squared, p_value, std_err = stats.linregress(x, y)
    line = slope*x + intercept
    plt.plot(x, line, color='#20B2AA') 
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.text(max(x)*0.75, max(y)*0.50, "$R^2$ = {s}".format(s=str(round(r_squared,3))))
    return

samp = NBL3_2
scan = 3
# 0:Cu, 1:Cd, 2:Te, 3:Zn, 4:Mo
index1 = 0
index2 = 1
sigma = 1

# strings used here: 
    # 'raw': for raw, fitted data 
    # 'just_gauss' for smoothed maps w/o gradients 
    # 'filt_grad' for smoothed gradient maps (first smooth, then calc and plot gradient)
make_plots(index1, index2, sigma, 'raw')
