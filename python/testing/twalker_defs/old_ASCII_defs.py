import pandas as pd
import numpy as np


#supplement to "shrinkASCII()": MAPS exports ASCIIs with column header whitespace, this removes that whitespace
def noColNameSpaces(pd_csv_df):
    old_colnames = pd_csv_df.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    pd_csv_df.rename(columns = {i:j for i,j in zip(old_colnames,new_colnames)}, inplace=True)
    return pd_csv_df

#IMPORT AND SHIRNK DATAFRAME: imports and shrinks ASCII according to what elements are specified and the sector the scan was taken
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

# to "FS_bias.py"
def import_line_ASCIIS(scans):
    line_scans = []
    usecols = list(range(7))                                            #line plots exported only with ds_ic channel
    for scan in scans:
        s = str(scan)
        filename = r'\line2idd_0'+s+'.h5.csv'
        df = pd.read_csv(path_to_ASCIIs + filename, usecols=usecols)
        noColNameSpaces(df)
        line_scans.append(df)
    return line_scans

### plotting in ASCII format ###
def mapConvertAxes(dataframes, scans):
    for df, scan in zip(dataframes, scans):
        height_factor = scan['height'] / scan['y_points']                       #converts to (um/line) for y-direction
        width_factor = scan['width'] / scan['x_points']                         #converts to (um/line) for x-direction
        df['y pixel no']  = df['y pixel no'] * height_factor                    #OVERWRITE Y PIXEL COLUMN: ypixel-no/line *(um/line) = um (y)
        df['x pixel no']  = df['x pixel no'] * width_factor                     #OVERWRITE X PIXEL COLUMN: xpixel-no/line *(um/line) = um (x)
    return

def mapShape(dataframe_list):
    plotList = []
    for df in dataframe_list:
        df = df.pivot(index = 'y pixel no', columns = 'x pixel no', values = 'XCE') #shape XCE column into map accroding to converted x and y column indices
        plotList.append(df)                                                         #store shaped dfs in list
    return plotList

### (older) for ASCIIs ###
def collect_XBIC(small_dfs, scan_list):
    eh_per_coulomb = 1/(1.60217634*10**-19)                                  #most recent accepted value for electrons per coulomb
    XBIC_switch = int(input('Type 0 for XBIC, 1 for ehPairs: '))
    
    if XBIC_switch == 0:
        for df, scan in zip(small_dfs, scan_list):
            df["ds_ic"] = df["ds_ic"].astype(float)                             #reformat column for floating arithmetic operations
            scaled_dsic = df.loc[:,'ds_ic'] * scan['scale factor']              #apply amplifaction settings  (converts counts to amps)
            df['ds_ic'] = scaled_dsic
            df.rename(columns = {'ds_ic': 'XBIC'}, inplace = True)  
        
        
    if XBIC_switch == 1:
        for df, scan in zip(small_dfs, scan_list):
            df["ds_ic"] = df["ds_ic"].astype(float)                             #reformat column for floating arithmetic operations
            scaled_dsic = df.loc[:,'ds_ic'] * scan['scale factor']              #apply amplifaction settings  (converts counts to amps)
            collected_dsic = scaled_dsic * eh_per_coulomb                       #convert amps to e-h pairs
            df['ds_ic'] = collected_dsic
            df.rename(columns = {'ds_ic': 'eh_pairs'}, inplace = True)                        
    return 
    
#CALCULATE XBIC
def generate_scalar_factor(scan_list):
    beamconversion_factor = 100000
    for scan in scan_list:
        correction = ((scan['stanford']*(1*10**-9)) / (beamconversion_factor * scan['lockin']))     #calculate scale factor for chosen scan
        key = 'scale factor'                                                                        #CREATE: define key for scan dictionary
        scan.setdefault(key, correction)                                                            #add key and correction factor to scan
        #print(correction)
    return

def collect_XBIC(list_of_smaller_dfs):
    eh_per_coulomb = 1/(1.60217634*10**-19)                                             #most recent accepted value for electrons per coulomb
    for df, scan in zip(list_of_smaller_dfs, scan_list):
        df["ds_ic"] = df["ds_ic"].astype(float)                                         #reformat column for floating arithmetic operations
        scaled_dsic = df.loc[:,'ds_ic'] * scan['scale factor']                          #apply amplifaction settings  (converts counts to amps)
        collected_dsic = scaled_dsic * eh_per_coulomb                                   #convert amps to e-h pairs
        df['ds_ic'] = collected_dsic                                                    #OVERWRITE ds_ic column with number of e-h pairs
        df.rename(columns = {'ds_ic': 'eh_pairs'}, inplace = True)                        
    return 

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

