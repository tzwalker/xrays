import xraylib as xl
import numpy as np

def eStringToAtomicNum(e):
    if len(e) <= 2: #--> K-line channel
        ele_string = e
    else:
        ele_string = e[:-2] #--> remove '_L' or '_M' from channel string        
    s = xl.SymbolToAtomicNumber(ele_string) # --> convert string to atomic number for use in xraylib
    return s
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

# 1
def test_fxn(ChOIs, LoLoDicts):    
    #matched_list_of_lists = []
    for scan_stack in LoLoDicts:
        #ele_nums = []
        for e in ChOIs:
            ele_num = eStringToAtomicNum(e)
            # use ele_num to find ele_of_interest in the layers of a scan_stack
            ele_check = is_ele_in_layer(scan_stack, ele_num)

    return 

#returns the energy of fluorescent photon of a given element due to the beam energy
#if-statements checks whether the element will absorb; is absorption edge higher than beam_energy?
    #if yes, no absorption, fluorescent photon energy is set to the next highest energy of the next shell
        # ex) Cd_L = 3.1338 keV , Cd_K_edge = 26.7, Cd_L_edge = 4.018
        #       
    #if no, absorption, fluorescent photon energy remains at the highest energy of the current shell
    
    ##functions of interest!
    #element_XRF_energy = xl.LineEnergy(xl.SymbolToAtomicNumber("element"), xl.XRF line you want)
    #Layer_cataching_ele_XRF = xl.CS_Total_CP("layer", element_XRF_energy)
#if-statements checks whether the element will absorb
# ex) beam_energy = 12.7 keV
		#Cd_KA_SHELL = 26.7 
		#Cd_KA_SHELL !< 12.7 keV
		#move to next absorption edge
		#Cd_L1_SHELL = 4.018
		#Cd_L1_SHELL < 12.7 keV
		#XRF photon energy set to the highest energy transition of this shell
		#Cd_LA1_LINE = 3.081 keV = energy captured by other layers (this value is close to that obtained via NIST lookup methods)
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

# check if element is in all layers by its atomic number
def is_ele_in_layer(stack_list, ele_nums):
    es = []
    for layer_dict in stack_list:
        layer_eles = layer_dict['Elements']
        matched_elements = [e for e in layer_eles for Z in ele_nums if e == Z]
        es.append(matched_elements)
    return es

import xraylib as xl


def get_stack_info(STACKS, dens, T, E):
    stack_whole_info = []
    for S, D, t, e in zip(STACKS, dens, T, E):
        stack_layer_infos = []
        for layer, density, thickness in zip(S, D, t): 
            scan_layer_dict = dict()
            key = 'Name'
            scan_layer_dict.setdefault(key, layer)
            
            key = 'rho'
            scan_layer_dict.setdefault(key, density)
        
            key = 'cap-x-sect'
            capture = xl.CS_Total_CP(layer, e)
            scan_layer_dict.setdefault(key, capture)
    
            key = 'thick'
            scan_layer_dict.setdefault(key, thickness)
            
            layer_info = xl.CompoundParser(layer)
        #example for SnO2
        #layer_info = {'nElements': 2, 
                        #'nAtomsAll': 3.0, 
                        #'Elements': [8, 50], 
                        #'massFractions': [0.21235649346340169, 0.7876435065365983], 
                        #'nAtoms': [2.0, 1.0], 
                        #'molarMass': 150.69}
            scan_layer_dict.update(layer_info)
            stack_layer_infos.append(scan_layer_dict)
        
        stack_whole_info.append(stack_layer_infos)
    return stack_whole_info


### defs BELOW dependent ###
def get_previous_layers(i, S):
    count = 0 
    before_list = []
    while i > count:
        before_dict = S[count]
        before_list.append(before_dict)
        count = count + 1
    return before_list

def calc_external_layer_iios(layer):
    iio_in_layer = np.exp(- layer['cap-x-sect'] * layer['rho'] * layer['thick']) #need to include thicknesses of layers in stack_info
    
    #ele_string = # how to input elements of interest here?
    ele_XRF = get_Ele_XRF_Energy(ele_string, beam_energy)
    #iio_out_layer = np.exp( - 
    return iio_in #,iio_out

# =============================================================================
# for layer_index, layer in enumerate(stack_info):
#     before_layers = get_previous_layers(layer_index, stack_info)
#     iio_ins = []
#     iio_outs = []
#     for before_layer in before_layers:
#         iio_in, iio_out = calc_external_layer_iios(before_layer)
#         iio_ins.append(iio_in)
#         iio_outs.append(iio_out)
#     ext_iio = np.prod(iio_ins) * np.prod(iio_outs)
# =============================================================================
###         defs ABOVE dependent ###


import xraylib as xl

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

