import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as tkr

#MAPS exports ASCIIs with column header whitespace, this function is used to remove that whitespace
def noColNameSpaces(pd_csv_df):
    old_colnames = pd_csv_df.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    pd_csv_df.rename(columns = {i:j for i,j in zip(old_colnames,new_colnames)}, inplace=True)
    return pd_csv_df

#this function imports and shrinks the ASCII according to what elements are specified and the sector the scan was taken
def shrinkASCII(large_ASCII_files):
    smaller_dfs = []
    for scan in large_ASCII_files:
        if scan["sector"] == 2:
            file_name = r'\combined_ASCII_2idd_0{n}.h5.csv'.format(n = scan['Scan #'])
        else:
            file_name = r'\combined_ASCII_26idbSOFT_0{n}.h5.csv'.format(n = scan['Scan #'])
        csvIn = pd.read_csv(path_to_ASCIIs + file_name, skiprows = 1)
        noColNameSpaces(csvIn)                                                                      #removes whitspaces from column headers, for easy access
        shrink1 = csvIn[['x pixel no', 'y pixel no', 'ds_ic']]                                      #isolates x,y,and electrical columns
        shrink2 = csvIn[scan["EOI"]]                                                                #isolates element of interest columns
        shrink = pd.concat([shrink1, shrink2], axis=1, sort=False)                                  #combines these columns into one matrix while maintaining indices
        smaller_dfs.append(shrink)                                                                  #add smaller matrices to list so they may be iterated over...
    return smaller_dfs

def generate_scalar_factor(scan_list):
    beamconversion_factor = 100000
    for scan in scan_list:
        correction = ((scan['stanford']*(1*10**-9)) / (beamconversion_factor * scan['lockin']))     #calculate scale factor for chosen scan
        key = 'scale factor'                                                                        #define key for scan dictionary
        scan.setdefault(key, correction)                                                            #add key and correction factor to scan
        #print(correction)
    return

def collect_XBIC(list_of_smaller_dfs):
    #eh_per_coulomb = 1/(1.60217634*10**-19)                                  #most recent accepted value for electrons per coulomb
    for df, scan in zip(list_of_smaller_dfs, scan_list):
        df["ds_ic"] = df["ds_ic"].astype(float)                             #reformat column for floating arithmetic operations
        scaled_dsic = df.loc[:,'ds_ic'] * scan['scale factor']              #apply amplifaction settings  (converts counts to amps)
        #collected_dsic = scaled_dsic * eh_per_coulomb                       #convert amps to e-h pairs
        df['ds_ic'] = scaled_dsic
        df.rename(columns = {'ds_ic': 'XBIC'}, inplace = True)                        
    return 

def interpolate_diode_calibration(scans):
    lower_ASU_PIN_energy = 8.08                                         #keV
    upper_ASU_PIN_energy = 12.8                                         #keV
    flux_at_8keV = 3071                                                 #ph/(s*pA) ; from 2018_07 beam run (8.08keV)
    flux_at_12keV = 2728                                                #ph/(s*pA) ; from 2018_07 beam run (12.8keV)
    for scan in scans:
        flux_of_interest = flux_at_8keV + (scan['beam_energy'] - lower_ASU_PIN_energy) * ((flux_at_12keV - flux_at_8keV)/(upper_ASU_PIN_energy-lower_ASU_PIN_energy)) #interpolate at the energy the scan was taken
        rounded_calib = round(flux_of_interest, 1)                      #keep an integer
        key = 'ph/(s*pA)'                                               #store calibration in sample dictionary for easy retrieval
        scan.setdefault(key, rounded_calib)                             #assign key:value pair
    return 

def get_flux(scans):
    for scan in scans:
        if scan["sector"] == 2:
            beamconversion = 100000                                             #sector 2 beam conversion factor
        else:
            beamconversion = 5000                                               #UNKNOWN beamconversion for sector 26
        PIN_current = ((scan['PIN beam_on'] - scan['PIN beam_off'])  /  beamconversion) * (scan["PIN stanford"] *10**-9)        #converts counts to current from beam
        flux = PIN_current * scan['ph/(s*pA)'] * (1*10**12)                     #converts to flux of beam
        rounded_flux = round(flux)                                              #round to nearest whole photon
        key = 'flux'                                                            #store fluxx in sample dictionary for easy retrieval
        scan.setdefault(key, rounded_flux)                                      #assign key:value pair
    return

def calc_XCE(smaller_dfs, scans):
    alpha = 3
    for df, scan in zip(smaller_dfs, scans):
        C = scan["E_abs"] / (scan['absorber_Eg'] * alpha)           #calculate correction factor, function of energy absorbed, bandgap, and energy conversion, ideally, get_thickness_factor(energy, absorber_compound, absorber_thickness, abosrber_density) would go here
        XCE = df['eh_pairs'] / (C * scan['flux']) * 100             #calculate collection efficiency
        df['eh_pairs'] = XCE                                        #replace df column for ease of use
        df.rename(columns = {'eh_pairs': 'XCE'}, inplace = True)    #rename to XCE column
    return



