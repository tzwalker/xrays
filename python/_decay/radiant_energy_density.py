# -*- coding: utf-8 -*-
"""

Trumann
Tue Apr 19 13:12:23 2022

this program is meant for a dosage calculation on per-pixel basis

it simply includes a time component, converts photon flux to energy dose

relevant for scan196, unfiltered beam

"""
import numpy as np

flux = 3.4e8 # ph/s

# assuming clyindrical interaction volume
spot_radius = 50 # nm
spot_radius = spot_radius * (1/1e9) * (1e2/1) # cm
spot_area = np.pi*spot_radius**2  # cm2
CdTe_thickness = 3 # um
CdTe_thickness = CdTe_thickness * (1/1e6) * (1e2/1) # cm

spectral_flux_density = flux/(spot_area*CdTe_thickness) # ph/(cm3*s)
energy = 10400 # eV
spectral_flux_density_eV = spectral_flux_density*energy # eV/(cm3*s)
spectral_flux_density_J = spectral_flux_density_eV*1.602e-19 # J/(cm3*s)

# the radiant energy density for one pixel
time_per_pixel = 0.5 # sec
radiant_energy_density = spectral_flux_density_J*time_per_pixel # J/cm3

# but this is cumulative... make pixel array in raster pattern similar to measurement
# this is basically the time index for the measurement
x = np.arange(41*41).reshape(41, -1)
# add one because the first pixel is the first time step
x = x+1
# make map that has time counter
time_of_pixels = x*time_per_pixel

radiant_energy_density_spacetime = time_of_pixels*spectral_flux_density_J # J/cm3
radiant_energy_density_spacetime_MJ = radiant_energy_density_spacetime/1e6
radiant_energy_density_spacetime_GJ = radiant_energy_density_spacetime/1e9

#%%
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import ticker
from matplotlib import colors

unit = 'Radiant Energy Density (GJ/cm$^3$)'
cbar_txt_size = 11

fig, ax = plt.subplots()

im = ax.imshow(radiant_energy_density_spacetime_GJ,cmap ='viridis', norm=colors.LogNorm(vmin=0.01,vmax=10))

divider = make_axes_locatable(ax)

cax = divider.append_axes('right', size='5%', pad=0.1)
#fmt = ticker.ScalarFormatter(useMathText=True)
#fmt.set_powerlimits((0, 0))
cb = fig.colorbar(im, cax=cax, orientation='vertical')#,format=fmt)
    #get color bar object
cbar = plt.gcf().axes[-1]
    #format colorbar
cbar.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
    # change number of tick labels on colorbar
#cbar.locator_params(nbins=4)
    #change colorbar tick label sizes
cbar.tick_params(labelsize=cbar_txt_size)
    #change color bar scale label size, e.g. 1e-8
cbar.yaxis.get_offset_text().set(size=cbar_txt_size)
    #change color bar scale label position   
cbar.yaxis.set_offset_position('left')