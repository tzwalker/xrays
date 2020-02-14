import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as tkr
from skimage.transform import rotate

#IMPORT AND SHIRNK DATAFRAME: imports and shrinks ASCII according to what elements are specified and the sector the scan was taken
def shrinkASCII(large_ASCII_files):
    smaller_dfs = []
    for scan in large_ASCII_files:
        if scan["sector"] == 2:
            file_name = r'\combined_ASCII_2idd_0{n}.h5.csv'.format(n = scan['Scan #'])
        else:
            file_name = r'\combined_ASCII_26idbSOFT_0{n}.h5.csv'.format(n = scan['Scan #'])
        csvIn = pd.read_csv(path_to_ASCIIs + file_name, skiprows = 1)
        noColNameSpaces(csvIn)                                                 #removes whitspaces from column headers, for easy access
        shrink1 = csvIn[['x pixel no', 'y pixel no', 'ds_ic']]                 #isolates x,y,and electrical columns
        shrink2 = csvIn[scan["EOI"]]                                           #isolates element of interest columns
        shrink = pd.concat([shrink1, shrink2], axis=1, sort=False)             #combines these columns into one matrix while maintaining indices
        smaller_dfs.append(shrink)                                             #add smaller matrices to list so they may be iterated over...
    return smaller_dfs

def noColNameSpaces(pd_csv_df):
    old_colnames = pd_csv_df.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    pd_csv_df.rename(columns = {i:j for i,j in zip(old_colnames,new_colnames)}, inplace=True)
    return pd_csv_df

# import linescanes (e.g. for bias studies)
def import_line_ASCIIS(scans):
    line_scans = []
    usecols = list(range(7))  #line plots exported only with ds_ic channel
    for scan in scans:
        s = str(scan)
        filename = r'\line2idd_0'+s+'.h5.csv'
        df = pd.read_csv(path_to_ASCIIs + filename, usecols=usecols)
        noColNameSpaces(df)
        line_scans.append(df)
    return line_scans

def generate_scalar_factor(scan_list):
    beamconversion_factor = 200000
    for scan in scan_list:
        correction = ((scan['stanford']*(1*10**-9)) / (beamconversion_factor * scan['lockin']))     #calculate scale factor for chosen scan
        key = 'scale factor'                                                                        #CREATE: define key for scan dictionary
        scan.setdefault(key, correction)                                                            #add key and correction factor to scan
        #print(correction)
    return

## converting XBIC
def collect_XBIC(small_dfs, scan_list):
    eh_per_coulomb = 1/(1.60217634*10**-19)                                  #most recent accepted value for electrons per coulomb
    eh_or_amps = int(input('Type 0 for XBIC, 1 for ehPairs: '))
    
    if eh_or_amps == 0:
        for df, scan in zip(small_dfs, scan_list):
            df["ds_ic"] = df["ds_ic"].astype(float)                             #reformat column for floating arithmetic operations
            scaled_dsic = df.loc[:,'ds_ic'] * scan['scale factor']              #apply amplifaction settings  (converts counts to amps)
            df['ds_ic'] = scaled_dsic
            df.rename(columns = {'ds_ic': 'XBIC'}, inplace = True)  
        
        
    if eh_or_amps == 1:
        for df, scan in zip(small_dfs, scan_list):
            df["ds_ic"] = df["ds_ic"].astype(float)                             #reformat column for floating arithmetic operations
            scaled_dsic = df.loc[:,'ds_ic'] * scan['scale factor']              #apply amplifaction settings  (converts counts to amps)
            collected_dsic = scaled_dsic * eh_per_coulomb                       #convert amps to e-h pairs
            df['ds_ic'] = collected_dsic
            df.rename(columns = {'ds_ic': 'eh_pairs'}, inplace = True)                        
    return

def custom_format_ticks(axes_object):
    x_txt_labs = [label.get_text() for label in axes_object.get_xticklabels()]
    x_ticking = ['{:g}'.format(float(x)) for x in x_txt_labs]
    y_txt_labs = [label.get_text() for label in axes_object.get_yticklabels()]
    y_ticking = ['{:g}'.format(float(y)) for y in y_txt_labs]
    return x_ticking, y_ticking

#PLOTTING FUNCTIONS
def mapConvertAxes(dataframes, scans):
    for df, scan in zip(dataframes, scans):
        height_factor = scan['height'] / scan['y_points']                       #converts to (um/line) for y-direction
        width_factor = scan['width'] / scan['x_points']                         #converts to (um/line) for x-direction
        df['y pixel no']  = df['y pixel no'] * height_factor                    #OVERWRITE Y PIXEL COLUMN: ypixel-no/line *(um/line) = um (y)
        df['x pixel no']  = df['x pixel no'] * width_factor                     #OVERWRITE X PIXEL COLUMN: xpixel-no/line *(um/line) = um (x)
        #print(width_factor, scan["Name"])
        #print(height_factor, scan["Name"])        
    return

