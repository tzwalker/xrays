import xraylib as xl
import numpy as np
import matplotlib.pyplot as plt

# returns highest energy photon fluoresced at the given beam energy
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

# values being compared in comments are for Cd_L
def iio_vs_depth(ele, t, dt):
    # percent incoming beam transmitted to CdTe layer
    iio_Mo = np.exp(- MO['capXsect'] * MO['LDensity'] * MO['Thick'] / beam_geometry)
    iio_ZnTe = np.exp(- ZNTE['capXsect'] * ZNTE['LDensity'] * ZNTE['Thick'] / beam_geometry)
    iio_in = iio_Mo * iio_ZnTe
    
    # percent outgoing Cd_L transmitted by external layers
    ele_line = get_Ele_XRF_Energy(ele, beam_energy)
    mu_Mo_ele_line = xl.CS_Total_CP('Mo', ele_line)             #1800 vs. 1872 (matlab)
    mu_ZnTe_Cd_ele_line = xl.CS_Total_CP('ZnTe', ele_line)      #653 vs. 680 (matlab)
    c_1 = np.exp(- mu_Mo_ele_line * MO['LDensity'] * MO['Thick'] / detect_geometry)        # moly is a really good Cd_L and Te_L absorber, iio ~0.0287
    c_2 = np.exp(- mu_ZnTe_Cd_ele_line * ZNTE['LDensity'] * ZNTE['Thick'] / detect_geometry)
    iio_out = iio_in * c_1 * c_2                                #0.0151 vs. 0.0163 (matlab)
    
    # percent outgoing Cd_L transmitted by CdTe itself
    mu_CdTe_ele = xl.CS_Total_CP('CdTe', ele_line)
    iio_ele_cdte = np.zeros(len(t))
    cap_cross_section_of_one_sublayer_in = - CDTE['capXsect'] * CDTE['LDensity'] * dt / beam_geometry
    cap_cross_section_of_one_sublayer_out_ele = - mu_CdTe_ele * CDTE['LDensity'] * dt / detect_geometry
    for index, step in enumerate(t):
        beam_in = cap_cross_section_of_one_sublayer_in * step;
        beam_out = cap_cross_section_of_one_sublayer_out_ele * step
        iio_ele_cdte[index] = iio_out * np.exp(beam_in + beam_out)
    #iio_ele = np.mean(iio_ele_cdte) #0.00117 vs. 0.0021 (matlab)
    return iio_ele_cdte


## define settings and stack parameters ##
beam_energy = 12.7 #keV
beam_theta = 75                                                     #angle of the beam relative to sample normal
beam_geometry = np.sin(beam_theta*np.pi/180)                        #convert to radians
detect_theta = 15                                                   #angle of the detector sample normal
detect_geometry = np.sin(detect_theta*np.pi/180)                    #convert to radians
# enter thickness of layer in cm
# only upstream layers are of interest
MO =    {'Thick':0.00005,    'LDensity': 10.2, 'Name': 'Mo',     'capXsect': xl.CS_Total_CP('Mo', beam_energy)}
ZNTE =  {'Thick':0.0000375,  'LDensity': 6.34, 'Name': 'ZnTe',   'capXsect': xl.CS_Total_CP('ZnTe', beam_energy)}
CDTE =  {'Thick':0.0012000,  'LDensity': 5.85, 'Name': 'CdTe',   'capXsect': xl.CS_Total_CP('CdTe', beam_energy)}

# enter element for which you wish to see I/Io (will work on generatign plots for many elements at once)
ele = 'Cu'

# specify arbitrary depth of absorber
no_rough = np.linspace(0, 12000, 12001)               #(nm) arbitrary absorber depth of 12um;
dt = 1*10**-7                                       # 1nm = 1E-7cm
no_rough_iio = iio_vs_depth(ele, no_rough, dt)      #calc reference profile
no_rough_converted = (no_rough/1000).reshape(-1,1)
save_arr = np.concatenate((no_rough_converted, no_rough_iio.reshape(-1,1)), axis=1)

