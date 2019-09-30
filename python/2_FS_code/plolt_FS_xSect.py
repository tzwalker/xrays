import plot_FS_xSect_defs as FSdefs

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


