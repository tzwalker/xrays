import sys
def_path = r'C:\Users\Trumann\Desktop\xrays\python\testing'
sys.path.append(def_path)

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import defs_old_ASCII_defs as old_ascii

def plotXCE(scans, shaped_dataframes):
    for scan, df in zip(scans, shaped_dataframes):
        df[df == 0] = np.nan                                                    #convert all zeros to NaN for scale convenience
        plt.figure()                                                            #initialize plotting object
        plt.title(scan['Name'], fontsize = 20)                                  #settings
        ax = sns.heatmap(df, xticklabels = 50, yticklabels = 50, annot= None, square = True, cbar_kws={'label': '%'})   #plot heatmap using seaborn
        ax.figure.axes[-1].yaxis.label.set_size(20)                             #settings
        ax.invert_yaxis()
        plt.xlabel('X (um)', fontsize = 18)
        plt.xticks(rotation = 0)
        plt.ylabel('Y (um)', fontsize = 18)
        plt.yticks(rotation = 0)
        plt.tick_params(axis="both", labelsize = 15)
    return ax

path_to_ASCIIs = r'C:\Users\Trumann\Desktop\ASCII\refit_NBL3_noZnL'

#enter energy in keV, stanford amplifcations in nanoamps, width/height in um, and elements of interest (EOI)
scan1 = {"sector": 2, 'Scan #': 439, 'Name': 'TS58A', 'width': 15, 'height': 15, 'x_points': 150, 'y_points': 150, 'beam_energy': 8.99, 'stanford': 200, 'lockin': 20, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 4359, "EOI": ['Sn_L', 'S', 'Cd_L', 'Te_L', 'Cu', 'Cl', 'Mo_L']} 
scan2 = {"sector": 2, 'Scan #': 475, 'Name': 'NBL3-3', 'width': 15, 'height': 15, 'x_points': 150, 'y_points': 150, 'beam_energy': 8.99, 'stanford': 200, 'lockin': 20, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 5680,  "EOI": ['Sn_L', 'S', 'Cd_L', 'Te_L', 'Cu', 'Cl', 'Mo_L']}
scan3 = {"sector": 2, 'Scan #': 519, 'Name': 'NBL3-1', 'width': 15, 'height': 15, 'x_points': 150, 'y_points': 150, 'beam_energy': 8.99, 'stanford': 200, 'lockin': 20, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 4787, "EOI": ['Sn_L', 'S', 'Cd_L', 'Te_L', 'Cu', 'Cl', 'Mo_L']}
scan4 = {"sector": 2, 'Scan #': 550, 'Name': 'NBL3-2', 'width': 15, 'height': 15, 'x_points': 150, 'y_points': 150, 'beam_energy': 8.99, 'stanford': 50000, 'lockin': 100, 'PIN beam_on': 105400, 'PIN beam_off': 510, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 5907, "EOI": ['Sn_L', 'S', 'Cd_L', 'Te_L', 'Cu', 'Cl', 'Mo_L']}

           
scan_list = [scan1, scan2, scan3, scan4]

imported_scans_dfs = old_ascii.shrinkASCII(scan_list)
old_ascii.generate_scalar_factor(scan_list)
#collect_XBIC(imported_scans_dfs)
#interpolate_diode_calibration(scan_list)
#get_flux(scan_list)
#calc_XCE(imported_scans_dfs, scan_list)

old_ascii.mapConvertAxes(imported_scans_dfs, scan_list)
list_of_shaped_XCE_dfs = old_ascii.mapShape(imported_scans_dfs)
old_ascii.plotXCE(scan_list, list_of_shaped_XCE_dfs)
