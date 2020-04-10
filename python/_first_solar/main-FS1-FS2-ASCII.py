"""
this files takes asciis of the scans below and only plots them
need to sys append path, as well as locate these scans
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as tkr

import definitions ASCII as old_ascii


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

old_ascii.CdTe_ratio(imported_scan_dfs)
old_ascii.mapShapeEle(imported_scan_dfs, scan_list)

"""
not sure what this program is for...
"""

import definitions ASCII as FSdefs

ASCII_path = r'C:\Users\Trumann\Desktop\FS_data\FS2_2019_03_2IDD'

#enter energy in keV, stanford amplifcations in nanoamps, width/height in um, (x_y_points - 1), and elements of interest (EOI)
scan1 = {"sector": 2, 'Scan #': '087', 'Name': 'FS1_1', 'width': 10, 'height': 30, 'x_points': 200, 'y_points': 600, 'x_ticks': 100,  'y_ticks': 100,  'beam_energy': 12.8, 'stanford': 500, 'lockin': 100, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 4359, "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L'], 'figure_size': (5,5)} 
scan2 = {"sector": 2, 'Scan #': 551, 'Name': 'FS2_1', 'width': 10, 'height': 20, 'x_points': 100, 'y_points': 200, 'x_ticks': 50,    'y_ticks': 25,        'beam_energy': 12.7, 'stanford': 5000, 'lockin': 2000, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 5680,  "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L'], 'figure_size': (5,4)}
scan3 = {"sector": 2, 'Scan #': 661, 'Name': 'FS2_2', 'width': 15, 'height': 20, 'x_points': 150, 'y_points': 200, 'x_ticks': 50, 'y_ticks': 25, 'beam_energy': 12.7, 'stanford': 100, 'lockin': 2000, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 4787, "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L'], 'figure_size': (5, 4)}
scan4 = {"sector": 26, 'Scan #': 100, 'Name': 'FS2_2', 'width': 4, 'height': 4, 'x_points': 100, 'y_points': 100, 'x_ticks': 25,   'y_ticks': 25, 'beam_energy': 10.4, 'stanford': 200, 'lockin': 200, 'PIN beam_on': 105400, 'PIN beam_off': 510, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 5907, "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'Sn_L']}

electrical_scaler_channel = 'ds_ic'
         
#what do you want to plot? note the number of plots made is limited by the smallest list here!
element_plot_list =     ['Cd_L', 'Se', 'As']#, 'Cd_L', 'Cd_CdTe', 'Zn', 'As', 'Se', 'Sn_L'] #, 'Cu', 'Zn', 'As', 'Se', 'Sn_L']
plot_titles =           ['Cd', 'Se', 'As']# ,'Cd/Cd+Te', 'Zn', 'As', 'Se', 'Sn']
element_plot_labels =   ['ug/cm2', 'ug/cm2', 'ug/cm2','ug/cm2', 'ug/cm2', 'ug/cm2', 'ug/cm2'] #, 'ug/cm2', 'ug/cm2', 'ug/cm2', 'ug/cm2', 'ug/cm2']
        
scan_list = [scan3]#, scan3, scan4]

imported_scan_dfs = FSdefs.shrinkASCII(ASCII_path, scan_list, electrical_scaler_channel)  #returns list containing dataframes of each scan
FSdefs.generate_scalar_factor(scan_list)           #generates the scalar factor for each scan and adds it to the scan in scan_list dictionary
FSdefs.collect_XBIC(imported_scan_dfs, scan_list)             #converts from ds_ic to amperes for each scan (replaces ds_ic column)

#FOR PLOTTING
FSdefs.mapConvertAxes(imported_scan_dfs, scan_list)
#CdTe_ratio(imported_scan_dfs)
#FSdefs.make_2d_plots(imported_scan_dfs, scan_list, element_plot_list, element_plot_labels, plot_titles)

shaped_dfs = FSdefs.MapsAsMatrices(scan_list, imported_scan_dfs, element_plot_list)
rotated_dfs = FSdefs.rotate_integrate_normalize(shaped_dfs)

x = list(np.linspace(0,15,151))
label_list = ['XBIC'] + plot_titles
FSdefs.make_line_plots(x,rotated_dfs, label_list)

#FSdefs.integrateStackDepth(shaped_dfs)


"""
this program integrates the ascii data from first solar
cross-section set FS2

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as tkr

import old_ASCII_defs as old_ascii

# this files takes asciis of the scans below and integrates them

