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

# returns the highest energy XRF photon of an element due to the beam energy
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


###         defs BELOW dependent ###
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