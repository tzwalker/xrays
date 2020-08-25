"""
coding: utf-8

tzwalker
Thu Aug 20 10:32:47 2020

Fourier transform play file
this is a manual implementation of an FFT filter
there are concerns with this approach, to be addressed later
for now, just trying to see if we can get some output
"""

import numpy as np
img = imgs[0].copy()

# normalize data using "max-min stretch"
img_norm = (img - img.min()) / (img.max() - img.min())

# compute fast fourier transform
fft_spectrum = np.fft.fft2(img_norm)
fft_mod = np.abs(fft_spectrum)
fft_log = np.log(1+fft_mod)

# shift zero-frequency component to center of spectrum (for convenience)
fft_shft = np.fft.fftshift(fft_spectrum)
#img_mod1 = np.abs(img_shft)
#img_log1 = np.log(1+img_mod1)


# the filter threshold radius is defined as the index of the frequency bin that
# has the spatial frequency at which you want to threshold:
    # e.g.if I want to set a threshold at 1.2/um,
    # the frequency bin closest to 1.2/um has an index of 43
    # the index can be calculated using numpy fxn 'np.fft.fftfreq'
    # the index 43 defines the threshold radius:
        # 43 is the number of steps away
        # from the center of the frequency-space fft spectrum one needs to take
        # make a filter that eliminates frequencies above 1.2/um
# compute (symmetric) frequency bins accroding to sample step
N = np.shape(img_norm)[1]
um_step = 0.150
freq = np.fft.fftfreq(N, d=um_step)

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

fft_filt = np.fft.ifftshift(fft_shft_filt)

img_filt = np.fft.ifft2(fft_filt)

plt.imshow(np.log(1+np.abs(fft_shft_filt)))
plt.imshow(np.abs(img_filt))