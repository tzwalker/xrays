# -*- coding: utf-8 -*-
"""
Trumann
Mon Oct 14 10:43:17 2019
"""
import numpy as np
import xraylib as xl
import samp_dict_grow

def get_upstream_iioIN(layers_before, beam_settings):
    # convert to radians
    beam_rad = np.sin(beam_settings['beam_theta']*np.pi/180) 
    iios = []
    for layer, layer_info in layers_before.items():
        # capture cross-section of upstream layer
        sigma = xl.CS_Total_CP(layer, beam_settings['beam_energy'])
        # layer density and thickness
        density = layer_info[0]; thickness = layer_info[1] 
        
        iio = np.exp(- sigma * density * thickness / beam_rad) # layer transmission
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

def get_upstream_iioOUT(layers_before, elements, beam_settings):
    det_rad = np.sin(beam_settings['detect_theta']*np.pi/180)
    elements = [element[0:2] for element in elements] # remove XRF line for easy str searches
    XRF_lines = [eleXRF_energy(element, beam_settings['beam_energy']) for element in elements]
    upstream_iios_out = [] # holds cumulative atten. coeff. of each layer for each imported element
    for XRF_line in XRF_lines:
        tmp_iios = [] # holds the atten. coeff. of each layer for one element
        for layer, layer_info in layers_before.items():
            sigma = xl.CS_Total_CP(layer,XRF_line)
            density=layer_info[0];      thickness=layer_info[1]
            iio = np.exp(- sigma * density * thickness / det_rad) # Beer-Lambert
            tmp_iios.append(iio)
        # find cumulative atten. coeff. of each layer for one element
        upstream_ele_iio = np.prod(tmp_iios) 
        upstream_iios_out.append(upstream_ele_iio)
    upstream_iios_out = np.array(upstream_iios_out)
    return upstream_iios_out

def get_avg_internal_attn(layer_info, elements, beam_settings, cum_upstrm_attn):
    beam_energy = beam_settings['beam_energy']
    beam_rad = np.sin(beam_settings['beam_theta']*np.pi/180)
    det_rad = np.sin(beam_settings['detect_theta']*np.pi/180)
    density=layer_info[0];    thickness=layer_info[1];      step_size=1*10**-7  # 1nm steps
    
    XRF_lines = [eleXRF_energy(element, beam_energy) for element in elements]
    thickness_nm = int(thickness * 1E7)
    sublayers_array = np.linspace(0, thickness_nm, thickness_nm+1)
    ele_avg_iios = []
    for ele_idx, XRF_line in enumerate(XRF_lines):
        each_sublayer_iio = np.zeros(len(sublayers_array))
        sigma_sublayer_in = - xl.CS_Total_CP(layer, beam_energy) * density * step_size / beam_rad
        sigma_sublayer_out = - xl.CS_Total_CP(layer, XRF_line) * density * step_size / det_rad
        for sub_idx,sublayer in enumerate(sublayers_array):
            iio_in = sigma_sublayer_in * sublayer 
            iio_out = sigma_sublayer_out * sublayer
            each_sublayer_iio[sub_idx] = cum_upstrm_attn[ele_idx] * np.exp(iio_in + iio_out)
        ele_avg_iio = np.mean(each_sublayer_iio)
        ele_avg_iios.append(ele_avg_iio)
    ele_avg_iios = np.array(ele_avg_iios)
    return ele_avg_iios

def get_layer_iios(samples, elements, beam_settings, layer):
    iio_arrays = []
    for sample in samples:
        STACK = sample['STACK']
        layer_idx=list(STACK.keys()).index(layer)
        if layer_idx != 0:
            # retrieve info of upstream layers
            layers_before = {k:v for idx,(k,v) in enumerate(STACK.items()) if idx < layer_idx}
            # percent incoming beam transmitted to layer
            upstream_attn_in = get_upstream_iioIN(layers_before, beam_settings)
            # percent outgoing XRF transmitted by upstream layers
            upstream_attn_out = get_upstream_iioOUT(layers_before, elements, beam_settings)
            cumulative_upstream_attenuation = upstream_attn_in * upstream_attn_out
            # percent outgoing XRF transmitted
            ele_avg_iios = get_avg_internal_attn(STACK[layer], elements, beam_settings, cumulative_upstream_attenuation)
            # ... deciding how to best store the iios for convenient application to scans from different beam times
            # samp_dict_grow.build_dict(sample, 'avg_iios', ele_avg_iios)
        else:
            print('you have chosen the first layer of the stack.')
            print('this program is not currently configured to calculate element iios for the first layer.')
            print('please either enter another layer, or look into modifying this function')
    return # ...

beam_settings = {'beam_energy': 8.99, 'beam_theta':90, 'detect_theta':43}
layer = 'CdTe'
elements_for_iios = ['Cu', 'Cd', 'Te'] 
get_layer_iios(samples, elements_for_iios, beam_settings, layer) # ... 
    

# if Cu is not considered mono-layer, simply exclude it from the stack entries in the sample dicts
    # one may still calculate Cu attn. if no Cu layer is present
    # the thickness of the monolayer produces a very small difference in the avg iio results
        # and whether it is included or not is negligible
# can one estimate the placement/thickness of the Cu layer better using SIMS or xsect XRF?
# ran code for 75 degree geometry and got identical cumulative_upstream attenuation
    # as those from Reabsorption Explore Plots slide 42 in consolidated notes1.ppt

# stuff to include in ReadMe
    # cumulative_upstream_attenuation returns array of corresponding iios for element string included in "elements_for_iios", 
    # the user must decide which iios are relevant
        # for example, if the stack is Mo/ZnTe/CdTe/CdS/SnO2, 
        # the upstream atten. of Mo is meaningless as it is the top layer
    # the program is not configured for calculating iios of only the top layer
        # though it should easily be adaptable to perform such calculation
    # 