def CdTe_ratio(dataframes_as_arrays):
    for df in dataframes_as_arrays:
        Cd_and_Te = pd.concat([df["Cd_L"], df["Te_L"]], axis=1, sort=False)     #isolate and make Cd and Te matrix
        Cd_plus_Te = Cd_and_Te.sum(axis=1)                                      #sum the two columns in new matrix
        df["Cd_CdTe"] = (df["Cd_L"] / Cd_plus_Te) * 100                         #CREATE Cd/(Cd+Te) column
        df["Te_CdTe"] = (df["Te_L"] / Cd_plus_Te) * 100                         #CREATE Te/(Cd+Te) column
    return

def make_plots(dataframe_as_array, scan_list):
    for df, scan in zip(dataframe_as_array, scan_list):
        xtick_iter = scan['x_ticks'] 
        ytick_iter = scan['y_ticks']
        
        df0 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = 'XBIC')
        
        fig = plt.figure(figsize = scan["figure_size"], dpi = 250)
        
        ax = sns.heatmap(df0, xticklabels = xtick_iter, yticklabels = ytick_iter, annot= None, square = True, cbar_kws={'label': 'A'})   #plot heatmap using seaborn
        #PLOT SETTINGS
        ax.figure.axes[-1].yaxis.label.set_size(18)                             #changes colorbar text label size
        ax.invert_yaxis()                                                       #orients the plot as displayed in MAPS
        
        #changes colorbar numeric label size
        cax = plt.gcf().axes[-1]
        cax.tick_params(labelsize = 15)
        
        plt.title('XBIC', fontsize = 18)
        plt.xlabel('X (um)', fontsize = 18)
        plt.xticks(rotation = 0)
        plt.ylabel('Y (um)', fontsize = 18)
        plt.yticks(rotation = 0)
        plt.tick_params(axis="both", labelsize = 15)
        
        for ele, legend, pltTitle in zip(element_plot_list, element_plot_labels, plot_titles):
            df1 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = ele)
            
            fig = plt.figure(figsize = scan["figure_size"], dpi = 250)
            
            #FORMATS Colorbar
            formatter = tkr.ScalarFormatter(useMathText=False)
            formatter.set_scientific(True)
            formatter.set_powerlimits((-2, 0))
            
            ax = sns.heatmap(df1, xticklabels = xtick_iter, yticklabels = ytick_iter, vmin = 0, annot= None, square = True, cbar_kws={'label': legend, "format": formatter})   #plot heatmap using seaborn
            #PLOT SETTINGS
            #changes colorbar text label size
            ax.figure.axes[-1].yaxis.label.set_size(18)
            ax.invert_yaxis()
            
            
            #changes colorbar tick label size
            cax = plt.gcf().axes[-1]
            cax.tick_params(labelsize = 15)


            #changes title, x, and y axis text size
            plt.title(pltTitle, fontsize = 18)
            plt.xlabel('X (um)', fontsize = 18)
            plt.xticks(rotation = 0)
            plt.ylabel('Y (um)', fontsize = 18)
            plt.yticks(rotation = 0)
            plt.tick_params(axis="both", labelsize = 15)
            
            #SAVE FIGURE
            #fig.get_figure()
            #fig.savefig(r"C:\Users\Trumann\Desktop\Plot Directory\FS\20190326 FS Set 2_Se edge_normalized pic size\{s}, {e}.jpg".format(e = ele, s = scan["Name"]))
    return 

	
def MapsAsMatrices(scan_list, dataframe_as_array):
    shaped_scan_dictionary = {}                                                         #initializes empty dictionary to contain each scans
    for scan, df in zip(scan_list, dataframe_as_array):
        plotList = []                                                                   #initializes list to contain the shaped channels of interest
        df1 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = 'XBIC')   #shapes the XBIC channel
        plotList.append(df1)                                                        
        for ele in element_plot_list:
            df2 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = ele)  #shapes the element channels
            plotList.append(df2)
        key = 'shaped_dfs of ' + str(scan["Scan #"])                                          #CREATE key for shaped_dictionary
        shaped_scan_dictionary.setdefault(key, plotList) 
    return shaped_scan_dictionary
	
path_to_ASCIIs = r'C:\Users\Trumann\Desktop\ASCII\FS'

