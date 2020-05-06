import numpy as np
import xraylib as xl

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

def get_char_depth(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def get_avg_internal_attn(layer_info, layer, elements, beam_settings, cum_upstrm_attn):
    beam_energy = beam_settings['beam_energy']
    beam_rad = np.sin(beam_settings['beam_theta']*np.pi/180)
    det_rad = np.sin(beam_settings['detect_theta']*np.pi/180)
    
    density=layer_info[0]
    thickness=layer_info[1]
    step_size=1*10**-7  # 1nm steps
    
    XRF_lines = [eleXRF_energy(element, beam_energy) for element in elements]
    thickness_nm = int(thickness * 1E7)
    sublayers_array = np.linspace(0, thickness_nm, thickness_nm+1)
    ele_avg_iios = []
    for ele_idx, XRF_line in enumerate(XRF_lines):
        each_sublayer_iios = np.zeros(len(sublayers_array))
        sigma_sublayer_in = - xl.CS_Total_CP(layer, beam_energy) * density * step_size / beam_rad
        sigma_sublayer_out = - xl.CS_Total_CP(layer, XRF_line) * density * step_size / det_rad
        for sub_idx,sublayer in enumerate(sublayers_array):
            iio_in = sigma_sublayer_in * sublayer 
            iio_out = sigma_sublayer_out * sublayer
            each_sublayer_iios[sub_idx] = cum_upstrm_attn[ele_idx] * np.exp(iio_in + iio_out)
        ### new proposed correction ###
        depth_idx_iio_bound = each_sublayer_iios[0] * (1/np.e)
        characteristic_depth = get_char_depth(each_sublayer_iios, depth_idx_iio_bound)
        ele_avg_iio = np.mean(each_sublayer_iios[:characteristic_depth])
        #print(ele_avg_iio)
        ele_avg_iios.append(ele_avg_iio)
    ele_avg_iios = np.array(ele_avg_iios)
    return ele_avg_iios

def get_iios(beam_settings, elements, STACK, end_layer):
    # clip XRF line for xraylib
    elements = [element[0:2] for element in elements]
    # check if first layer was chosen
    layer_idx=list(STACK.keys()).index(end_layer)
    if layer_idx != 0:
        # retrieve info of upstream layers
        layers_before = {k:v for idx,(k,v) in enumerate(STACK.items()) if idx < layer_idx}
        # percent incoming beam transmitted to layer
        upstream_attn_in = get_upstream_iioIN(layers_before, beam_settings)
        # percent outgoing XRF transmitted by upstream layers
        upstream_attn_out = get_upstream_iioOUT(layers_before, elements, beam_settings)
        cumulative_upstream_attenuation = upstream_attn_in * upstream_attn_out
        # percent outgoing XRF transmitted
        ele_avg_iios = get_avg_internal_attn(STACK[end_layer], end_layer, elements, 
                                             beam_settings, cumulative_upstream_attenuation)
    else:
        print('you have chosen the first layer of the stack')
        print('this program cannot correct XRF for the first layer')
        print('please enter another layer')
    return ele_avg_iios


stack = {'Mo':   [10.2, 500E-7], 
                 'ZnTe': [6.34, 375E-7], 
                 'Cu':   [8.96, 10E-7], 
                 'CdTe': [5.85, 10.85E-4], 
                 'CdS':  [4.82, 80E-7], 
                 'SnO2': [100E-7]}

elements = ['Cu', 'Cd_L', 'Te_L', 'Cl']

beam_settings = {'beam_energy': 12.7, 'beam_theta':75, 'detect_theta':15}

iios2019 = get_iios(beam_settings, elements, stack, end_layer='ZnTe')