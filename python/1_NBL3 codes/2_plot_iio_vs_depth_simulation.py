import xraylib as xl
import numpy as np
import matplotlib.pyplot as plt

def get_Ele_XRF_Energy(ele, energy):
    Z = xl.SymbolToAtomicNumber(ele)
    #will it abosrb? if so, it will fluoresce
    F = xl.LineEnergy(Z, xl.KA1_LINE)
    if xl.EdgeEnergy(Z, xl.K_SHELL) > energy:
            F = xl.LineEnergy(Z, xl.LA1_LINE)
            if xl.EdgeEnergy(Z, xl.L1_SHELL) > energy:
                    F = xl.LineEnergy(Z, xl.LB1_LINE)
                    if xl.EdgeEnergy(Z, xl.L2_SHELL) > energy:
                            F = xl.LineEnergy(Z, xl.LB1_LINE)
                            if xl.EdgeEnergy(Z, xl.L3_SHELL) > energy:
                                    F = xl.LineEnergy(Z, xl.LG1_LINE)
                                    if xl.EdgeEnergy(Z, xl.M1_SHELL) > energy:
                                            F = xl.LineEnergy(Z, xl.MA1_LINE) 
    return F


# returns numpy (fl64) array; essentially the simulated profile for the element 'ele' above
def iio_vs_depth(ele, t, dt):
    # percent incoming beam transmitted to CdTe layer
    iio_Mo = np.exp(- MO['capXsect'] * MO['LDensity'] * MO['Thick'] / beam_geometry)
    iio_ZnTe = np.exp(- ZNTE['capXsect'] * ZNTE['LDensity'] * ZNTE['Thick'] / beam_geometry)
    iio_in = iio_Mo * iio_ZnTe
    
    # percent outgoing Cd_L transmitted by external layers
    ele_line = get_Ele_XRF_Energy(ele, beam_energy)
    mu_Mo_ele_line = xl.CS_Total_CP('Mo', ele_line)         #1800 vs. 1872 (matlab)
    mu_ZnTe_Cd_ele_line = xl.CS_Total_CP('ZnTe', ele_line)     #653 vs. 680 (matlab)
    
    c_1 = np.exp(- mu_Mo_ele_line * MO['LDensity'] * MO['Thick'] / detect_geometry)        # moly is a really good Cd_L and Te_L absorber, iio ~0.0287
    c_2 = np.exp(- mu_ZnTe_Cd_ele_line * ZNTE['LDensity'] * ZNTE['Thick'] / detect_geometry)
    iio_out = iio_in * c_1 * c_2                  #0.0151 vs. 0.0163 (matlab)
    
    # percent outgoing Cd_L transmitted by CdTe itself
    mu_CdTe_ele = xl.CS_Total_CP('CdTe', ele_line)
    
    iio_ele_cdte = np.zeros(len(t))
    
    cap_cross_section_of_one_sublayer_in = - CDTE['capXsect'] * CDTE['LDensity'] * dt / beam_geometry
    cap_cross_section_of_one_sublayer_out_ele = - mu_CdTe_ele * CDTE['LDensity'] * dt / detect_geometry
    
    for index, step in enumerate(t):
        beam_in = cap_cross_section_of_one_sublayer_in * step;
        beam_out = cap_cross_section_of_one_sublayer_out_ele * step
        iio_ele_cdte[index] = iio_out * np.exp(beam_in + beam_out)
        
    #iio_ele = np.mean(iio_ele_cdte) #0.00117 vs. 0.0021 (matlab)
    return iio_ele_cdte

beam_energy = 12.7 #keV
beam_theta = 75                                                     #angle of the beam relative to the surface of the sample
beam_geometry = np.sin(beam_theta*np.pi/180)                        #convert to radians
detect_theta = 15                                                   #angle of the detector relative to the beam
detect_geometry = np.sin(detect_theta*np.pi/180)                    #convert to radians

MO =    {'Thick':0.00005,    'LDensity': 10.2, 'Name': 'Mo',     'capXsect': xl.CS_Total_CP('Mo', beam_energy)}
ZNTE =  {'Thick':0.0000375,  'LDensity': 6.34, 'Name': 'ZnTe',   'capXsect': xl.CS_Total_CP('ZnTe', beam_energy)}
# CU 'layer' is shown here, but is not used in this program
CU =    {'Thick':0.000001,   'LDensity': 8.96, 'Name': 'Cu',     'capXsect': xl.CS_Total_CP('Cu', beam_energy)}
# CDTE thickness is defined here, but is not used in this program
CDTE =  {'Thick':0.0005,    'LDensity': 5.85, 'Name': 'CdTe',   'capXsect': xl.CS_Total_CP('CdTe', beam_energy)} 
CDS =   {'Thick':0.000008,   'LDensity': 4.82, 'Name': 'CdS',    'capXsect': xl.CS_Total_CP('CdS', beam_energy)}
SNO2 =  {'Thick':0.00006,    'LDensity': 6.85, 'Name': 'SnO2',   'capXsect': xl.CS_Total_CP('SnO2', beam_energy)}


# enter element for which you wish to see I/Io
ele = 'Cu'

# the term 'uniform absorber' 
no_rough = np.linspace(0, 6000, 6001)             #(nm) arbitrary absorber depth of 12um;
dt = 1*10**-7                                       # 1nm = 1E-7cm

## 10 % roughness ##
roughness = 0.1

rough_up = no_rough * (1+roughness)
rough_down = no_rough * (1-roughness)


rough_list = [rough_up, no_rough, rough_down]

rough_in_um_list = []
for rough in rough_list:
    rough_in_um = rough / 1000
    rough_in_um_list.append(rough_in_um)


ele_rough_iios = []
for rough, rough_in_um in zip(rough_list, rough_in_um_list):
    ele_rough_iio = iio_vs_depth(ele, rough, dt)
    ele_rough_iios.append(ele_rough_iio)

# plot settings #
fig = plt.figure()
plt.plot(no_rough, ele_rough_iios[0], '--')
plt.plot(no_rough, ele_rough_iios[1])
plt.plot(no_rough, ele_rough_iios[2], '--')
#plt.title(ele + ' Attenuation', fontsize = 18)
plt.xlabel('Depth (um)', fontsize = 16)
plt.ylabel('I/Io' + ' (' + ele + ')', fontsize = 16)

ax.tick_params(axis = 'both', labelsize = 14) 
plt.ylim([0, 1.0])

plt.grid()

plt.show()