#enter energy in keV, stanford amplifcations in nanoamps, width/height in um, (x_y_points - 1), and elements of interest (EOI)
scan1 = {"sector": 2, 'Scan #': '087', 'Name': 'FS1_1', 'width': 10, 'height': 30, 'x_points': 200, 'y_points': 600, 'x_ticks': 100,  'y_ticks': 100,  'beam_energy': 12.8, 'stanford': 500, 'lockin': 100, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 4359, "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L', 'Pt_L'], 'figure_size': (5,5)} 
scan2 = {"sector": 2, 'Scan #': 551, 'Name': 'FS2_1', 'width': 10, 'height': 20, 'x_points': 100, 'y_points': 200, 'x_ticks': 50,    'y_ticks': 25,        'beam_energy': 12.8, 'stanford': 5000, 'lockin': 2000, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 5680,  "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L', 'Pt_L'], 'figure_size': (5,4)}
scan3 = {"sector": 2, 'Scan #': 661, 'Name': 'FS2_2', 'width': 15, 'height': 20, 'x_points': 150, 'y_points': 200, 'x_ticks': 50, 'y_ticks': 25,               'beam_energy': 10.4, 'stanford': 100, 'lockin': 2000, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 4787, "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L', 'Pt_L'], 'figure_size': (5, 4)}
scan4 = {"sector": 26, 'Scan #': 100, 'Name': 'FS2_2', 'width': 4, 'height': 4, 'x_points': 100, 'y_points': 100, 'x_ticks': 25,   'y_ticks': 25, 'beam_energy': 10.4, 'stanford': 200, 'lockin': 200, 'PIN beam_on': 105400, 'PIN beam_off': 510, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 5907, "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'Sn_L']}

#what do you want to plot? note the number of plots made is limited by the smallest list here!
element_plot_list =     ['Pt_L'] #, 'Cd_L', 'Te_L', 'Zn', 'As', 'Se', 'Sn_L'] #, 'Cu', 'Zn', 'As', 'Se', 'Sn_L']
plot_titles =           ['Pt']#, 'Cd', 'Te', 'Zn', 'As', 'Se', 'Sn']
element_plot_labels =   ['ug/cm2']#, 'ug/cm2', 'ug/cm2','ug/cm2', 'ug/cm2', 'ug/cm2', 'ug/cm2'] #, 'ug/cm2', 'ug/cm2', 'ug/cm2', 'ug/cm2', 'ug/cm2']
        
scan_list = [scan2] #, scan3, scan4]

imported_scan_dfs = old_ascii.shrinkASCII(scan_list)  #returns list containing dataframes of each scan
old_ascii.generate_scalar_factor(scan_list)           #generates the scalar factor for each scan and adds it to the scan in scan_list dictionary
old_ascii.collect_XBIC(imported_scan_dfs)             #converts from ds_ic to amperes for each scan (replaces ds_ic column)

#FOR PLOTTING
old_ascii.mapConvertAxes(imported_scan_dfs, scan_list)
CdTe_ratio(imported_scan_dfs)
make_plots(imported_scan_dfs, scan_list)

#FOR summed concntration of species as a function of depth
#want to create sum of concentrations for a given "stack depth (x)" and plot vs. x
imported_shaped_dict = MapsAsMatrices(scan_list, imported_scan_dfs)

plot_titles2 =           ['XBIC', 'Cu', 'Cd', 'Te', 'Zn', 'As', 'Se', 'Sn']

def integrateStackDepth(imported_shaped_dict):
    for (scan_number, list_of_shaped_dfs), scan in zip(imported_shaped_dict.items(), scan_list):        #access shaped dictionary (dict) and scan_list (list of dictionaries)
        for df, channel in zip(list_of_shaped_dfs, plot_titles2):                                       #access dataframe list in dictionary (df) and naming list (list)
            column_sum = df.sum(axis = 0, skipna = True)
            channel_max = column_sum.max(axis = 0)
            
            norm_channel = column_sum.divide(channel_max, axis=0)
            norm_max = norm_channel.max(axis = 0)
            
            #PLOT SETTINGS
            fig = plt.figure()
            ax = norm_channel.plot(kind = 'line', grid = True)
            #x axis
            majorXlocator = tkr.MultipleLocator(1)
            minorXlocator = tkr.MultipleLocator(0.2)
            ax.set_xlim((0, scan["width"]))
            ax.xaxis.set_major_locator(majorXlocator)
            ax.xaxis.set_minor_locator(minorXlocator)
            #y axis
            majorYlocator = tkr.MultipleLocator(0.25)
            #minorYlocator = tkr.MultipleLocator(0.1)
            ax.set_ylim((0, norm_max))
            ax.yaxis.set_major_locator(majorYlocator)
            #ax.yaxis.set_minor_locator(minorYlocator)
            
            #format gridlines
            ax.grid(b=True, which='major', color='k', linestyle='-')
            ax.grid(which='minor', color='k', linestyle=':', alpha=0.5)
            #format labels
            ax.set_title(scan["Name"] + ', ' + channel, fontsize = 18)
            ax.set_xlabel('X (um)', fontsize = 18)
            ax.set_ylabel(channel + ' Norm. (%)', fontsize = 18)
            plt.tick_params(axis="both", labelsize = 15)
    return

#integrateStackDepth(imported_shaped_dict)



