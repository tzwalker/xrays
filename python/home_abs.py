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

def get_avg_internal_attn(layer_info, layer, elements, beam_settings, cum_upstrm_attn):
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
            ele_avg_iios = get_avg_internal_attn(STACK[layer], layer, elements, 
                                                 beam_settings, cumulative_upstream_attenuation)
            #print(ele_avg_iios)
            #iio_arrays.append(ele_avg_iios)
            samp_dict_grow.build_dict(sample, beam_settings['beamtime']+'_iios', ele_avg_iios)
        else:
            print('you have chosen the first layer of the stack.')
            print('this program is not currently configured to calculate element iios for the first layer.')
            print('please either enter another layer, or look into modifying this function')
    return 

def apply_iios(samples, electrical_key, scan_ranges, iio_arr_key, ele_map_idxs, ele_iio_idxs):    
    for sample, scan_range in zip(samples, scan_ranges):
        correct_scans = []
        iio_arr = sample[iio_arr_key]
        # if only one scan is imported
        if len(scan_range) == 1:
            scan_raw_maps = sample[electrical_key+'_maps'][scan_range[0]]
            correct_maps = scan_raw_maps.copy() # create copy to overwrite
            for ele_idx, iio_idx in zip(ele_map_idxs, ele_iio_idxs):
                map_to_correct = scan_raw_maps[ele_idx,:,:] # extract map
                correct_map = map_to_correct / iio_arr[iio_idx] # correct map
                correct_maps[ele_idx,:,:] = correct_map # store map
            correct_scans.append(correct_maps)
            samp_dict_grow.build_dict(sample, '{e_key}{dat_key}_corr'.format(e_key=electrical_key, dat_key=iio_arr_key[0:8]), correct_scans)
        else:
            scans = sample[electrical_key+'_maps'][scan_range[0]:scan_range[1]]
            for scan_raw_maps in scans:
                # to apply to correct map
                correct_maps = scan_raw_maps.copy() # create copy to overwrite
                for ele_idx, iio_idx in zip(ele_map_idxs, ele_iio_idxs):
                    map_to_correct = scan_raw_maps[ele_idx,:,:] # extract map
                    correct_map = map_to_correct / iio_arr[iio_idx] # correct map
                    correct_maps[ele_idx,:,:] = correct_map # store map
                correct_scans.append(correct_maps)
            samp_dict_grow.build_dict(
                    sample, 
                    '{e_key}{dat_key}_corr'.format(e_key=electrical_key, dat_key=iio_arr_key[0:8]), 
                    correct_scans)
    return 

if __name__ == "__main__":
    beam_settings0 = {'beamtime': '2017_12','beam_energy': 8.99, 'beam_theta':90, 'detect_theta':43}
    beam_settings1 = {'beamtime': '2019_03','beam_energy': 12.7, 'beam_theta':75, 'detect_theta':15}
    layer = 'CdTe'
    elements_for_iios = ['Cu', 'Cd', 'Te'] # enter in same order as seen in 'elements'
    get_layer_iios(samples, elements_for_iios, beam_settings0, layer)
    get_layer_iios(samples, elements_for_iios, beam_settings1, layer)
    ele_map_idxs = [1,2,3] ; ele_iio_idxs = [0,1,2] # have user set these 
    
    cv_ranges=[[0,3], [0,3], [0,3]] # to avoid having to enter same amount of scans in each dictionary
    apply_iios(samples, 'XBIC', cv_ranges, '2019_03_iios', ele_map_idxs, ele_iio_idxs) 
    apply_iios(samples, 'XBIV', cv_ranges, '2019_03_iios', ele_map_idxs, ele_iio_idxs) 
    
    c_ranges=[[4,6], [4,5], [4,6]]
    apply_iios(samples, 'XBIC', c_ranges, '2017_12_iios', ele_map_idxs, ele_iio_idxs)
    
    v_ranges=[[3], [3], [3]]
    apply_iios(samples, 'XBIV', v_ranges, '2017_12_iios', ele_map_idxs, ele_iio_idxs)
    
    # combine the XBIC and XBIV maps: NBL3_2['XBIC2019_03_corr'] + NBL3_2['XBIC2017_12_corr']
        # after this operation, a list with corrected maps will mirror that of the original scan list
# apply_iios can be run on different scans in the XBIC and XBIV lists
    # corrected maps will be stored in a list identical to the raw map lists
        # then stored in the sample dictionary with whatever dict_key is given 
        # as second argument (e.g. '2019_03_corr') 
    # future processing will have to recombine the fractured lists for each sample, i.e.
        #apply_iios(samples, '2019_03_corr', 'XBIC', [0,3], 2019_03_matrix) --> NBL3_2['XBIc2019_03_corr']
        #apply_iios(samples, '2019_03_corr', 'XBIV', [0,3], 2019_03_matrix) --> NBL3_2['XBIV2019_03_corr']
        #apply_iios(samples, '2017_12_corr', 'XBIC', [4,7], 2017_12_matrix) --> NBL3_2['XBIC2017_12_corr']
        #apply_iios(samples, '2017_12_corr', 'XBIV', [4,7], 2017_12_matrix) --> NBL3_2['XBIv2017_12_corr']
        # an apply_iio line will have to exist for 
            # both XBIC and XBIV sets of scasn run at different beamtimes
    # combine fractured dict entries back together after correction:
        # NBL3_2['2019_03_corr'] + NBL3_2['2017_12_corr']
    # same will have to be done with XBIV scans
    
# =============================================================================
# elements = ['Cu', 'Cd_L', 'Te_L', 'Mo_L']
# elements_for_iios = ['Cu', 'Te', 'Cd']
# elements = [element[0:2] for element in elements]
# idxs_for_correction = np.array([imported_eles.index(e) for e in imported_eles for i in iio_eles if e==i])
# matched_ele_index = [elements.index(e) for e in elements for i in elements_for_iios if e==i]
# =============================================================================

# =============================================================================
# for sample, (sort_key, scans) in zip(samples, sorted_scans.items()):
#     if sample['Name'] == sort_key:
#         sample_scans = scans
#         #scans_to_correct = [sample['XBIC_scans'].index(scan_num) for scan_num in scans if scan_num in scans]
#         print(sample_scans)
# =============================================================================
            