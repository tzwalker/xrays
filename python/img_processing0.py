"""
tzwalker
Sun Dec  1 20:38:13 2019
coding: utf-8

#xy points in each bulk scan
#3:151, 4:201, 5:201 --> TS58A
#3:151, 4:151 --> NBL3_3
#3:151, 4:151, 5:201 --> NBL3_2

#bulk selected:
    #scan538 (4) for NBL3_2
    #scan491 (4) for NBL3_3
    #scan439 (3) of TS58A
    
#interface selected:
    #scan422 (0) for NBL3_2
    #scan264 (0) for NBL3_3
    #scan386 (1) of TS58A
"""

from scipy.ndimage.filters import gaussian_filter
from skimage import io, filters, feature
from skimage.segmentation import slic, mark_boundaries, watershed
from sklearn.linear_model import LinearRegression
import sklearn.preprocessing as sklp
from matplotlib.colors import colorConverter, LinearSegmentedColormap
from skimage.filters import sobel
from scipy import stats

SAMP = NBL3_2; SCAN = 0; CHAN=1; CHECK_MASK=1
IMG_PATH = r'Z:\Trumann\XRF images\py_exports_interface\{sample}\scan{scan_idx}'.format(sample=SAMP['Name'], scan_idx=SAMP['XBIC_scans'][SCAN])
MASKFILE = IMG_PATH + r'\bound_0in_2out_mask.txt' # <-- CORES OR BOUNDARIES 
mask = np.loadtxt(MASKFILE)
mask_plot = np.ma.masked_where(mask == 0, mask) # to plot transparent mask

NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Mo', 'Zn']
CMAPS = ['magma', 'Oranges_r', 'Greens_r', 'Blues_r', 'Reds_r', 'Greys_r']
# check mask #
if CHECK_MASK == 1:
    img = SAMP['XBIC_maps'][SCAN][CHAN,:,:-2]
    img_filt = gaussian_filter(img, sigma=1)
    plt.imshow(img, cmap=CMAPS[CHAN])
    plt.imshow(mask_plot, cmap='cool')
else: pass

scaler = sklp.StandardScaler()

PLOT_SWITCH=4
XCHAN = 2; YCHAN = 0
# raw, pix-by-pix correlation #
if PLOT_SWITCH == 0:
    xchan = SAMP['XBIC_maps'][SCAN][XCHAN,:,:-2]; ychan = SAMP['XBIC_maps'][SCAN][YCHAN,:,:-2] 
    x = xchan.ravel().reshape(-1,1); y = ychan.ravel().reshape(-1,1)

# gaussian filtered, pix-by-pix correlation #
if PLOT_SWITCH == 1:
    xchan = SAMP['XBIC_maps'][SCAN][XCHAN,:,:-2]; ychan = SAMP['XBIC_maps'][SCAN][YCHAN,:,:-2] 
    xfilt = gaussian_filter(xchan, sigma=1)
    yfilt = gaussian_filter(ychan, sigma=1)
    x = xfilt.ravel().reshape(-1,1); y = yfilt.ravel().reshape(-1,1)
# gaussian filtered, masked pix-pix correlation #
if PLOT_SWITCH == 2:
    xchan = SAMP['XBIC_maps'][SCAN][XCHAN,:,:-2]; ychan = SAMP['XBIC_maps'][SCAN][YCHAN,:,:-2] 
    xfilt = gaussian_filter(xchan, sigma=1)
    yfilt = gaussian_filter(ychan, sigma=1)
    xmasked = xfilt[np.where(mask!=0)]
    ymasked = yfilt[np.where(mask!=0)]
    x = xmasked.reshape(-1,1); y = ymasked.reshape(-1,1)
TXT_PLACE=[0.35*np.max(x), 0.97*np.max(y)]
# for XBIC vs. XRF comparisons #
if PLOT_SWITCH==3:
    xchan = SAMP['XBIC_maps'][SCAN][XCHAN,:,:-2]; ychan = SAMP['XBIC_maps'][SCAN][YCHAN,:,:-2] 
    xfilt = gaussian_filter(xchan, sigma=1)
    xmasked = xfilt[np.where(mask!=0)]; ymasked = yfilt[np.where(mask!=0)]
    xshaped = xmasked.reshape(-1,1); yshaped = ymasked.reshape(-1,1)
    scaler = sklp.StandardScaler()
    x = scaler.fit_transform(xshaped); y=scaler.fit_transform(yshaped)
    TXT_PLACE = [-1,2]

# use enhanced image from IMageJ #
if PLOT_SWITCH==4:
    XIMG_FILE = r'Z:\Trumann\XRF images\py_exports_interface\{sample}\scan{scan_idx}\{channel}.tif'.format(
            sample=SAMP['Name'], scan_idx=SAMP['XBIC_scans'][SCAN], channel=NAMES[XCHAN])
    ximg = io.imread(XIMG_FILE)
    
    YIMG_FILE = r'Z:\Trumann\XRF images\py_exports_interface\{sample}\scan{scan_idx}\{channel}.tif'.format(
            sample=SAMP['Name'], scan_idx=SAMP['XBIC_scans'][SCAN], channel=NAMES[YCHAN])
    yimg= io.imread(YIMG_FILE)
    CHECK_ENHANCED_MASK = 1
    # check mask #
    if CHECK_ENHANCED_MASK == 1:
        fig, (ax0, ax1) = plt.subplots(1,2)
        ax0.imshow(ximg, cmap=CMAPS[XCHAN])
        ax0.imshow(mask_plot, cmap='cool')
        ax1.imshow(yimg, cmap=CMAPS[YCHAN])
        ax1.imshow(mask_plot, cmap='cool')
    else: pass
    
    XMASKED = ximg[np.where(mask!=0)]; YMASKED = yimg[np.where(mask!=0)]
    xshaped = XMASKED.reshape(-1,1); yshaped = YMASKED.reshape(-1,1)
    x = scaler.fit_transform(xshaped); y=scaler.fit_transform(yshaped)

