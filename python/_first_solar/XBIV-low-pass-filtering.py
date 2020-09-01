"""
coding: utf-8

tzwalker
Tue Sep  1 14:09:48 2020

this program takes an XBIV image from "translated analyses.py"
and filters out the high spatial frequencies

this is done by computing the 2D FFT spectra,
applying a circular, binary mask to the spectra
then, inverting the thresholded spectra back to real space
"""

import numpy as np
img = imgs[0].copy()

# normalize data using "max-min stretch"
img_norm = (img - img.min()) / (img.max() - img.min())

# compute fast fourier transform
fft_spectrum = np.fft.fft2(img_norm)
# to plot
fft_mod = np.abs(fft_spectrum)
fft_log = np.log(1+fft_mod)

# shift zero-frequency component to center of spectrum (for convenience)
fft_shft = np.fft.fftshift(fft_spectrum)
# to plot
fft_mod1 = np.abs(fft_shft)
fft_log1 = np.log(1+fft_mod1)


# the filter threshold radius is defined as the index of the frequency bin that
# has the spatial frequency at which you want to threshold:
    # e.g.if I want to set a threshold at 1.2/um,
    # the frequency bin closest to 1.2/um has an index of 43
        # the index can be calculated using numpy fxn 
            #'np.fft.fftfreq(num_of_steps_in_width_of_img,step_size)'
    # index 43 defines the threshold radius:
        # 43 is the number of steps away
        # from the center of the frequency-space fft spectrum one needs to take
        # make a filter that eliminates frequencies above 1.2/um
# compute (symmetric) frequency bins accroding to (row-wise) sample step
N = np.shape(img_norm)[1]
um_step = 0.150
freq = np.fft.fftfreq(N, d=um_step)
# use array 'freq' to find index of patial frequency by which you wish to threshold

# https://medium.com/@hicraigchen/digital-image-processing-using-fourier-transform-in-python-bcb49424fd82
def distance(point1,point2):
    return np.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def low_pass_brickwall_filter(thres_radius,imgShape):
    base = np.zeros(imgShape)
    rows, cols = imgShape
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            if distance((y,x),center) < thres_radius:
                base[y,x] = 1
    return base
# make symmetric filter in frequency (i.e the fft spectrum's) space
LP_filt = low_pass_brickwall_filter(43, np.shape(img))

# apply filter to FFT spectrum
fft_shft_filt = LP_filt * fft_shft
# to plot
fft_mod2 = np.abs(fft_shft_filt)
fft_log2 = np.log(1+fft_mod2)

# shift the zero-frequency component to corners of spectrum 
# (prep for inversion to real space)
fft_filt = np.fft.ifftshift(fft_shft_filt)

# invert spectrum to real space
img_filt = np.fft.ifft2(fft_filt)

# plot filtered image
plt.imshow(np.abs(img_filt))