#CALCULATE CDTE RATIOS
def CdTe_ratio(dataframes_as_arrays):
    for df in dataframes_as_arrays:
        Cd_and_Te = pd.concat([df["Cd_L"], df["Te_L"]], axis=1, sort=False)     #isolate and make Cd and Te matrix
        Cd_plus_Te = Cd_and_Te.sum(axis=1)                                      #sum the two columns in new matrix
        df["Cd_CdTe"] = (df["Cd_L"] / Cd_plus_Te) * 100                         #CREATE Cd/(Cd+Te) column
        df["Te_CdTe"] = (df["Te_L"] / Cd_plus_Te) * 100                         #CREATE Te/(Cd+Te) column
    return

def rotate_integrate_normalize(list_of_imported_dfs):
    rot_arrs = [rotate(df, 25) for df in list_of_imported_dfs]
    integrated_arrs = [matrix.sum(axis = 0) for matrix in rot_arrs]
    norm_arrs = [((v - v.min()) / (v.max() - v.min())) for v in integrated_arrs]
    return norm_arrs

def interpolate_diode_calibration(scans):
    lower_ASU_PIN_energy = 8.08                                         #keV
    upper_ASU_PIN_energy = 12.8                                         #keV
    flux_at_8keV = 3071                                                 #ph/(s*pA) ; from 2018_07 beam run (8.08keV)
    flux_at_12keV = 2728                                                #ph/(s*pA) ; from 2018_07 beam run (12.8keV)
    for scan in scans:
        flux_of_interest = flux_at_8keV + (scan['beam_energy'] - lower_ASU_PIN_energy) * ((flux_at_12keV - flux_at_8keV)/(upper_ASU_PIN_energy-lower_ASU_PIN_energy)) #interpolate at the energy the scan was taken
        rounded_calib = round(flux_of_interest, 1)                      #keep an integer
        key = 'ph/(s*pA)'                                               #CREATE: store calibration in sample dictionary for easy retrieval
        scan.setdefault(key, rounded_calib)                             #assign key:value pair
    return 

def get_flux(scans):
    for scan in scans:
        if scan["sector"] == 2:
            beamconversion = 200000                                             #SET: sector 2 beam conversion factor
        else:
            beamconversion = 5000                                               #SET: sector 26 beam conversion factor
        PIN_current = ((scan['PIN beam_on'] - scan['PIN beam_off'])  /  beamconversion) * (scan["PIN stanford"] *10**-9)        #converts counts to current from beam
        flux = PIN_current * scan['ph/(s*pA)'] * (1*10**12)                     #converts to flux of beam
        rounded_flux = round(flux)                                              #round to nearest whole photon
        key = 'flux'                                                            #CREATE: store flux in sample dictionary for easy retrieval
        scan.setdefault(key, rounded_flux)                                      #assign key:value pair
    return

def calc_XCE(smaller_dfs, scans):
    alpha = 3
    for df, scan in zip(smaller_dfs, scans):
        C = scan["E_abs"] / (scan['absorber_Eg'] * alpha)           #calculate correction factor, function of energy absorbed, bandgap, and energy conversion, ideally, get_thickness_factor(energy, absorber_compound, absorber_thickness, abosrber_density) would go here
        XCE = df['eh_pairs'] / (C * scan['flux']) * 100             #calculate collection efficiency
        df['eh_pairs'] = XCE                                        #OVERWRITE: replace e-h column with XCE column
        df.rename(columns = {'eh_pairs': 'XCE'}, inplace = True)    #rename to XCE column
    return

### plotting in ASCII format ###
def mapConvertAxes(dataframes, scans):
    for df, scan in zip(dataframes, scans):
        height_factor = scan['height'] / scan['y_points']                       #converts to (um/line) for y-direction
        width_factor = scan['width'] / scan['x_points']                         #converts to (um/line) for x-direction
        df['y pixel no']  = df['y pixel no'] * height_factor                    #OVERWRITE Y PIXEL COLUMN: ypixel-no/line *(um/line) = um (y)
        df['x pixel no']  = df['x pixel no'] * width_factor                     #OVERWRITE X PIXEL COLUMN: xpixel-no/line *(um/line) = um (x)
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
    return 

def mapShape(dataframe_list):
    plotList = []
    for df in dataframe_list:
        df = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = 'XCE') #shape XCE column into map accroding to converted x and y column indices
        plotList.append(df)                                                         #store shaped dfs in list
    return plotList

