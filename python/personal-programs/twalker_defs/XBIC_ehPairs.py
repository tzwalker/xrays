def generate_scalar_factor(scan_list):
    beamconversion_factor = 100000
    for scan in scan_list:
        correction = ((scan['stanford']*(1*10**-9)) / (beamconversion_factor * scan['lockin']))     #calculate scale factor for chosen scan
        key = 'scale factor'                                                                        #define key for scan dictionary
        scan.setdefault(key, correction)                                                            #add key and correction factor to scan
        #print(correction)
    return



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
