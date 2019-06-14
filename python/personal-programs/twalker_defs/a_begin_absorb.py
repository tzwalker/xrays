import xraylib as xl
import numpy as np

#returns a list of dictionaries
#each dictionary contains information on the layer to be used in the absorption correction
def get_stack_info(STACK, layer_density, E):
    STACK_dicts = []
    for layer, dens in zip(STACK, layer_density):
        layer_dict = dict()
        key = 'Name'
        layer_dict.setdefault(key, layer)
        key = 'rho'
        layer_dict.setdefault(key, dens)
        key = 'cap-x-sect'
        capture = xl.CS_Total_CP(layer, E)
        layer_dict.setdefault(key, capture)
        
        layer_info = xl.CompoundParser(layer)
        #example for SnO2
        #layer_info = {'nElements': 2, 
                        #'nAtomsAll': 3.0, 
                        #'Elements': [8, 50], 
                        #'massFractions': [0.21235649346340169, 0.7876435065365983], 
                        #'nAtoms': [2.0, 1.0], 
                        #'molarMass': 150.69}
        layer_dict.update(layer_info)
        
        STACK_dicts.append(layer_dict)
    return STACK_dicts

#returns the highest energy XRF photon of an element due to the beam energy
def get_Ele_XRF_Energy(Z, energy):
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
        #if-statements checks whether the element will absorb
        # ex) beam_energy = 12.7 keV
                #Cd_KA_SHELL = 26.7 
                #Cd_KA_SHELL !< 12.7 keV
                #move to next absorption edge
                #Cd_L1_SHELL = 4.018
                #Cd_L1_SHELL < 12.7 keV
                #XRF photon energy set to the highest energy transition of this shell
                #Cd_LA1_LINE = 3.081 keV = energy captured by other layers (this value is close to that obtained via NIST lookup methods)
    return F

def channel_to_atomic_num(channels):
    Zs_for_xraylib = []
    for e in channels:
        if len(e) <= 2: #--> K-line channel
            ele_string = e
        else:
            ele_string = e[:-2] #--> remove '_L' or '_M' from channel string        
    
        s = xl.SymbolToAtomicNumber(ele_string) # --> convert string to atomic number for use in xraylib
        Zs_for_xraylib.append(s)
    return Zs_for_xraylib

# check if element is in layer by its atomic number
def is_ele_in_layer(stack_list, ele_nums):
    es = []
    for layer_dict in stack_list:
        layer_eles = layer_dict['Elements']
        matched_elements = [e for e in layer_eles for Z in ele_nums if e == Z]
        es.append(matched_elements)
    return es

for layer_index, layer in enumerate(STACK):
    before_layers = get_previous_layers(layer_index, STACK) # need help with this function; returns list of layer dictionaries coming before 'layer'
    
def get_previous_layers(i, S):
    count = 0 
    before_list = []
    while i > count:
        before_dict = S[count]
        before_list.append(before_dict)
        count = count + 1
    return before_list

    
for layer_index, layer in enumerate(STACK):
    before_layers = get_previous_layers(layer_index, layer) # need help with this function; returns list of layer dictionaries coming before 'layer'
    
    iio_ins = []
    iio_outs = []
    for before_layer in before_layers:
        iio_in, iio_out = calc_external_layer_iios(before_layer)
        iio_ins.append(iio_in)
        iio_outs.append(iio_out)
    ext_iio = np.prod(iio_ins) * np.prod(iio_outs)
    


