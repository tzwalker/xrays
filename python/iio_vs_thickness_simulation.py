import xraylib as xl
import numpy as np
import matplotlib.pyplot as plt

from eleXRF_energy import get_Ele_XRF_Energy

# values being compared in comments are for Cd_L
def iio_vs_depth(ele, thickness_increments, dt):
    # percent incoming beam transmitted to CdTe layer
    iio_Mo = np.exp(- MO['capXsect'] * MO['LDensity'] * MO['Thick'] / beam_geometry)
    iio_ZnTe = np.exp(- ZNTE['capXsect'] * ZNTE['LDensity'] * ZNTE['Thick'] / beam_geometry)
    iio_in = iio_Mo * iio_ZnTe
    
    # percent outgoing Cd_L transmitted by external layers
    ele_line = get_Ele_XRF_Energy(ele, beam_energy)
    mu_Mo_ele_line = xl.CS_Total_CP('Mo', ele_line)             #1800 vs. 1872 (matlab)
    mu_ZnTe_Cd_ele_line = xl.CS_Total_CP('ZnTe', ele_line)      #653 vs. 680 (matlab)
    c_1 = np.exp(- mu_Mo_ele_line * MO['LDensity'] * MO['Thick'] / detect_geometry)        # moly is a really good Cd_L and Te_L absorber, iio ~0.0287
    c_2 = np.exp(- mu_ZnTe_Cd_ele_line * ZNTE['LDensity'] * ZNTE['Thick'] / detect_geometry)
    iio_out = iio_in * c_1 * c_2                                #0.0151 vs. 0.0163 (matlab)
    
    # percent outgoing Cd_L transmitted by CdTe itself
    mu_CdTe_ele = xl.CS_Total_CP('CdTe', ele_line)
    iio_ele_cdte = np.zeros(len(thickness_increments))
    cap_cross_section_of_one_sublayer_in = - CDTE['capXsect'] * CDTE['LDensity'] * dt / beam_geometry
    cap_cross_section_of_one_sublayer_out_ele = - mu_CdTe_ele * CDTE['LDensity'] * dt / detect_geometry
    for index, step in enumerate(thickness_increments):
        beam_in = cap_cross_section_of_one_sublayer_in * step;
        beam_out = cap_cross_section_of_one_sublayer_out_ele * step
        iio_ele_cdte[index] = iio_out * np.exp(beam_in + beam_out)
    #iio_ele = np.mean(iio_ele_cdte) #0.00117 vs. 0.0021 (matlab)
    return iio_ele_cdte

def beamIn_vs_depth(thickness_increments, dt):
    # percent incoming beam transmitted to CdTe layer
    iio_Mo = np.exp(- MO['capXsect'] * MO['LDensity'] * MO['Thick'] / beam_geometry)
    iio_ZnTe = np.exp(- ZNTE['capXsect'] * ZNTE['LDensity'] * ZNTE['Thick'] / beam_geometry)
    iio_in = iio_Mo * iio_ZnTe
    
    iio_cdte = np.zeros(len(thickness_increments))
    cap_cross_section_of_one_sublayer_in = - CDTE['capXsect'] * CDTE['LDensity'] * dt / beam_geometry
    for index, step in enumerate(thickness_increments):
        beam_in = cap_cross_section_of_one_sublayer_in * step
        iio_cdte[index] = iio_in * np.exp(beam_in)
    return iio_cdte

def generate_deviated_thicknesses(roughness_deviations):
    rough_ups = []
    rough_downs = []
    for roughness in roughness_deviations:
        rough_up = no_rough * (1+roughness)
        rough_down = no_rough * (1-roughness)
        rough_ups.append(rough_up)
        rough_downs.append(rough_down)
    return rough_ups, rough_downs