import xraylib as xl

beam_energy = 8.99                                                  #beamtime keV
beam_theta = 90                                                     #angle of the beam relative to the surface of the sample
beam_geometry = np.sin(beam_theta*np.pi/180)                        #convert to radians
detect_theta = 47                                                   #angle of the detector relative to the beam
detect_gemoetry = np.sin(detect_theta*np.pi/180)                    #convert to radians
dt = 1 * (1*10**-3) * (1*10**-4)                                   #convert 1nm step sizes to cm: 1nm * (1um/1000nm) * (1cm/10000um)

#enter lengths in cm
MO =    {'Element':['Mo'],          'MolFrac':[1],      'Thick':0.00005,    'LDensity': 10.2, 'Name': 'Mo',     'capXsect': xl.CS_Total_CP('Mo', beam_energy)}
ZNTE =  {'Element':['Zn','Te'],     'MolFrac':[1,1],    'Thick':0.0000375,  'LDensity': 6.34, 'Name': 'ZnTe',   'capXsect': xl.CS_Total_CP('ZnTe', beam_energy)}
CU =    {'Element':['Cu'],          'MolFrac':[1],      'Thick':0.000001,   'LDensity': 8.96, 'Name': 'Cu',     'capXsect': xl.CS_Total_CP('Cu', beam_energy)}
CDTE =  {'Element':['Cd','Te'],     'MolFrac':[1,1],    'Thick':0.0005,    'LDensity': 5.85, 'Name': 'CdTe',   'capXsect': xl.CS_Total_CP('CdTe', beam_energy)}
CDS =   {'Element':['Cd','S'],      'MolFrac':[1,1],    'Thick':0.000008,   'LDensity': 4.82, 'Name': 'CdS',    'capXsect': xl.CS_Total_CP('CdS', beam_energy)}
SNO2 =  {'Element':['Sn','O'],      'MolFrac':[1,2],    'Thick':0.00006,    'LDensity': 6.85, 'Name': 'SnO2',   'capXsect': xl.CS_Total_CP('SnO2', beam_energy)}

#COMBINE THE LAYERS FROM ABOVE INTO A LIST (UPTREAM LAYER FIRST, DOWNSTREAM LAYER LAST)
STACK = [MO, ZNTE, CU, CDTE, CDS, SNO2]

def getSublayers(layer):
    T = layer['Thick']                                          #layer thickness in cm
    sublayers = T/dt                                            #number of 10nm sublayers in the layer
    sublayers = round(sublayers)
    sublayers = int(sublayers)
    key = 'numSublayers'                                        #add key to layer dictionary (for convenience)
    layer.setdefault(key, sublayers)                            #connect key to number of sublayers calculated
    return sublayers

#attenuation of beam intensity through each layer
def IncidentBeamAttenuation(stack_list):
    Bo_previous = 1
    for layer in STACK:
        Bo = Bo_previous * np.exp(- layer['capXsect'] * layer['LDensity'] * layer['Thick'])         #cm2/g * g/cm3 * cm; calculate bulk attenuation of layers external to the layer chosen
        rounded_Bo = round(Bo, 7)                                                                   #round Bo to 7 decimals for memory conservation
        key = 'Bo'                                                                                  #add key to layer dictionary (for later access)
        layer.setdefault(key, rounded_Bo)                                                           #store rounded incident beam attenuation of layer
        Bo_previous = Bo                                                                            #attenuation calculated for this layer to be used as incident beam intensity of next layer (when the for loop moves to next layer, Bo_previous is now the value calculated for previous layer)
    return

IncidentBeamAttenuation(STACK)


#returns the energy of fluorescent photon of a given element due to the beam energy
#if-statements checks whether the element will absorb; is absorption edge higher than beam_energy?
    #if yes, no absorption, fluorescent photon energy is set to the next highest energy of the next shell
        # ex) Cd_L = 3.1338 keV , Cd_K_edge = 26.7, Cd_L_edge = 4.018
        #       
    #if no, absorption, fluorescent photon energy remains at the highest energy of the current shell
    
    ##functions of interest!
    #element_XRF_energy = xl.LineEnergy(xl.SymbolToAtomicNumber("element"), xl.XRF line you want)
    #Layer_cataching_ele_XRF = xl.CS_Total_CP("layer", element_XRF_energy)
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



#outgoing fluorescence of external layers
def get_capXsect_of_layer_on_ele_line(layer, layer_element_list):
    for ele in layer_element_list:
        ext_layer_capXsect_on_ele_line = xl.CS_Total_CP(layer["Name"], get_Ele_XRF_Energy(ele, beam_energy))
    return ext_layer_capXsect_on_ele_line

