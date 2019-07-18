import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xraylib as xl

import sys
sys.path.append(r'C:\Users\Trumann\Desktop\XRF-dev\python\personal-programs\twalker_defs')

import import_MAPS_ASCII
## import XBIC_ehPairs --> defs from this module included in "defs_electrical_investigation.py"
  # change the references inside this file to point to that instead
  # e.g.
   #import defs_electrical_investigation as eiDefs (replace "XBIC_ehPairs")

# calcXCE, plotXCE moved to "old_ASCII_defs.py"

path_to_ASCIIs = r'C:\Users\Trumann\Desktop\2017_12_2018_07_NBL3_bacth_refit\output'

#enter energy in keV, stanford amplifcations in nanoamps, width/height in um, and elements of interest (EOI)
scan1 = {"sector": 2, 'Scan #': 439, 'Name': 'TS58A', 'width': 15, 'height': 15, 'x_points': 150, 'y_points': 150, 'beam_energy': 8.99, 'stanford': 200, 'lockin': 20, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 4359, "EOI": ['Sn_L', 'S', 'Cd_L', 'Te_L', 'Cu', 'Cl', 'Mo_L']} 
scan2 = {"sector": 2, 'Scan #': 475, 'Name': 'NBL3-3', 'width': 15, 'height': 15, 'x_points': 150, 'y_points': 150, 'beam_energy': 8.99, 'stanford': 200, 'lockin': 20, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 5680,  "EOI": ['Sn_L', 'S', 'Cd_L', 'Te_L', 'Cu', 'Cl', 'Mo_L']}
scan3 = {"sector": 2, 'Scan #': 519, 'Name': 'NBL3-1', 'width': 15, 'height': 15, 'x_points': 150, 'y_points': 150, 'beam_energy': 8.99, 'stanford': 200, 'lockin': 20, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 4787, "EOI": ['Sn_L', 'S', 'Cd_L', 'Te_L', 'Cu', 'Cl', 'Mo_L']}
scan4 = {"sector": 2, 'Scan #': 550, 'Name': 'NBL3-2', 'width': 15, 'height': 15, 'x_points': 150, 'y_points': 150, 'beam_energy': 8.99, 'stanford': 50000, 'lockin': 100, 'PIN beam_on': 105400, 'PIN beam_off': 510, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 5907, "EOI": ['Sn_L', 'S', 'Cd_L', 'Te_L', 'Cu', 'Cl', 'Mo_L']}

           
scan_list = [scan1, scan2, scan3, scan4]

imported_scans_dfs = import_MAPS_ASCII.shrinkASCII(scan_list, path_to_ASCIIs)
XBIC_ehPairs.generate_scalar_factor(scan_list)
XBIC_ehPairs.collect_XBIC(imported_scans_dfs, scan_list)
#interpolate_diode_calibration(scan_list)
#get_flux(scan_list)
#calc_XCE(imported_scans_dfs, scan_list)

# =============================================================================
# mapConvertAxes(imported_scans_dfs, scan_list)
# list_of_shaped_XCE_dfs = mapShape(imported_scans_dfs)
# plotXCE(scan_list, list_of_shaped_XCE_dfs)
# =============================================================================


#########################################################################################################################################################################
###BEGING FLUORESCENCE CALC

# =============================================================================
# beam_energy = 8.99                                                  #beamtime keV
# beam_theta = 90                                                     #angle of the beam relative to the surface of the sample
# beam_geometry = np.sin(beam_theta*np.pi/180)                        #convert to radians
# detect_theta = 47                                                   #angle of the detector relative to the beam
# detect_gemoetry = np.sin(detect_theta*np.pi/180)                    #convert to radians
# dt = 10 * (1*10**-3) * (1*10**-4)                                   #convert 10nm step sizes to cm: 10nm * (1um/1000nm) * (1cm/10000um)
# 
# #enter lengths in cm
# SNO2 =  {'Element':['Sn','O'],      'MolFrac':[1,2],    'Thick':0.00006,    'LDensity': 6.85, 'Name': 'SnO2',   'capXsect': xl.CS_Total_CP('SnO2', beam_energy)}
# CDS =   {'Element':['Cd','S'],      'MolFrac':[1,1],    'Thick':0.000008,   'LDensity': 4.82, 'Name': 'CdS',    'capXsect': xl.CS_Total_CP('CdS', beam_energy)}
# CDTE =  {'Element':['Cd','Te'],     'MolFrac':[1,1],    'Thick':0.0005,    'LDensity': 5.85, 'Name': 'CdTe',   'capXsect': xl.CS_Total_CP('CdTe', beam_energy)}
# CU =    {'Element':['Cu'],          'MolFrac':[1],      'Thick':0.000001,   'LDensity': 8.96, 'Name': 'Cu',     'capXsect': xl.CS_Total_CP('Cu', beam_energy)}
# ZNTE =  {'Element':['Zn','Te'],     'MolFrac':[1,1],    'Thick':0.0000375,  'LDensity': 6.34, 'Name': 'ZnTe',   'capXsect': xl.CS_Total_CP('ZnTe', beam_energy)}
# MO =    {'Element':['Mo'],          'MolFrac':[1],      'Thick':0.00005,    'LDensity': 10.2, 'Name': 'Mo',     'capXsect': xl.CS_Total_CP('Mo', beam_energy)}
# 
# #COMBINE THE LAYERS FROM ABOVE INTO A LIST (UPTREAM LAYER FIRST, DOWNSTREAM LAYER LAST)
# STACK = [MO, ZNTE, CU, CDTE, CDS, SNO2]
# 
# def getSublayers(layer):
#     T = layer['Thick']                                          #layer thickness in cm
#     sublayers = T/dt                                            #number of 10nm sublayers in the layer
#     sublayers = round(sublayers)
#     sublayers = int(sublayers)
#     key = 'numSublayers'                                        #add key to layer dictionary (for convenience)
#     layer.setdefault(key, sublayers)                            #connect key to number of sublayers calculated
#     return sublayers
# 
# #attenuation of beam intensity through each layer
# Bo_previous = 1
# for layer in STACK:
#     Bo = Bo_previous * np.exp(- layer['capXsect'] * layer['LDensity'] * layer['Thick']) #cm2/g * g/cm3 * cm
#     rounded_Bo = round(Bo, 7)
#     Bo_previous = Bo
#     #begin correction internal to each layer
#     sublayers = getSublayers(layer)
#     path_in = np.zeros(layer['numSublayers'])
#     path_out = np.zeros(layer['numSublayers'])
#     for sublayer in range(sublayers):
#         path_in[sublayer] = -layer['LDensity'] * layer['capXsect'] * dt / beam_geometry
#         path_out[sublayer] = -layer['LDensity'] * layer['capXsect'] * dt / detect_gemoetry        
#     #print(path_in, path_out)
# 
# =============================================================================
