import numpy as np
import pandas as pd

for scan in self.scans:
    scan_str = str(scan)
    # define ascii of scan
    file = path_ascii + '/combined_ASCII_2idd_0'+scan_str+'.h5.csv'
    # import ascii as dataframe
    data = pd.read_csv(file)
    # dataframe keys used for shaping into map
    i = 'y pixel no'; j='x pixel no'
    # extract maps of interest; shape according to pixel no
    data_shape = [data.pivot(index=i, columns=j, values=c) for c in CH]
    # convert dataframes to numpy arrays
    data_arr = [df.to_numpy() for df in data_shape]
    # prepare electrical map for cts to ampere
    electrical_map = data_arr[0]
    # get electrical factor for xbic
    factor = get_lockin(scan, path_lockin)
    # convert electrical: cts to ampere
    data_arr[0] = electrical_map*factor
    # stack numpy arrays (into 3D)
    data_stack = np.array(data_arr)
    # store stacked numpy arrays
    name = 'scan' + scan_str
    setattr(self, name, data_stack) # useful for plotting & reference
    self.maps.append(data_stack) #useful w/ code before 20200402