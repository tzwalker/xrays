import pandas as pd

path_to_ASCIIs = input("Enter path to ASCIIs here: ")

#notes:
    # local file does not have global list EOI = [Cd_L, Cu, ...]. prompt for input? 


#MAPS saves column headers with whitespace, this function is used to remove that whitespace
def noColNameSpaces(pd_csv_df):
    old_colnames = pd_csv_df.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    pd_csv_df.rename(columns = {i:j for i,j in zip(old_colnames,new_colnames)}, inplace=True)
    return pd_csv_df

def shrinkASCII(large_ASCII_files):
    smaller_dfs = []
    for scan in large_ASCII_files:
        csvIn = pd.read_csv(path_to_ASCIIs + r'/combined_ASCII_2idd_0{n}.h5.csv'.format(n = scan['Scan #']), skiprows = 1)
        noColNameSpaces(csvIn)                                          #removes whitspaces from column headers, for easy access
        shrink1 = csvIn[['x pixel no', 'y pixel no', 'ds_ic']]          #isolates x,y,and electrical columns
        shrink2 = csvIn[EOI]                                            #isolates element of interest columns
        shrink = pd.concat([shrink1, shrink2], axis=1, sort=False)      #combines these columns into one matrix while maintaining indices
        smaller_dfs.append(shrink)                                      #add smaller matrices to list so they may be iterated over...
    return smaller_dfs