def make_line_plots(x_range, y_vars, labels):
    for arr,lab in zip(y_vars, labels):
        fig, ax0 = plt.subplots(1)
        ax0.plot(x_range,arr)
        plt.minorticks_on()
        plt.xlim([0, max(x_range)])
        plt.yticks(np.arange(0,1.05,0.25))
        plt.ylim([0, 1])
        plt.grid(b=True, which='major', color='k', linewidth=1)
        plt.grid(b=True, which='minor', axis='x', linestyle='--', linewidth=1)
        
        plt.xlabel('X (um)', fontsize=16)
        plt.ylabel(lab + ' Norm (%)', fontsize=16)
        ax0.tick_params(axis="both", labelsize=14)
        plt.title('FS2_2 '+ lab)
    return

def plotXCE(scans, shaped_dataframes):
    for scan, df in zip(scans, shaped_dataframes):
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

def make_2d_plots(dataframe_as_array, scan_list, ele_plt_list, ele_plt_lab, plt_t):
    for df, scan in zip(dataframe_as_array, scan_list):
        xtick_iter = scan['x_ticks'] 
        ytick_iter = scan['y_ticks']
        df0 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = 'XBIC')
        
        fig = plt.figure() #figsize = scan["figure_size"], dpi = 250
        
        ax = sns.heatmap(df0, xticklabels = xtick_iter, yticklabels = ytick_iter, 
                         annot= None, square = True, cbar_kws={'label': 'A'})   #plot heatmap using seaborn
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
        
        for ele, legend, pltTitle in zip(ele_plt_list, ele_plt_lab, plt_t):
            df1 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = ele)
            
            fig = plt.figure() #figsize = scan["figure_size"], dpi = 250
            
            #FORMATS Colorbar
            formatter = tkr.ScalarFormatter(useMathText=False)
            formatter.set_scientific(True)
            formatter.set_powerlimits((-2, 0))
            
            ax = sns.heatmap(df1, xticklabels = xtick_iter, yticklabels = ytick_iter, 
                             vmin = 0, annot= None, square = True, 
                             cbar_kws={'label': legend, "format": formatter})   #plot heatmap using seaborn
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

def plot_nice2d_from_ascii(xrf_image_full_path, channel, colormap):
    df = pd.read_csv(xrf_image_full_path, skiprows = 1)
    df = noColNameSpaces(df)
    resolution = abs(df['y position'][0] - df['y position'][1]) * 1000
    df['x pixel no'] = df['x pixel no'] * resolution
    df['x pixel no'] = round(df['x pixel no'], 1)
    df['y pixel no'] = df['y pixel no'] * resolution
    df['y pixel no'] = round(df['y pixel no'], 1)
    map_df = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = channel)
    
    fig, ax0 = plt.subplots()
    ax0 = sns.heatmap(map_df, square = True, cmap = colormap, 
                      xticklabels = 40, yticklabels = 40, vmin=100000)
    # figure level
    plt.xlabel('X (\u03BCm)', fontsize=16)
    plt.ylabel('Y (\u03BCm)', fontsize=16)
    # axis level
    ax0.tick_params(labelsize = 14)                     #formats size of ticklabels
    x_labls, y_labls = custom_format_ticks(ax0)         #formats tick label strings without ".0"
    ax0.set_xticklabels(x_labls)                        #set the tick labels
    ax0.set_yticklabels(y_labls, rotation = 0)   
    ax0.invert_yaxis()
    
    cbar_ax = plt.gcf().axes[-1]                        #gets colorbar of current figure object, behaves as second y object
    # colorbar label settings
    cbar_ax.set_ylabel('cts/s', fontsize = 16, #\u03BCg/cm'+ r'$^{2}$
                       rotation = 90, labelpad = 10)   #label formatting
    cbar_ax.tick_params(labelsize=12)                   #tick label formatting
    cbar_ax.yaxis.set_offset_position('left')           #scale at top of colorbar (i.e. 'offset') position
    cbar_ax.yaxis.get_offset_text().set(size=12)        #format colorbar offset text
    #cbar_ax.set_yticklabels('0.2f') --> debug
    return

#FOR summed concntration of species as a function of depth
#want to create sum of concentrations for a given "stack depth (x)" and plot vs. x
# converts array of csv into NxM matrix 
def MapsAsMatrices(scan_list, dataframe_as_array, el):
    plotList = []                                                         #initializes list to contain the shaped channels of interest
    for scan, df in zip(scan_list, dataframe_as_array):
        df1 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = 'XBIC')   #shapes the XBIC channel
        plotList.append(df1)                                                        
        for ele in el:
            df2 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = ele)  #shapes the element channels
            plotList.append(df2)
    return plotList

def integrateStackDepth(imported_shaped_dict):
    for df in imported_shaped_dict:
        column_sum = df.sum(axis = 0, skipna = True)
        fig = plt.figure()
        column_sum.plot.line()
    return




