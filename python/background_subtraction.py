# -*- coding: utf-8 -*-
"""
Trumann
Tue Mar 17 11:27:20 2020

similar (but not exact) background subtraction performed in imageJ
the program uses a white-top hat transform; helpful inks:
    https://en.wikipedia.org/wiki/Top-hat_transform
    https://en.wikipedia.org/wiki/Opening_(morphology)
    https://en.wikipedia.org/wiki/Closing_(morphology)
    
the program allows the user to specify a radius (in pixels) of the rolling-ball

NOTE: strictly speaking, the radius of the ball
should not be smaller than the LARGEST feature size in the image (in pixels)
"""

from scipy.ndimage import white_tophat
from skimage.morphology import ball

def rollball_bkgnd_subtraction(array, ball_radius):
    # Create 3D ball structure
    s = ball(ball_radius) 
    # Take only the upper half of the ball
    h = int((s.shape[1] + 1) / 2)
    # Flat the 3D ball to a weighted 2D disc
    s = s[:h, :, :].sum(axis=0)
    # Rescale weights into 0-1
    s = (1 * (s - s.min())) / (s.max()- s.min()) 
    # Use "white tophat" transform 
    nobkgnd_array = white_tophat(array, structure=s)
    return nobkgnd_array