def rough_iios(rough_ups, rough_downs):
    ele_rough_iios_up =     [iio_vs_depth(ele, roughness, dt) for roughness in rough_ups]
    ele_rough_iios_up = np.stack(ele_rough_iios_up, axis=1)
    ele_rough_iios_down =   [iio_vs_depth(ele, roughness, dt) for roughness in rough_downs]
    ele_rough_iios_down = np.stack(ele_rough_iios_down, axis=1)
    return ele_rough_iios_up, ele_rough_iios_down

## define settings and stack parameters ##
beam_time = 'good_geom'
if beam_time == 'good_geom':
    beam_energy = 8.99
    beam_theta = 90
    detect_theta = 43
elif beam_time == 'bad_geom':
    beam_energy = 12.7
    beam_theta = 75
    detect_theta = 15

beam_geometry = np.sin(beam_theta*np.pi/180)                        #convert to radians
detect_geometry = np.sin(detect_theta*np.pi/180)                    #convert to radians
# enter thickness of layer in cm
# only upstream layers are of interest
MO =    {'Thick':0.00005,    'LDensity': 10.2, 'capXsect': xl.CS_Total_CP('Mo', beam_energy)}
ZNTE =  {'Thick':0.0000375,  'LDensity': 6.34, 'capXsect': xl.CS_Total_CP('ZnTe', beam_energy)}
CDTE =  {'Thick':0.0012000,  'LDensity': 5.85, 'capXsect': xl.CS_Total_CP('CdTe', beam_energy)}

# enter element for which you wish to see I/Io (will work on generatign plots for many elements at once)
ele = 'Cu'
# specify arbitrary depth of absorber
dt = 1*10**-7                           # thickness increment (cm); 1nm = 1E-7cm
no_rough = np.linspace(0, 12000, 12001) # thickness increment array (nm)
x_for_plotting = (no_rough/1000).reshape(-1,1) # convert x axis to um; format arr

#calc incicent beam attenuation profile
beam_attn = beamIn_vs_depth(no_rough, dt)
beam_attn = beam_attn.reshape(-1,1)

## calc XRF reabsorption reference profile
ref_iio = iio_vs_depth(ele, no_rough, dt) 
ref_iio = ref_iio.reshape(-1,1)   # format array      

## calc roughness profiles
deviations = np.linspace(0.05, 0.2, 3) # specfiy roughness parameters
rough_ups, rough_downs = generate_deviated_thicknesses(deviations)
rough_up, rough_down = rough_iios(rough_ups, rough_downs)

## save x and y for plotting in Origin
arr_for_plotting0 = np.concatenate((x_for_plotting, beam_attn, ref_iio, 
                                    # first column for 12.5% roughness (from 'deviations')
                                    rough_up[:,1].reshape(-1,1), 
                                    rough_down[:,1].reshape(-1,1)), axis=1)

np.savetxt(r'C:\Users\Trumann\Dropbox (ASU)\1_NBL3 data\for Origin iio_sims\iio_sim_' + str(detect_theta) +'deg_ALL'+ ele +'.csv', arr_for_plotting0, delimiter=',')


# supplementary info plotting
plt.plot(x_for_plotting, beam_attn)
plt.plot(x_for_plotting, ref_iio)
plt.plot(x_for_plotting, rough_up[:,1])
plt.plot(x_for_plotting, rough_down[:,1])
plt.grid()
plt.ylabel('% attenuation')
plt.xlabel('CdTe thickness')

# iio vs. depth() is essentially the same as the calculation seen in absorb_matlib_v_xraylib
# only dependency iio_vs_depth() has on CdTe thickness is seen in the "no_rough" variable
    # an arbitrarily large 12um thickness was chosen to calculate iio through the entirety of a thick cdte layer
    # slicing iio to thickness found from SIMS (slide 60 in "NBL3 consolidated notes.ppt"), then averaging will
    # yield mean iio correction factor for Cu in all samples
    # enter these factors somewhere into a_start.py, and apply them to Cu maps

# =============================================================================
### get average iio for absorbers of different thicknesses
# absorbers = [8516, 7745, 5320]
# samp_iios = [np.mean(ref_iio[0:absorber_thick] for absorber_thick in absorbers]
# =============================================================================

