import xraylib as xl
import numpy as np

beam_energy = 12.7 #keV
beam_theta = 90                                                     #angle of the beam relative to sample normal
beam_geometry = np.sin(beam_theta*np.pi/180)                        #convert to radians
detect_theta = 47                                                   #angle of the detector sample normal
detect_geometry = np.sin(detect_theta*np.pi/180)                    #convert to radians
# left off: want to check if element is in a given layer of interest
    # then call functions required for calculating iio of that element in that layer
    # relvant functions found in absorb_defs.py

### code comparable to matlab, only for and up to CdTe layer, will work on later ###
#percent incoming beam transmitted to CdTe layer
iio_Mo = np.exp(- MO['capXsect'] * MO['LDensity'] * MO['Thick'] / beam_geometry)
iio_ZnTe = np.exp(- ZNTE['capXsect'] * ZNTE['LDensity'] * ZNTE['Thick'] / beam_geometry)

iio_in = iio_Mo * iio_ZnTe

#percent outgoing Cd_L transmitted by external layers
Cd_L = get_Ele_XRF_Energy('Cd', beam_energy)

mu_Mo_Cd_L = xl.CS_Total_CP('Mo', Cd_L)         #1800 vs. 1872 (matlab)
mu_ZnTe_Cd_L = xl.CS_Total_CP('ZnTe', Cd_L)     #653 vs. 680 (matlab)

cd_1 = np.exp(- mu_Mo_Cd_L * MO['LDensity'] * MO['Thick'] / detect_geometry)        # moly is a really good Cd_L and Te_L absorber, iio ~0.0287
cd_2 = np.exp(- mu_ZnTe_Cd_L * ZNTE['LDensity'] * ZNTE['Thick'] / detect_geometry)

iio_out = iio_in * cd_1 * cd_2                  #0.0151 vs. 0.0163 (matlab)

#percent outgoing Cd_L transmitted by CdTe itself
mu_CdTe_Cd_L = xl.CS_Total_CP('CdTe', Cd_L)
steps = np.linspace(0, 12000, 12001)
dt = 1*10**-7

iio_cd_cdte = np.zeros(len(steps))

cap_cross_section_of_one_sublayer_in = - CDTE['capXsect'] * CDTE['LDensity'] * dt / beam_geometry
cap_cross_section_of_one_sublayer_out_CdL = - mu_CdTe_Cd_L * CDTE['LDensity'] * dt / detect_geometry

for index, step in enumerate(steps):
    beam_in = cap_cross_section_of_one_sublayer_in * index;
    beam_out = cap_cross_section_of_one_sublayer_out_CdL * index
    iio_cd_cdte[index] = iio_out * np.exp(beam_in + beam_out)
    
iio_cdL = np.mean(iio_cd_cdte) #0.00117 vs. 0.0021 (matlab)
    
    

