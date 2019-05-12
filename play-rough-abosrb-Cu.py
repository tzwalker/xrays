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

beam_energy = 12.7 #keV
beam_theta = 75                                                     #angle between beam and sample normal
beam_geometry = np.sin(beam_theta*np.pi/180)                        #convert to radians
detect_theta = 15                                                   #angle between sample normal and detector
detect_geometry = np.sin(detect_theta*np.pi/180)                    #convert to radians

MO =    {'Element':['Mo'],          'MolFrac':[1],      'Thick':0.00005,    'LDensity': 10.2, 'Name': 'Mo',     'capXsect': xl.CS_Total_CP('Mo', beam_energy)}
ZNTE =  {'Element':['Zn','Te'],     'MolFrac':[1,1],    'Thick':0.0000375,  'LDensity': 6.34, 'Name': 'ZnTe',   'capXsect': xl.CS_Total_CP('ZnTe', beam_energy)}
CU =    {'Element':['Cu'],          'MolFrac':[1],      'Thick':0.000001,   'LDensity': 8.96, 'Name': 'Cu',     'capXsect': xl.CS_Total_CP('Cu', beam_energy)}
CDTE =  {'Element':['Cd','Te'],     'MolFrac':[1,1],    'Thick':0.0005,    'LDensity': 5.85, 'Name': 'CdTe',   'capXsect': xl.CS_Total_CP('CdTe', beam_energy)}
CDS =   {'Element':['Cd','S'],      'MolFrac':[1,1],    'Thick':0.000008,   'LDensity': 4.82, 'Name': 'CdS',    'capXsect': xl.CS_Total_CP('CdS', beam_energy)}
SNO2 =  {'Element':['Sn','O'],      'MolFrac':[1,2],    'Thick':0.00006,    'LDensity': 6.85, 'Name': 'SnO2',   'capXsect': xl.CS_Total_CP('SnO2', beam_energy)}


####### ONE: percent incoming beam transmitted to CdTe layer #######

iio_Mo = np.exp(- MO['capXsect'] * MO['LDensity'] * MO['Thick'] / beam_geometry)
iio_ZnTe = np.exp(- ZNTE['capXsect'] * ZNTE['LDensity'] * ZNTE['Thick'] / beam_geometry)
#iio_Au = np.exp(- xl.CS_Total_CP('Au', beam_energy) * 19.32 * (100*10**-7))
#iio_Ag = np.exp(- xl.CS_Total_CP('Ag', beam_energy) * 10.49 * (100*10**-7))
iio_in =  iio_Mo * iio_ZnTe

####### TWO: percent outgoing Cd_L transmitted by external layers #######
Cu_K = get_Ele_XRF_Energy('Cu', beam_energy)

mu_Mo_Cu_K = xl.CS_Total_CP('Mo', Cu_K)         
mu_ZnTe_Cu_K = xl.CS_Total_CP('ZnTe', Cu_K)
#mu_Au_Cd_L = xl.CS_Total_CP('Au', Cd_L)
#mu_Ag_Cd_L = xl.CS_Total_CP('Ag', Cd_L)          

c_1 = np.exp(- mu_Mo_Cu_K * MO['LDensity'] * MO['Thick'] / detect_geometry)        # moly is a really good Cd_L and Te_L absorber, iio ~0.0287
c_2 = np.exp(- mu_ZnTe_Cu_K * ZNTE['LDensity'] * ZNTE['Thick'] / detect_geometry)
#cd_3 = np.exp( - mu_Au_Cd_L * 19.32 * (100*10**-7))
#cd_4 = np.exp( - mu_Ag_Cd_L * 10.49 * (100*10**-7))

iio_out = iio_in * c_1 * c_2

####### THREE: percent outgoing Cd_L transmitted by CdTe itself #######
mu_CdTe_Cu_K = xl.CS_Total_CP('CdTe', Cu_K)
steps = np.linspace(0, 12000, 12001)
dt = 1*10**-7

iio_cu_cdte = np.zeros(len(steps))

cap_cross_section_of_one_sublayer_in = - CDTE['capXsect'] * CDTE['LDensity'] * dt / beam_geometry
cap_cross_section_of_one_sublayer_out_CuK = - mu_CdTe_Cu_K * CDTE['LDensity'] * dt / detect_geometry

for index, step in enumerate(steps):
    beam_in = cap_cross_section_of_one_sublayer_in * index;
    beam_out = cap_cross_section_of_one_sublayer_out_CuK * index
    iio_cu_cdte[index] = iio_out * np.exp(beam_in + beam_out)
    
iio_cdL = np.mean(iio_cu_cdte)

steps_in_um = steps / 1000

fig, ax = plt.subplots()

plt.plot(steps_in_um, iio_cu_cdte)
plt.title('Cu_K Attenuation - w/Mo and ZnTe', fontsize = 18)
plt.xlabel('Depth (um)', fontsize = 16)
plt.ylabel('I/Io', fontsize = 16)

ax.tick_params(axis = 'both', labelsize = 14) 
#plt.ylim([0, 0.0155])

plt.grid()

plt.show()