# manual regression #
MODELR = LinearRegression()
model = MODELR.fit(x, y)
ypred = model.predict(x)
# NICE HEXBIN PLOT WITH HISTOGRAMS: SETUP #
fig = plt.figure(figsize=(5,5))
grid = plt.GridSpec(4, 4, hspace=0.2, wspace=0.2)
main_ax = fig.add_subplot(grid[-3:, :-1])
x_hist = fig.add_subplot(grid[0, :-1], xticklabels=[], xticks=[])
y_hist = fig.add_subplot(grid[-3:, 3], yticklabels=[], yticks=[])
# plot #
#main_ax.hexbin(x,y, mincnt=1, cmap='Greys', gridsize=(50,20))
main_ax.scatter(x,y,s=2, c='#808080')
main_ax.plot(x, ypred, color='#0f0f0f', linestyle='--', linewidth=3)
main_ax.set_xlim([np.min(x), np.max(x)])
main_ax.set_ylim([np.min(y), np.max(y)])
x_hist.hist(x, 40, orientation='vertical', color='gray')
y_hist.hist(y, 40, orientation='horizontal', color='gray')
TXT_PLACE = [0,2]
main_ax.text(TXT_PLACE[0], TXT_PLACE[1], "m={0:.3g}, b={1:.3g}".format(model.coef_[0][0],model.intercept_[0]))

def complicated_overlay_plots(index1, index2, sig, switch):
    ele_1 = samp['elXBIC'][scan][index1][:,:-2]
    ele_2 = samp['elXBIC'][scan][index2][:,:-2]
    
    if switch == 'raw':
        map_key = [ele_1, ele_2]
        x = map_key[0].ravel() ; xlab = 'raw ' + elements[index1]
        y = map_key[1].ravel() ; ylab = 'raw ' + elements[index2]
    elif switch=='just_gauss':
		# gaussian filter of original data
		cu_gauss = gaussian_filter(ele_1, sigma=sig)   # maintains shape
		zn_gauss = gaussian_filter(ele_2, sigma=sig)
        map_key = [cu_gauss, zn_gauss]
        x = map_key[0].ravel() ; xlab = elements[index1] + ' gauss filt sig={s}'.format(s=str(sig))
        y = map_key[1].ravel() ; ylab = elements[index2] + ' gauss filt sig={s}'.format(s=str(sig))
    elif switch=='filt_grad':
		# gradients of gaussian filtered image
		cu_gradient = sobel(cu_gauss)    # maintains shape
		zn_gradient = sobel(zn_gauss)
		# gradients without trimmed 'zero 'edges; prepping to find percentiles
		cu_gradient_no_edge = cu_gradient[np.nonzero(cu_gradient)] # returns raveled array
		zn_gradient_no_edge = zn_gradient[np.nonzero(zn_gradient)]
        map_key = [cu_gradient, zn_gradient]
        scatter_key = [cu_gradient_no_edge, zn_gradient_no_edge]
        x = scatter_key[0] ; xlab = elements[index1] + ' gradient filt sig={s}'.format(s=str(sig))
        y = scatter_key[1] ; ylab = elements[index2] + ' gradient filt sig={s}'.format(s=str(sig))
    
	
    color1 = colorConverter.to_rgba('c')
    color2 = colorConverter.to_rgba('c')
    # make the colormaps
    cmap2 = LinearSegmentedColormap.from_list('my_cmap2',[color1,color2])
	# create the _lut array, with rgba values
    cmap2._init() 
    # create your alpha array and fill the colormap with them
    alphas2 = np.linspace(0, 1.0, cmap2.N+3)
    cmap2._lut[:,-1] = alphas2
	
	## original map 1, original map 2, overlaid map ##
    fig, axs = plt.subplots(1,3)
    plt.tight_layout()
    axs[0].imshow(map_key[0], cmap='Oranges_r', origin='lower')
    axs[1].imshow(map_key[1], cmap='Blues_r', origin='lower')
    axs[2].imshow(map_key[0], cmap='Oranges_r', origin='lower')
    axs[2].imshow(map_key[1], cmap=cmap2, origin='lower')
    ## scatter plot bewteen overlapped maps ##
    plt.figure()
    plt.scatter(x, y, s=3, color='#6B8E23')
    slope, intercept, r_squared, p_value, std_err = stats.linregress(x, y)
    line = slope*x + intercept
    plt.plot(x, line, color='#20B2AA') 
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.text(max(x)*0.75, max(y)*0.50, "$R^2$ = {s}".format(s=str(round(r_squared,3))))
    return

#samp = NBL3_2
#scan = 3
#idx1 = 0; idx2 = 1
#sigma = 1
# for overlaying plots ; generate the colors for your colormap
# strings used here: 
    # 'raw': for raw, fitted data 
    # 'just_gauss' for smoothed maps w/o gradients 
    # 'filt_grad' for smoothed gradient maps (first smooth, then calc and plot gradient)
#overlay_plots(idx1, idx2, sigma, 'raw')