# =============================================================================
# #percent incoming beam transmitted to CdTe layer
# iio_Mo = np.exp(- MO['capXsect'] * MO['LDensity'] * MO['Thick'] / beam_geometry)
# iio_ZnTe = np.exp(- ZNTE['capXsect'] * ZNTE['LDensity'] * ZNTE['Thick'] / beam_geometry)
# 
# iio_in = iio_Mo * iio_ZnTe
# 
# #percent outgoing Cd_L transmitted by external layers
# Cd_L = get_Ele_XRF_Energy('Cd', beam_energy)
# 
# mu_Mo_Cd_L = xl.CS_Total_CP('Mo', Cd_L)         #1800 vs. 1872 (matlab)
# mu_ZnTe_Cd_L = xl.CS_Total_CP('ZnTe', Cd_L)     #653 vs. 680 (matlab)
# 
# cd_1 = np.exp(- mu_Mo_Cd_L * MO['LDensity'] * MO['Thick'] / detect_geometry)        # moly is a really good Cd_L and Te_L absorber, iio ~0.0287
# cd_2 = np.exp(- mu_ZnTe_Cd_L * ZNTE['LDensity'] * ZNTE['Thick'] / detect_geometry)
# 
# iio_out = iio_in * cd_1 * cd_2                  #0.0151 vs. 0.0163 (matlab)
# 
# #percent outgoing Cd_L transmitted by CdTe itself
# mu_CdTe_Cd_L = xl.CS_Total_CP('CdTe', Cd_L)
# steps = np.linspace(0, 12000, 12001)
# dt = 1*10**-7
# 
# iio_cd_cdte = np.zeros(len(steps))
# 
# cap_cross_section_of_one_sublayer_in = - CDTE['capXsect'] * CDTE['LDensity'] * dt / beam_geometry
# cap_cross_section_of_one_sublayer_out_CdL = - mu_CdTe_Cd_L * CDTE['LDensity'] * dt / detect_geometry
# 
# for index, step in enumerate(steps):
#     beam_in = cap_cross_section_of_one_sublayer_in * index;
#     beam_out = cap_cross_section_of_one_sublayer_out_CdL * index
#     iio_cd_cdte[index] = iio_out * np.exp(beam_in + beam_out)
#     
# iio_cdL = np.mean(iio_cd_cdte) #0.00117 vs. 0.0021 (matlab)
# 
# 
# =============================================================================
### code comparable to matlab, only for and up to CdTe layer, will work on later ###
# =============================================================================
# #percent incoming beam transmitted to CdTe layer
# iio_Mo = np.exp(- MO['capXsect'] * MO['LDensity'] * MO['Thick'] / beam_geometry)
# iio_ZnTe = np.exp(- ZNTE['capXsect'] * ZNTE['LDensity'] * ZNTE['Thick'] / beam_geometry)
# 
# iio_in = iio_Mo * iio_ZnTe
# 
# #percent outgoing Cd_L transmitted by external layers
# Cd_L = get_Ele_XRF_Energy('Cd', beam_energy)
# 
# mu_Mo_Cd_L = xl.CS_Total_CP('Mo', Cd_L)         #1800 vs. 1872 (matlab)
# mu_ZnTe_Cd_L = xl.CS_Total_CP('ZnTe', Cd_L)     #653 vs. 680 (matlab)
# 
# cd_1 = np.exp(- mu_Mo_Cd_L * MO['LDensity'] * MO['Thick'] / detect_geometry)        # moly is a really good Cd_L and Te_L absorber, iio ~0.0287
# cd_2 = np.exp(- mu_ZnTe_Cd_L * ZNTE['LDensity'] * ZNTE['Thick'] / detect_geometry)
# 
# iio_out = iio_in * cd_1 * cd_2                  #0.0151 vs. 0.0163 (matlab)
# 
# #percent outgoing Cd_L transmitted by CdTe itself
# mu_CdTe_Cd_L = xl.CS_Total_CP('CdTe', Cd_L)
# steps = np.linspace(0, 12000, 12001)
# dt = 1*10**-7
# 
# iio_cd_cdte = np.zeros(len(steps))
# 
# cap_cross_section_of_one_sublayer_in = - CDTE['capXsect'] * CDTE['LDensity'] * dt / beam_geometry
# cap_cross_section_of_one_sublayer_out_CdL = - mu_CdTe_Cd_L * CDTE['LDensity'] * dt / detect_geometry
# 
# for index, step in enumerate(steps):
#     beam_in = cap_cross_section_of_one_sublayer_in * index;
#     beam_out = cap_cross_section_of_one_sublayer_out_CdL * index
#     iio_cd_cdte[index] = iio_out * np.exp(beam_in + beam_out)
#     
# iio_cdL = np.mean(iio_cd_cdte) #0.00117 vs. 0.0021 (matlab)
# =============================================================================
    
    