np.savetxt(r'C:\Users\triton\iio_sim_' + str(detect_theta) +'deg.csv', save_arr, delimiter=',')
plt.plot(no_rough, no_rough_iio)


# =============================================================================
# # specfiy roughness parameters
# roughnesses = np.linspace(0.05, 0.2, 3)
# rough_ups, rough_downs = gen_upd_and_downs(roughnesses)
# ele_rough_iios_up, ele_rough_iios_down = gen_up_down_iios(rough_ups, rough_downs)
# no_rough_in_um = no_rough / 1000        #for proper x-axis units while plotting
# 
# def gen_upd_and_downs(r):
#     rough_ups = []
#     rough_downs = []
#     for roughness in roughnesses:
#         rough_up = no_rough * (1+roughness)
#         rough_down = no_rough * (1-roughness)
#         rough_ups.append(rough_up)
#         rough_downs.append(rough_down)
#     return rough_ups, rough_downs
# 
# def gen_up_down_iios(rough_ups, rough_downs):
#     ele_rough_iios_up = []
#     for roughness in rough_ups:
#         ele_rough_iio_up = iio_vs_depth(ele, roughness, dt)
#         ele_rough_iios_up.append(ele_rough_iio_up)
#     
#     ele_rough_iios_down = []
#     for roughness in rough_downs:
#         ele_rough_iio_down = iio_vs_depth(ele, roughness, dt)
#         ele_rough_iios_down.append(ele_rough_iio_down)
#     return ele_rough_iios_up, ele_rough_iios_down
# =============================================================================

# iio vs. depth() is essentially the same as the calculation seen in absorb_matlib_v_xraylib
# only dependency iio_vs_depth() has on CdTe thickness is seen in the "no_rough" variable
    # an arbitrarily large 12um thickness was chosen to calculate iio through the entirety of a thick cdte layer
    # slicing iio to thickness found from SIMS (slide 60 in "NBL3 consolidated notes.ppt"), then averaging will
    # yield mean iio correction factor for Cu in all samples
    # enter these factors somewhere into a_start.py, and apply them to Cu maps

# =============================================================================
# samp_cdte_thicknesses = [8516, 7745, 5320]
# samp_iios = []
# for s in samp_cdte_thicknesses:
#     mean_iio = np.mean(no_rough_iio[0:s])
#     samp_iios.append(mean_iio)
# =============================================================================

### plotting iio vs. CdTe thickness ###
# =============================================================================
# 
# # labels for legend are automatically genrated
# label_nums = roughnesses * 100
# label_list = []
# for num in label_nums:
#     b = int(num)
#     c = str(b)
#     d = '+/- ' + c + '%'
#     label_list.append(d)
# 
# # note these list lengths must be greater than or equal to the steps in 'roughnesses'
# color_list = ['r', 'b', 'g', 'c', 'm', 'r', 'b', 'g', 'c']
# line_list = ['--', '--','--','--', '--', '-.', '-.', '-.', '-.']
# # plot
# fig, ax = plt.subplots()
# plt.plot(no_rough_in_um, no_rough_iio, 'k', label = 'No roughness')
# for rough_down, rough_up, l, c, lab in zip(ele_rough_iios_down, ele_rough_iios_up, line_list, color_list, label_list):
#     plt.plot(no_rough_in_um, rough_down, linestyle = l, color = c, label = lab)
#     plt.plot(no_rough_in_um, rough_up, linestyle = l, color = c)
# # axis settings
# plt.xlabel('CdTe Thickness (um)', fontsize = 16)
# plt.ylabel('% ' + ele + ' Signal', fontsize = 16)
# ax.tick_params(axis = 'both', labelsize = 14) 
# plt.ylim([0, 1.0])
# plt.grid()
# ax.legend()
# plt.legend(prop={'size': 14})
# plt.show()
# =============================================================================
