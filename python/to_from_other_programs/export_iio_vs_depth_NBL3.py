import xraylib as xl
import numpy as np

def eleXRF_energy(ele, energy):
    Z = xl.SymbolToAtomicNumber(ele); F =  xl.LineEnergy(Z, xl.KA1_LINE)
    if   xl.EdgeEnergy(Z, xl.K_SHELL) > energy: F = xl.LineEnergy(Z, xl.LA1_LINE)
    elif xl.EdgeEnergy(Z, xl.L1_SHELL) > energy: F = xl.LineEnergy(Z, xl.LB1_LINE)
    elif xl.EdgeEnergy(Z, xl.L2_SHELL) > energy: F = xl.LineEnergy(Z, xl.LB1_LINE)
    elif xl.EdgeEnergy(Z, xl.L3_SHELL) > energy: F = xl.LineEnergy(Z, xl.LG1_LINE)
    elif xl.EdgeEnergy(Z, xl.M1_SHELL) > energy: F = xl.LineEnergy(Z, xl.MA1_LINE) 
    return F

# values being compared in comments are for Cd_L
def iio_vs_depth(ele, thickness_increments, dt):
    # percent incoming beam transmitted to CdTe layer
    iio_Mo = np.exp(- xl.CS_Total_CP('Mo', beam_energy) * MO['LDensity'] * MO['Thick'] / beam_geometry)
    iio_ZnTe = np.exp(- ZNTE['capXsect'] * ZNTE['LDensity'] * ZNTE['Thick'] / beam_geometry)
    iio_in = iio_Mo * iio_ZnTe
    
    # percent outgoing Cd_L transmitted by external layers
    ele_line = eleXRF_energy(ele, beam_energy)
    mu_Mo_ele_line = xl.CS_Total_CP('Mo', ele_line)             #1800 vs. 1872 (matlab)
    mu_ZnTe_Cd_ele_line = xl.CS_Total_CP('ZnTe', ele_line)      #653 vs. 680 (matlab)
    c_1 = np.exp(- mu_Mo_ele_line * MO['LDensity'] * MO['Thick'] / detect_geometry)        # moly is a really good Cd_L and Te_L absorber, iio ~0.0287
    c_2 = np.exp(- mu_ZnTe_Cd_ele_line * ZNTE['LDensity'] * ZNTE['Thick'] / detect_geometry)
    iio_out = iio_in * c_1 * c_2                                #0.0151 vs. 0.0163 (matlab)
    
    # percent outgoing Cd_L transmitted by CdTe itself
    #mu_CdTe_ele = xl.CS_Total_CP('CdTe', ele_line)
    iio_ele_cdte = np.zeros(len(thickness_increments))
    cap_cross_section_of_one_sublayer_in = - xl.CS_Total_CP('CdTe', beam_energy) * CDTE['LDensity'] * dt / beam_geometry
    cap_cross_section_of_one_sublayer_out_ele = - xl.CS_Total_CP('CdTe', ele_line) * CDTE['LDensity'] * dt / detect_geometry
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
        rough_up = DEPTH_STEPS * (1+roughness)
        rough_down = DEPTH_STEPS * (1-roughness)
        rough_ups.append(rough_up)
        rough_downs.append(rough_down)
    return rough_ups, rough_downs

def rough_iios(rough_ups, rough_downs):
    ele_rough_iios_up =     [iio_vs_depth(ele, roughness, DT) for roughness in rough_ups]
    ele_rough_iios_up = np.stack(ele_rough_iios_up, axis=1)
    ele_rough_iios_down =   [iio_vs_depth(ele, roughness, DT) for roughness in rough_downs]
    ele_rough_iios_down = np.stack(ele_rough_iios_down, axis=1)
    return ele_rough_iios_up, ele_rough_iios_down

# SYCNHROTRON SETTINGS
beam_time = 'bad_geom'
if beam_time == 'good_geom':
    beam_energy = 8.99
    beam_theta = 90
    detect_theta = 47
elif beam_time == 'bad_geom':
    beam_energy = 12.7
    beam_theta = 75
    detect_theta = 15
#deg to radians
beam_geometry = np.sin(beam_theta*np.pi/180)
detect_geometry = np.sin(detect_theta*np.pi/180)                    
# layer thicknesses in cm
# only enter layer dictionary for upstream layers
MO =    {'Thick':0.00005,    'LDensity': 10.2, 'capXsect': xl.CS_Total_CP('Mo', beam_energy)}
ZNTE =  {'Thick':0.0000375,  'LDensity': 6.34, 'capXsect': xl.CS_Total_CP('ZnTe', beam_energy)}
CDTE =  {'Thick':0.0012000,  'LDensity': 5.85, 'capXsect': xl.CS_Total_CP('CdTe', beam_energy)}

# enter element 
ele = 'Cu'
# specify arbitrary depth of absorber
# thickness increment (cm); 1nm = 1E-7cm
DT = 1*10**-7
# thickness increment array (nm)                   
DEPTH_STEPS = np.linspace(0, 12000, 12001) 

# calc incicent beam attenuation profile
iio_beam = beamIn_vs_depth(DEPTH_STEPS, DT)

# calc XRF reabsorption reference profile
iio_ele = iio_vs_depth(ele, DEPTH_STEPS, DT) 

# calc XRF error dure to roughness
# specfiy percentage of roughness
    # e.g np.linspace(0.05, 0.2, 3) --> 5%, 12%, 20% 
deviations = np.linspace(0.05, 0.2, 3) 
rough_ups, rough_downs = generate_deviated_thicknesses(deviations)
rough_up, rough_down = rough_iios(rough_ups, rough_downs)

## save x and y for plotting in Origin
# convert x axis to um; format arr
DEPTH_UM = (DEPTH_STEPS/1000).reshape(-1,1)
# format arrays
iio_ele = iio_ele.reshape(-1,1)        
iio_beam = iio_beam.reshape(-1,1)
roughup = rough_up[:,1].reshape(-1,1)
roughdown = rough_down[:,1].reshape(-1,1)
arr = np.concatenate((DEPTH_UM, iio_beam, iio_ele, roughup, roughdown), axis=1)
SYSPATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\XRF absorption profiles'
FILE_OUT = SYSPATH + '\\' + str(detect_theta) +'deg_ALL'+ ele +'.csv'
#np.savetxt(FILE_OUT, arr, delimiter=',')

# finding attenuation length (length at which iio decays to 1/e)
# the initial intensity fraction is that fraction of XRF at the beginning
# of the CdTe layer (after penetrating the capping layers):
BEAM_ATTN_VAL = iio_beam[0]*(1/np.e)
ELE_ATTN_VAL = iio_ele[0]*(1/np.e)
# from 
#https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    print('1/e depth: {s}nm'.format(s=str(idx)))
    return array[idx]

print('1/e fraction: {s}'.format(s=str(find_nearest(iio_beam, BEAM_ATTN_VAL))))
print('1/e fraction: {s}'.format(s=str(find_nearest(iio_ele, ELE_ATTN_VAL))))

