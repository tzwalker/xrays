import defs_NBL3_xSect as xsect_defs
import numpy as np

path = r'C:\Users\Trumann\Desktop\NBL3_data\cross_sections_MS\csvs'
sample = 'NBL31'
scannum = 8
channels = ['XBIC_lockin', 'Cu_K', 'Cd_L3']
meta_data = xsect_defs.get_scan_metadata(path, sample, scannum)
rotation = 0

imported_rotated_dataframes = xsect_defs.import_xSect_csvs(path, sample, scannum, channels, meta_data, rotation)

# there should be as many entries in these lists as channels imported
ch_units = ['nA', '\u03BCg/cm'+ r'$^{2}$', '\u03BCg/cm'+ r'$^{2}$']
heat_colors = ['magma', 'Oranges_r', 'viridis']
#xsect_defs.plot_2D_xSect(imported_rotated_dataframes, ch_units, heat_colors)

def export_integrated_dfs(imp_rot_dfs):
    integrated_arrays_of_each_channel = []
    x = imp_rot_dfs[0].columns.values
    x = x.reshape(-1,1)
    for df in imp_rot_dfs:
        y_integrate = df.sum(axis=0)        #df
        y_integrate = y_integrate.to_numpy()
        y_integrate = y_integrate.reshape(-1,1)
        integrated_arrays_of_each_channel.append(y_integrate)
    integrated_arrays_of_each_channel.insert(0, x)
    arrays = np.concatenate(integrated_arrays_of_each_channel, axis=1)
    return arrays

arrays = export_integrated_dfs(imported_rotated_dataframes)
np.savetxt(r'C:\Users\Trumann\Dropbox (ASU)\1_NBL3 data\py_' + sample +"_Scan"+ str(scannum) + '.csv', arrays, delimiter = ',')