#functions for plotting!
def mapConvertAxes(dataframes, scans):
    for df, scan in zip(dataframes, scans):
        height_factor = scan['height'] / scan['y_points']                       #converts to (um/line) for y-direction
        width_factor = scan['width'] / scan['x_points']                         #converts to (um/line) for x-direction
        df['y pixel no']  = df['y pixel no'] * height_factor                    #ypixel-no/line *(um/line) = um (y)
        df['x pixel no']  = df['x pixel no'] * width_factor                     #xpixel-no/line *(um/line) = um (x)
        #print(width_factor, scan["Name"])
        #print(height_factor, scan["Name"])        
    return

def mapShape(dataframe_list):
    plotList = []
    for df in dataframe_list:
        df = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = 'XBIC') #shape XCE column into map accroding to converted x and y column indices
        plotList.append(df)                                                         #store shaped dfs in list
    return plotList

def plotXCE(scans, shaped_dataframes):
    for scan, df in zip(scans, shaped_dataframes):
        df[df == 0] = np.nan                                                    #convert all zeros to NaN for scale convenience
        fig = plt.figure()
        
        ax = sns.heatmap(df, xticklabels = scan['x_ticks'], yticklabels = scan['y_ticks'], annot= None, square = True, cbar_kws={'label': 'A'})   #plot heatmap using seaborn
        ax.figure.axes[-1].yaxis.label.set_size(18)                             #settings
        ax.invert_yaxis()
        
        #changes colorbar ticklabel size
        cax = plt.gcf().axes[-1]
        cax.tick_params(labelsize = 15)
        
        #plt.title('XBIC, ' + scan["Name"], fontsize = 18)
        plt.xlabel('X (um)', fontsize = 18)
        plt.xticks(rotation = 0)
        plt.ylabel('Y (um)', fontsize = 18)
        plt.yticks(rotation = 0)
        plt.tick_params(axis="both", labelsize = 15)
    return ax

path_to_ASCIIs = r'C:\Users\Trumann\Desktop\ASCII\FS'

#enter energy in keV, stanford amplifcations in nanoamps, width/height in um, (x_y_points - 1), and elements of interest (EOI)
scan1 = {"sector": 2, 'Scan #': '087', 'Name': 'FS1_1', 'width': 10, 'height': 30, 'x_points': 200, 'y_points': 600, 'x_ticks': 100,  'y_ticks': 100,  'beam_energy': 12.8, 'stanford': 500, 'lockin': 100, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 4359, "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L'], 'figure_size': (5,5)} 
scan2 = {"sector": 2, 'Scan #': 551, 'Name': 'FS2_1', 'width': 10, 'height': 20, 'x_points': 100, 'y_points': 200, 'x_ticks': 50,    'y_ticks': 25,        'beam_energy': 12.8, 'stanford': 5000, 'lockin': 2000, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 5680,  "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L'], 'figure_size': (5,4)}
scan3 = {"sector": 2, 'Scan #': 661, 'Name': 'FS2_2', 'width': 15, 'height': 20, 'x_points': 150, 'y_points': 200, 'x_ticks': 50, 'y_ticks': 25,               'beam_energy': 10.4, 'stanford': 100, 'lockin': 2000, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 4787, "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'As', 'Se', 'Sn_L'], 'figure_size': (5, 4)}
scan4 = {"sector": 26, 'Scan #': 100, 'Name': 'FS2_2', 'width': 4, 'height': 4, 'x_points': 100, 'y_points': 100, 'x_ticks': 25,   'y_ticks': 25, 'beam_energy': 10.4, 'stanford': 200, 'lockin': 200, 'PIN beam_on': 105400, 'PIN beam_off': 510, 'PIN stanford': 500, "absorber_Eg": 1.45, 'E_abs': 5907, "EOI": ['Cd_L', 'Te_L', 'Cu', 'Zn', 'Sn_L']}

element_plot_list = ['Cu', 'Te_CdTe']#, 'Cu', 'Zn', 'As', 'Se', 'Sn_L']
element_plot_labels = ['ug/cm2', 'at. %']#, 'ug/cm2', 'ug/cm2', 'ug/cm2', 'ug/cm2', 'ug/cm2']
        
scan_list = [scan1, scan2, scan3, scan4]

imported_scan_dfs = shrinkASCII(scan_list)
generate_scalar_factor(scan_list)
collect_XBIC(imported_scan_dfs)
#interpolate_diode_calibration(scan_list)
#get_flux(scan_list)
#calc_XCE(XCE_corrected_dfs, scan_list)

mapConvertAxes(imported_scan_dfs, scan_list)
shaped_dfs = mapShape(imported_scan_dfs)
#plotXCE(scan_list, shaped_dfs)

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
