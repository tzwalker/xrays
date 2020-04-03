import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as tkr

import definitions ASCII as old_ascii

# this files takes asciis of the scans below and only plots them
# need to sys append path, as well as locate these scans
path_to_ASCIIs = r'C:\Users\Trumann\Desktop\ASCII\FS'

#enter energy in keV, stanford amplifcations in nanoamps, width/height in um, (x_y_points - 1), and elements of interest (EOI)
scan1 = {"sector": 2, 'Scan #': '087', 'Name': 'FS1_1', 
'width': 10, 'height': 30, 
'x_points': 200, 'y_points': 600, 
'x_ticks': 100,  'y_ticks': 100,  
'beam_energy': 12.8, 'stanford': 500, 'lockin': 100, 
'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, 
"absorber_Eg": 1.45, 'E_abs': 4359, 
"EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L'], 
'figure_size': (5,5)} 
scan2 = {"sector": 2, 'Scan #': 551, 'Name': 'FS2_1', 'width': 10, 'height': 20, 'x_points': 100, 'y_points': 200, 'x_ticks': 50,    'y_ticks': 25,        'beam_energy': 12.8, 'stanford': 5000, 'lockin': 2000, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 5680,  "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L'], 'figure_size': (5,4)}
scan3 = {"sector": 2, 'Scan #': 661, 'Name': 'FS2_2', 'width': 15, 'height': 20, 'x_points': 150, 'y_points': 200, 'x_ticks': 50, 'y_ticks': 25,               'beam_energy': 10.4, 'stanford': 100, 'lockin': 2000, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 4787, "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L'], 'figure_size': (5, 4)}
scan4 = {"sector": 26, 'Scan #': 100, 'Name': 'FS2_2', 'width': 4, 'height': 4, 'x_points': 100, 'y_points': 100, 'x_ticks': 25,   'y_ticks': 25, 'beam_energy': 10.4, 'stanford': 200, 'lockin': 200, 'PIN beam_on': 105400, 'PIN beam_off': 510, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 5907, "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'Sn_L']}

element_plot_list = ['Cu', 'Te_CdTe']#, 'Cu', 'Zn', 'As', 'Se', 'Sn_L']
element_plot_labels = ['ug/cm2', 'at. %']#, 'ug/cm2', 'ug/cm2', 'ug/cm2', 'ug/cm2', 'ug/cm2']
        
scan_list = [scan1, scan2, scan3, scan4]

old_ascii.imported_scan_dfs = shrinkASCII(scan_list)
old_ascii.generate_scalar_factor(scan_list)
old_ascii.collect_XBIC(imported_scan_dfs)
#old_ascii.interpolate_diode_calibration(scan_list)
#old_ascii.get_flux(scan_list)
#old_ascii.calc_XCE(XCE_corrected_dfs, scan_list)

old_ascii.mapConvertAxes(imported_scan_dfs, scan_list)
shaped_dfs = old_ascii.mapShape(imported_scan_dfs)
#old_ascii.plotXCE(scan_list, shaped_dfs)

old_ascii.CdTe_ratio(imported_scan_dfs)
old_ascii.mapShapeEle(imported_scan_dfs, scan_list)
