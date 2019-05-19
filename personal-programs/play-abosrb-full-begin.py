import xraylib as xl
import numpy as np

#returns the energy of fluorescent photon of a given element due to the beam energy
#if-statements checks whether the element will absorb; is absorption edge higher than beam_energy?
    #if yes, no absorption, fluorescent photon energy is set to the next highest energy of the next shell
        # ex) Cd_L = 3.1338 keV , Cd_K_edge = 26.7, Cd_L_edge = 4.018
        #       
    #if no, absorption, fluorescent photon energy remains at the highest energy of the current shell
    
    ##functions of interest!
    #element_XRF_energy = xl.LineEnergy(xl.SymbolToAtomicNumber("element"), xl.XRF line you want)
    #Layer_cataching_ele_XRF = xl.CS_Total_CP("layer", element_XRF_energy)
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
beam_energy = 8.99                                                  #beamtime keV
beam_theta = 90                                                     #angle of the beam relative to the surface of the sample
beam_geometry = np.sin(beam_theta*np.pi/180)                        #convert to radians
detect_theta = 47                                                   #angle of the detector relative to the beam
detect_gemoetry = np.sin(detect_theta*np.pi/180)                    #convert to radians
dt = 1 * (1*10**-3) * (1*10**-4)                                   #convert 1nm step sizes to cm: 1nm * (1um/1000nm) * (1cm/10000um)

#enter lengths in cm
MO =    {'Element':['Mo'],          'MolFrac':[1],      'Thick':0.00005,    'LDensity': 10.2, 'Name': 'Mo',     'capXsect': xl.CS_Total_CP('Mo', beam_energy)}
ZNTE =  {'Element':['Zn','Te'],     'MolFrac':[1,1],    'Thick':0.0000375,  'LDensity': 6.34, 'Name': 'ZnTe',   'capXsect': xl.CS_Total_CP('ZnTe', beam_energy)}
CU =    {'Element':['Cu'],          'MolFrac':[1],      'Thick':0.000001,   'LDensity': 8.96, 'Name': 'Cu',     'capXsect': xl.CS_Total_CP('Cu', beam_energy)}
CDTE =  {'Element':['Cd','Te'],     'MolFrac':[1,1],    'Thick':0.0005,    'LDensity': 5.85, 'Name': 'CdTe',   'capXsect': xl.CS_Total_CP('CdTe', beam_energy)}
CDS =   {'Element':['Cd','S'],      'MolFrac':[1,1],    'Thick':0.000008,   'LDensity': 4.82, 'Name': 'CdS',    'capXsect': xl.CS_Total_CP('CdS', beam_energy)}
SNO2 =  {'Element':['Sn','O'],      'MolFrac':[1,2],    'Thick':0.00006,    'LDensity': 6.85, 'Name': 'SnO2',   'capXsect': xl.CS_Total_CP('SnO2', beam_energy)}

#COMBINE THE LAYERS FROM ABOVE INTO A LIST (UPTREAM LAYER FIRST, DOWNSTREAM LAYER LAST)
STACK = [MO, ZNTE, CU, CDTE, CDS, SNO2]

def get_iio_in(layer_index, layer_dict):
    
    
    
    return attenuation_of_incdent_beam_thru_upstream_layers

for index, layer in enumerate(STACK):
    iio_in = get_iio_in(index, layer)
    iio_out = get_iio_out(index, layer)
    iio_array = get_iio_array(index, layer)
    ele_iio = np.mean(iio_array)


def getSublayers(layer):
    T = layer['Thick']                                          #layer thickness in cm
    sublayers = T/dt                                            #number of 10nm sublayers in the layer
    sublayers = round(sublayers)
    sublayers = int(sublayers)
    key = 'numSublayers'                                        #add key to layer dictionary (for convenience)
    layer.setdefault(key, sublayers)                            #connect key to number of sublayers calculated
    return sublayers

#attenuation of beam intensity through each layer
def IncidentBeamAttenuation(stack_list):
    Bo_previous = 1
    for layer in STACK:
        Bo = Bo_previous * np.exp(- layer['capXsect'] * layer['LDensity'] * layer['Thick'])         #cm2/g * g/cm3 * cm; calculate bulk attenuation of layers external to the layer chosen
        rounded_Bo = round(Bo, 7)                                                                   #round Bo to 7 decimals for memory conservation
        key = 'Bo'                                                                                  #add key to layer dictionary (for later access)
        layer.setdefault(key, rounded_Bo)                                                           #store rounded incident beam attenuation of layer
        Bo_previous = Bo                                                                            #attenuation calculated for this layer to be used as incident beam intensity of next layer (when the for loop moves to next layer, Bo_previous is now the value calculated for previous layer)
    return

IncidentBeamAttenuation(STACK)


#outgoing fluorescence of external layers
def get_capXsect_of_layer_on_ele_line(layer, layer_element_list):
    for ele in layer_element_list:
        ext_layer_capXsect_on_ele_line = xl.CS_Total_CP(layer["Name"], get_Ele_XRF_Energy(ele, beam_energy))
    return ext_layer_capXsect_on_ele_line

for layer_num, layer in enumerate(STACK):
    prev_layers = STACK[:layer_num]                             #return list containing dictionaries of previous layers
    layer_ele_line_muS = []
    for prev_layer in prev_layers:
        mu_layer_ele_line = get_capXsect_of_layer_on_ele_line(prev_layer, layer["Element"])
        
        layer_ele_line_muS.append(mu_layer_ele_line)
        print(prev_layer["Name"], layer_ele_line_muS)

#for CdTe layer

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
