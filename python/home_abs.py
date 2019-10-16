# -*- coding: utf-8 -*-
"""
Trumann
Mon Oct 14 10:43:17 2019
"""
import numpy as np
import xraylib as xl

def get_upstream_iioIN(layers_before, beam_settings):
    # convert to radians
    beam_theta = np.sin(beam_settings['beam_theta']*np.pi/180) 
    iios = []
    for layer, layer_info in layers_before.items():
        # capture cross-section of upstream layer
        sigma = xl.CS_Total_CP(layer, beam_settings['beam_energy'])
        # layer density and thickness
        density = layer_info[0]; thickness = layer_info[1] 
        # layer transmission
        iio = np.exp(- sigma * density * thickness / beam_theta) 
        iios.append(iio)
    upstream_iio = np.prod(iios) # cumulative transmission of upstream layers
    return upstream_iio

# =============================================================================
# def filter_layers(layers_before, upstream_elements):
#     # print(type(layers_before)) --> dict
#     ignored_layers = []
#     for up_layer in layers_before:
#         for element in upstream_elements:
#             if element in up_layer:
#                 ignored_layers.append(up_layer)        
#         print('dummy line')
#     return elements_to_ignore
# =============================================================================

def eleXRF_energy(ele, energy):
    Z = xl.SymbolToAtomicNumber(ele); F =  xl.LineEnergy(Z, xl.KA1_LINE)
    if   xl.EdgeEnergy(Z, xl.K_SHELL) > energy: F = xl.LineEnergy(Z, xl.LA1_LINE)
    elif xl.EdgeEnergy(Z, xl.L1_SHELL) > energy: F = xl.LineEnergy(Z, xl.LB1_LINE)
    elif xl.EdgeEnergy(Z, xl.L2_SHELL) > energy: F = xl.LineEnergy(Z, xl.LB1_LINE)
    elif xl.EdgeEnergy(Z, xl.L3_SHELL) > energy: F = xl.LineEnergy(Z, xl.LG1_LINE)
    elif xl.EdgeEnergy(Z, xl.M1_SHELL) > energy: F = xl.LineEnergy(Z, xl.MA1_LINE) 
    return F

def get_upstream_iioOUT(layers_before, elements, beam_settings):
    det_theta = np.sin(beam_settings['detect_theta']*np.pi/180)
    elements = [element[0:2] for element in elements] # remove XRF line for easy str searches
    XRF_lines = [eleXRF_energy(element, beam_settings['beam_energy']) for element in elements]
    upstream_iios_out = [] # holds cumulative atten. coeff. of each layer for each imported element
    for XRF_line in XRF_lines:
        tmp_iios = [] # holds the atten. coeff. of each layer for one element
        for layer, layer_info in layers_before.items():
            sigma = xl.CS_Total_CP(layer,XRF_line)
            density = layer_info[0]; thickness = layer_info[1]
            iio = np.exp(- sigma * density * thickness / det_theta) # Beer-Lambert
            tmp_iios.append(iio)
        upstream_ele_iio = np.prod(tmp_iios) # find cumulative atten. coeff. of each layer for one element
        upstream_iios_out.append(upstream_ele_iio)
    upstream_iios_out = np.array(upstream_iios_out)
    return upstream_iios_out

def get_layer_iios(samples, elements, beam_settings, layer):
    for sample in samples:
        STACK = sample['STACK']
        layer_idx=list(STACK.keys()).index(layer)
        if layer_idx != 0:
            # retrieve info of upstream layers
            layers_before = {k:v for idx,(k,v) in enumerate(STACK.items()) if idx < layer_idx}
            # percent incoming beam transmitted to layer
            upstream_attn_in = get_upstream_iioIN(layers_before, beam_settings)
            # percent outgoing XRF transmitted by upstram layers
            upstream_attn_out = get_upstream_iioOUT(layers_before, elements, beam_settings) # returns array of iios corresponding to all imported elements
            cumulative_upstream_attenuation = upstream_attn_in * upstream_attn_out
            print(cumulative_upstream_attenuation)
            # percent outgoing XRF transmitted by layer itself 
            #avg_internal_attenuation = get_avg_internal_attn(STACK[layer], elements)
            #final_iios = 
    return 

beam_settings = {'beam_energy': 8.99, 'beam_theta': 90, 'detect_theta':43}
layer = 'CdTe'; elements_for_iios = ['Cu', 'Cd', 'Te'] 
layer_iios = get_layer_iios(samples, elements_for_iios, beam_settings, layer)

# should the user include upstream layers for iio_out calc...
    # do not generate iio if element is in a upstream layer...?
    #neglected_elements = filter_layers(layers_before, upstream_elements) # ... 
    
# can i estimate the placement/thickness of the Cu layer better using SIMS or xsect XRF...?

# =============================================================================
# step_size = 1*10**-7  # 1nm steps
# STACK = sample['STACK']
# # there needs to be some mechanism that recognizes the layer we are on, what elements come before it, and what elements are inside of it...
#     # percent outgoing transmitted by external layers
#     
#     # percent outgoing Cd_L transmitted by CdTe itself
# =============================================================================

# stuff to include in ReadMe
    # cumulative_upstream_attenuation returns array of corresponding iios for all imported elements, though not all of them may be relevant
    # for example, if the stack is Mo/ZnTe/CdTe/CdS/SnO2, the upstream atten. of Mo is meaningless
    # therefore, the user must exercise caution when accessing these arrays, 