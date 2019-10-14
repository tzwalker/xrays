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
        sigma = xl.CS_Total_CP(layer, beam_settings['beam_energy']) #capture cross-section of upstream layer
        density = layer_info[0]; thickness = layer_info[1] # layer density and thickness
        iio = np.exp(- sigma * density * thickness / beam_theta) # layer transmission
        iios.append(iio)
    upstream_iio = np.prod(iios) # cumulative transmission of upstream layers
    return upstream_iio

def eleXRF_energy(ele, energy):
    Z = xl.SymbolToAtomicNumber(ele); F =  xl.LineEnergy(Z, xl.KA1_LINE)
    if   xl.EdgeEnergy(Z, xl.K_SHELL) > energy: F = xl.LineEnergy(Z, xl.LA1_LINE)
    elif xl.EdgeEnergy(Z, xl.L1_SHELL) > energy: F = xl.LineEnergy(Z, xl.LB1_LINE)
    elif xl.EdgeEnergy(Z, xl.L2_SHELL) > energy: F = xl.LineEnergy(Z, xl.LB1_LINE)
    elif xl.EdgeEnergy(Z, xl.L3_SHELL) > energy: F = xl.LineEnergy(Z, xl.LG1_LINE)
    elif xl.EdgeEnergy(Z, xl.M1_SHELL) > energy: F = xl.LineEnergy(Z, xl.MA1_LINE) 
    return F

def get_upstram_iioOUT(layers_before, elements, beam_settings):
    det_theta = np.sin(beam_settings['detect_theta']*np.pi/180)
    XRF_lines = [eleXRF_energy(element, beam_settings['beam_energy']) for element in elements]
    for XRF_line in XRF_lines:
        iios = []
        for layer, layer_info in layers_before.items():
            sigma = xl.CS_Total_CP(layer,XRF_line)
            density = layer_info[0]; thickness = layer_info[1]
            iio = np.exp(- sigma * density * thickness / det_theta)
            iios.append(iio)
        upstream_ele_iio = np.prod(iios)
        print(upstream_ele_iio)
    print()
    return

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
            upstream_attn_out = get_upstram_iioOUT(layers_before, elements, beam_settings)
            #print(upstream_attn_out)
            layer_info = STACK[layer]
# =============================================================================
#         if layer in STACK.items():
#             layer_idx = arg
#         #element_iios = [calc_iio(sample, element, beam_settings) for element in elements]
#         # remember to save the iios
# =============================================================================
    return 
beam_settings = {'beam_energy': 8.99, 'beam_theta': 90, 'detect_theta':43}
layer = 'CdTe'; upstream_elements = ['Mo', 'Zn', 'Te'] 
# should the user include upstream layers for iio_out calc; can i estimate the placement/thickness of the Cu layer better using SIMS or xsect XRF...?
layer_iios = get_layer_iios(samples, elements, beam_settings, layer)

# =============================================================================
# step_size = 1*10**-7  # 1nm steps
# STACK = sample['STACK']
# # there needs to be some mechanism that recognizes the layer we are on, what elements come before it, and what elements are inside of it...
# 	# build previous layers object...?
# for layer_idx, layer in enumerate(STACK.items()):
#     compound, layer_info = layer[0], layer[1]
#     
#     iio_in = get_prefactor(layer_idx, compound) #analogous to iio_in in iio_v_thick_sim.py/iio_vs_depth
# 		#...
#     # percent outgoing transmitted by external layers
#     
#     # percent outgoing Cd_L transmitted by CdTe itself
# =============================================================================
