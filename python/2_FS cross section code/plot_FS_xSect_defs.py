import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as tkr

#IMPORT AND SHIRNK DATAFRAME: imports and shrinks ASCII according to what elements are specified and the sector the scan was taken
def shrinkASCII(path, large_ASCII_files):
    smaller_dfs = []
    for scan in large_ASCII_files:
        if scan["sector"] == 2:
            file_name = r'\combined_ASCII_2idd_0{n}.h5.csv'.format(n = scan['Scan #'])
        else:
            file_name = r'\combined_ASCII_26idbSOFT_0{n}.h5.csv'.format(n = scan['Scan #'])
        csvIn = pd.read_csv(path + file_name, skiprows = 1)
        noColNameSpaces(csvIn)                                                                      #removes whitspaces from column headers, for easy access
        shrink1 = csvIn[['x pixel no', 'y pixel no', 'ds_ic']]                                      #isolates x,y,and electrical columns
        shrink2 = csvIn[scan["EOI"]]                                                                #isolates element of interest columns
        shrink = pd.concat([shrink1, shrink2], axis=1, sort=False)                                  #combines these columns into one matrix while maintaining indices
        smaller_dfs.append(shrink)                                                                  #add smaller matrices to list so they may be iterated over...
    return smaller_dfs

#supplement to "shrinkASCII()": MAPS exports ASCIIs with column header whitespace, this removes that whitespace
def noColNameSpaces(pd_csv_df):
    old_colnames = pd_csv_df.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    pd_csv_df.rename(columns = {i:j for i,j in zip(old_colnames,new_colnames)}, inplace=True)
    return pd_csv_df

#CALCULATE XBIC
def generate_scalar_factor(scan_list):
    beamconversion_factor = 100000
    for scan in scan_list:
        correction = ((scan['stanford']*(1*10**-9)) / (beamconversion_factor * scan['lockin']))     #calculate scale factor for chosen scan
        key = 'scale factor'                                                                        #define key for scan dictionary
        scan.setdefault(key, correction)                                                            #add key and correction factor to scan
        #print(correction)
    return

def collect_XBIC(dataframes_as_array, sl):
    for df, scan in zip(dataframes_as_array, sl):
        df["ds_ic"] = df["ds_ic"].astype(float)                             #reformat column for floating arithmetic operations
        scaled_dsic = df.loc[:,'ds_ic'] * scan['scale factor']              #apply amplifaction settings  (converts counts to amps)
        df['ds_ic'] = scaled_dsic                                           #OVERWRITE ds_ic
        df.rename(columns = {'ds_ic': 'XBIC'}, inplace = True)              #renames column from "ds_ic" to "XBIC" for convenience          
    return 

#CALCULATE CDTE RATIOS
def CdTe_ratio(dataframes_as_arrays):
    for df in dataframes_as_arrays:
        Cd_and_Te = pd.concat([df["Cd_L"], df["Te_L"]], axis=1, sort=False)     #isolate and make Cd and Te matrix
        Cd_plus_Te = Cd_and_Te.sum(axis=1)                                      #sum the two columns in new matrix
        df["Cd_CdTe"] = (df["Cd_L"] / Cd_plus_Te) * 100                         #CREATE Cd/(Cd+Te) column
        df["Te_CdTe"] = (df["Te_L"] / Cd_plus_Te) * 100                         #CREATE Te/(Cd+Te) column
    return


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

def make_plots(dataframe_as_array, scan_list, ele_plt_list, ele_plt_lab, plt_t):
    for df, scan in zip(dataframe_as_array, scan_list):
        xtick_iter = scan['x_ticks'] 
        ytick_iter = scan['y_ticks']
        
        df0 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = 'XBIC')
        
        fig = plt.figure() #figsize = scan["figure_size"], dpi = 250
        
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
        
        for ele, legend, pltTitle in zip(ele_plt_list, ele_plt_lab, plt_t):
            df1 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = ele)
            
            fig = plt.figure() #figsize = scan["figure_size"], dpi = 250
            
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


#FOR summed concntration of species as a function of depth
#want to create sum of concentrations for a given "stack depth (x)" and plot vs. x
# converts array of csv into nxm matrix 
def MapsAsMatrices(scan_list, dataframe_as_array):
    plotList = []                                                         #initializes list to contain the shaped channels of interest
    for scan, df in zip(scan_list, dataframe_as_array):
        df1 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = 'XBIC')   #shapes the XBIC channel
        plotList.append(df1)                                                        
        for ele in element_plot_list:
            df2 = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = ele)  #shapes the element channels
            plotList.append(df2)
    return plotList


def integrateStackDepth(imported_shaped_dict):
    for df in imported_shaped_dict:
        column_sum = df.sum(axis = 0, skipna = True)
            
        fig = plt.figure()

        column_sum.plot.line()

    return

def pivot_then_rotate():
    #extract a map as a shaped array, then apply skimage.io rotate, then integrate using functions from NBL3 code
    return