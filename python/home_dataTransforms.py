import xraylib as xl
import samp_dict_grow
import numpy as np

import numpy as np
import sklearn.preprocessing as skpp
import samp_dict_grow

# the dimensions of 3d axis can be combine with reshape
#y=z.T.reshape(np.shape(z)[1]*np.shape(z)[2], np.shape(z)[0]) #--> stacked maps to psuedo-ASCII column format

def stat_arrs(samples, dict_data, new_dict_data):
    for sample in samples:
        stat_scans = []
        for maps in sample[dict_data]:
            no_nan_maps = maps[:,:,:-2]
            z3Dto2D_rows = np.shape(no_nan_maps)[1]*np.shape(no_nan_maps)[2]
            z3Dto2D_cols = np.shape(no_nan_maps)[0]
            stat_arrs = no_nan_maps.T.reshape(z3Dto2D_rows, z3Dto2D_cols)
            stat_scans.append(stat_arrs)
        samp_dict_grow.build_dict(sample, new_dict_data, stat_scans)
    return

def stand_arrs(samples, dict_data, new_dict_data):
    scaler = skpp.StandardScaler()
    for sample in samples:
        stand_scans = []
        for stat_arrs in sample[dict_data]:
            stand_arrs_sep = [scaler.fit_transform(column.reshape(-1,1)) for column in stat_arrs.T] # is this necessary...? can i apply standardization on whole matrix...
            stand_arrs_comb = np.concatenate(stand_arrs_sep, axis = 1)
            stand_scans.append(stand_arrs_comb)
        samp_dict_grow.build_dict(sample, new_dict_data, stand_scans)
    return

def get_limits(bad_arr, sigma):
    lwr_lim = np.mean(bad_arr) - sigma*np.std(bad_arr)
    upr_lim = np.mean(bad_arr) + sigma*np.std(bad_arr)
    good_logic_arr = np.logical_and(bad_arr >= lwr_lim , bad_arr <= upr_lim)
    good_indices = np.where(good_logic_arr) # get indices within these bounds
    return good_indices

def remove_outliers(samples, dict_data, bad_idx, sigma, new_dict_data):
    for sample in samples:
        no_outliers = []
        for scan_arr in sample[dict_data]:
            bad_arr = scan_arr[:,bad_idx]
            good_indices = get_limits(bad_arr, sigma)
            no_outlier = scan_arr[good_indices]
            no_outliers.append(no_outlier)
        samp_dict_grow.build_dict(sample, new_dict_data, no_outliers)
    return

# generic function to change one element map from ug to mol # 
def ug_to_mol(samp, map_key, scan_idx, eles, e_idx):
    e_list_idx = e_idx-1
    e = eles[e_list_idx]
    if len(e) > 2: e = e[:-2]
    else: pass
    z = xl.SymbolToAtomicNumber(e)
    factor = (1/1E6) * (1/xl.AtomicWeight(z)) #(1g/1E6ug) * (1mol/g)
    mol_map = samp[map_key][scan_idx][e_idx,:,:-2] * factor
    return mol_map

def make_mol_maps(samples, elements, dict_data, new_dict_data):
    elements = [element[0:2] for element in elements]
    mol_masses = [xl.AtomicWeight(xl.SymbolToAtomicNumber(element)) for element in elements]
    #ug/cm2 * (g/ug) * (mol/g) == mol/cm2
    conv_factors = [(1/1E6) / (1/mol_mass) for mol_mass in mol_masses]
    for sample in samples:
        mol_scans = []
        for scan_raw_maps in sample[dict_data]: #CHANGE THIS BACK: FOCUSING ON ZN INCLUDED SCANS
            mol_maps = scan_raw_maps.copy()
            for ele_idx, factor in enumerate(conv_factors):
                map_idx = ele_idx + 1
                ele_map = scan_raw_maps[map_idx,:,:]
                mol_map = ele_map * factor
                mol_maps[map_idx,:,:] = mol_map
            mol_scans.append(mol_maps)
        samp_dict_grow.build_dict(sample, new_dict_data, mol_scans)
    return

def add_ratio_array(samples, dict_data, elem0_idx, elem1_idx):
    for sample in samples:
        scan_array_list = []
        for array in sample[dict_data]:
            if np.size(array.shape) == 2:
                ratio = array[:,elem0_idx] / (array[:,elem0_idx] + array[:,elem1_idx])
                ratio = ratio.reshape(-1,1)
                array = np.concatenate((array, ratio), axis=1)
                scan_array_list.append(array)
            elif np.size(array.shape == 3):
                ratio = array[elem0_idx,:,:] / (array[elem0_idx,:,:] + array[elem1_idx,:,:])
                x = np.shape(ratio)[1]; y = np.shape(ratio)[2]
                ratio = np.reshape(ratio, (1,x,y))
                array = np.concatenate((array, ratio), axis=0)
                scan_array_list.append(array)
            else:
                print('the scan array is neither 2d nor 3d; please try again')
            sample[dict_data] = scan_array_list
    return

if '__main__' == __name__:
    eles = ['Cu', 'Cd_L', "Te_L"]
    make_mol_maps(samples, eles, 'XBIC_corr', 'XBIC_mol')
    print('success')
