import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as tkr

import old_ASCII_defs as old_ascii

# this files takes asciis of the scans below and only plots them
# need to sys append path, as well as locate these scans
path_to_ASCIIs = r'C:\Users\Trumann\Desktop\ASCII\FS'

#enter energy in keV, stanford amplifcations in nanoamps, width/height in um, (x_y_points - 1), and elements of interest (EOI)
scan1 = {"sector": 2, 'Scan #': '087', 'Name': 'FS1_1', 'width': 10, 'height': 30, 'x_points': 200, 'y_points': 600, 'x_ticks': 100,  'y_ticks': 100,  'beam_energy': 12.8, 'stanford': 500, 'lockin': 100, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 4359, "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L'], 'figure_size': (5,5)} 
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

def CdTe_ratio(dataframes_as_arrays):
    for df in dataframes_as_arrays:
        Cd_and_Te = pd.concat([df["Cd_L"], df["Te_L"]], axis=1, sort=False)
        Cd_plus_Te = Cd_and_Te.sum(axis=1)
        df["Cd_CdTe"] = (df["Cd_L"] / Cd_plus_Te) * 100
        df["Te_CdTe"] = (df["Te_L"] / Cd_plus_Te) * 100
    return

def mapShapeEle(dataframe_as_array, scan_list):
    for df, scan in zip(dataframe_as_array, scan_list):
        xtick_iter = scan['x_ticks'] 
        ytick_iter = scan['y_ticks']
        for ele, legend in zip(element_plot_list, element_plot_labels):
            df1 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = ele)
            
            fig = plt.figure() 
            #prepares colorbar in seaborn heatmap for scientific notation
            formatter = tkr.ScalarFormatter(useMathText=False)
            formatter.set_scientific(True)
            formatter.set_powerlimits((-2, 0))
            
            #creates seaborn heatmap
            #sns.set(font_scale = 1.5)
            ax = sns.heatmap(df1, xticklabels = xtick_iter, yticklabels = ytick_iter, annot= None, square = True, cbar_kws={'label': legend, "format": formatter})   #plot heatmap using seaborn
            
            #changes colorbar text label size
            ax.figure.axes[-1].yaxis.label.set_size(18)
            ax.invert_yaxis()
            
            
            #changes colorbar ticklabel size
            cax = plt.gcf().axes[-1]
            cax.tick_params(labelsize = 15)


            #changes title, x, and y axis text size
            #plt.title(ele + ', ' + scan["Name"], fontsize = 18)
            plt.xlabel('X (um)', fontsize = 18)
            plt.xticks(rotation = 0)
            plt.ylabel('Y (um)', fontsize = 18)
            plt.yticks(rotation = 0)
            plt.tick_params(axis="both", labelsize = 15)
            
            #saves figure
            
            #fig.get_figure()
            #fig.savefig(r"C:\Users\Trumann\Desktop\Plot Directory\FS\20190317 FS Set 2_Se edge\{s}, {e}.jpg".format(e = ele, s = scan["Name"]))
    return 

CdTe_ratio(imported_scan_dfs)
mapShapeEle(imported_scan_dfs, scan_list)

#unoriginal superficial the issue
#changing this file too

#push a change from a contributor
#yo i'm pushing another change form a contributor
