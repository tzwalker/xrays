def XBIC_counts_to_amp(scan_list):
    beamconversion_factor = 100000
    correction_factors = []
    for scan in scan_list:
        correction = ((scan['stanford']*(1*10**-9)) / (beamconversion_factor * scan['lockin'])) #calculate correction factor for chosen scan
        correction_factors.append(correction)
        key = 'Scan ' + str(scan['Scan #']) + ' XBIC scale Factor (A)'                     #define key for scan dictionary
        scan.setdefault(key, correction)                        #add key and correction factor to scan
    return correction_factors

def scale_XBIC(list_of_smaller_dfs):
    for df, factor in zip(list_of_smaller_dfs, correction_factors):
        df["ds_ic"] = df["ds_ic"].astype(float)                     #reformat column for floating arithmetic operations
        correct_dsic = df.loc[:,'ds_ic'] * factor                   #apply amplifaction settings   
        df['ds_ic'] = correct_dsic                                  #replace XBIC (cts) with XBIC (nA)
    return 


