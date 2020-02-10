import sys
data_path = r'C:\Users\Trumann\Desktop\NBL3_data\all_H5s'
pymodule_path = r'C:\Users\Trumann\Desktop\xrays\python'
sys.path.append(pymodule_path)
import home_defs
import home_stat

# sample dictionary
  # electrical settings from the runnnotes
  # scan index and setting index should be identical
      # ex) XBIC scan 422 electrical settings: 
        # beam_conv (V2F converter) =       2E5 cts/V
        # stanford pre-amplifier (nA) =     5E5 nA/V
        # lock-in scale =                   500 V/V
      # example XBIV scan 419 electrical settings:
        # lock-in scale =                   1E3 V/V
sample_dict0 = {'Name': 'NBL3_2', 
          'XBIC_scans':     [422,538,550],
          'beam_conv':      [2E5,2E5,2E5], #(cts/V)
          'c_stanford':     [5E3,5E4,5E4], #(nA/V)
          'c_lockin':       [500,100,100], #(V/V)
          'XBIV_scans':     [419,551],     
          'v_lockin':       [1E3,1E4],     #(V/V)

          'STACK': {
          'Mo':     [10.2, 500E-7],        #[layer_compound_density, layer_thickness]
          'ZnTe':   [6.34, 375E-7], 
          'Cu':     [8.96, 2.5E-7], 
          'CdTe':   [5.85, 8.52E-4], 
          'CdS':    [4.82, 80E-7], 
          'SnO2':   [100E-7]}
          }
sample_dict1 = {'Name': 'NBL3_3', 
          'XBIC_scans':     [264,265,475],  
          'beam_conv':      [2E5,2E5,1E5], 
          'c_stanford':     [5E3,5E3,200], 
          'c_lockin':       [500,500,20], 
          'XBIV_scans':     [261,262,263],
          'v_lockin':       [1E4,1E4,1E4],
          'STACK': {
          'Mo':     [10.2, 500E-7], 
          'ZnTe':   [6.34, 375E-7],
          'Cu':     [8.96, 10E-7], 
          'CdTe':   [5.85, 10.85E-4], 
          'CdS':    [4.82, 80E-7], 
          'SnO2':   [100E-7]}
          }
          
samples = [sample_dict0, sample_dict1]
# import all h5 data
home_defs.import_h5s(samples, data_path)
# enter element maps you want to focus on (include XRF lineif not a K-line)
    # keep the index of the elment in mind
elements = ['Cu', 'Cd_L', 'Te_L', 'Mo_L']

# extract fitted data of above elements from h5
home_defs.import_maps(samples, 'XBIC', 2, elements, 'us_ic', 'fit') 
#home_defs.import_maps(samples, 'XBIV', 2, elements, 'us_ic', 'fit')
print(samples[0].keys())
#%%
import home_abs
# define layer for which you want to perform XRF correction
iio_layer = 'CdTe'
# enter elements which you wish to correct
iio_elements = ['Cu', 'Cd', 'Te']
# align element indices
ele_map_idxs = [1,2,3] #--> index of element in 'elements'
ele_iio_idxs = [0,1,2] #--> index of element in 'iio_elements'

### 2019_03 beamtime
# enter energy in keV, theta in degrees
beam_settings0 = {'beamtime': '2019_03','beam_energy': 12.7, 'beam_theta':75, 'detect_theta':15}
home_abs.get_layer_iios(samples, iio_elements, beam_settings0, iio_layer) 
# enter index of scans you want to correct for each sample
sample_scan_idxs=[[0], [0,1]] 
home_abs.apply_iios(samples, 'XBIC', sample_scan_idxs, '2019_03_iios', ele_map_idxs, ele_iio_idxs, 'XBIC_corr0')

### 2017_12 beamtime
beam_settings1 = {'beamtime': '2017_12','beam_energy': 8.99, 'beam_theta':90, 'detect_theta':43}
home_abs.get_layer_iios(samples, iio_elements, beam_settings1, iio_layer)
# enter index of scans you want to correct for each sample
sample_scan_idxs=[[1,2], [2]] 
home_abs.apply_iios(samples, 'XBIC', sample_scan_idxs, '2017_12_iios', ele_map_idxs, ele_iio_idxs, 'XBIC_corr1')

home_abs.join_corrected_beamtimes(samples, ['XBIC_corr0', 'XBIC_corr1'], 'XBIC_corr')
#%%
home_defs.make_mol_maps(samples, elements, 'XBIC_corr', 'XBIC_mol')
#home_defs.make_mol_maps(samples, elements, 'XBIV_corr', 'XBIV_mol')
print(samples[0].keys())

#%%
home_stat.stat_arrs(samples, 'XBIC_corr', 'XBIC_stat')
#home_stat.stat_arrs(samples, 'XBIV_corr', 'XBIV_stat')
print(samples[0].keys())
#%%
home_stat.stand_arrs(samples, 'XBIC_stat', 'XBIC_stand')
#home_stat.stand_arrs(samples, 'XBIV_stat', 'XBIV_stand')
print(samples[0].keys())
