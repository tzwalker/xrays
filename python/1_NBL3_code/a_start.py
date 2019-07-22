import sys
get_defs = 'work'
### paths for custom defintion files and scans ### change according to the operating system environment
if get_defs == 'work':
    custom_def_path = r'C:\Users\Trumann\Desktop\xrays\python\testing\twalker_defs'
    scan_path = r'C:\Users\Trumann\Desktop\NBL3_data\all_H5s'
else:
    custom_def_path = '/home/kineticcross/Desktop/xrays/python/testing/twalker_defs' 
    scan_path = '/home/kineticcross/Desktop/data'
sys.path.append(custom_def_path)

import h5_in_elect_scale as eiDefs
import rummage_thru_H5 as rumH

NBL3_2 = {'Name': 'NBL3-2', 'XBIC_scans': [422,423,424, 550], 'XBIV_scans': [419,420,421, 551], 
          'beam_conv': [2E5,2E5,2E5, 2E5], 
          'c_stanford': [5000,5000,5000, 50000], 
          'c_lockin':[500,500,500, 100], 
          'v_lockin': [1E3,1E3,1E3, 10000],
          '2017_12_ele_iios': [0.275, 0.0446, 0.0550],
          '2019_03_ele_iios': [0.104, 0.00131, 0.00418]}
NBL3_3 = {'Name': 'NBL3-3', 'XBIC_scans': [264,265,266, 475], 'XBIV_scans': [261,262,263, 472], 
          'beam_conv': [2E5, 2E5, 2E5, 1E5], 
          'c_stanford': [5000,5000,5000, 200], 
          'c_lockin':[500,500,500, 20], 
          'v_lockin': [1E4,1E4,1E4, 100000],
          '2017_12_ele_iios': [0.296, 0.0488, 0.0604],
          '2019_03_ele_iios': [0.114, 0.00144, 0.00459]}
TS58A = {'Name': 'TS58A', 'XBIC_scans': [385,386,387, 439], 'XBIV_scans': [382,383,384, 440], 
         'beam_conv': [2E5, 2E5, 2E5, 1E5], 
         'c_stanford': [5000,5000,5000, 200], 
         'c_lockin':[10000,10000,10000, 20], 
         'v_lockin': [1000,1000,1000, 100000],
         '2017_12_ele_iios': [0.381, 0.0682, 0.0867],
         '2019_03_ele_iios': [0.162, 0.00209, 0.00669]}

samples = [NBL3_2, NBL3_3]#], TS58A]

# import the H5s, build the dictionaries above, and scale the electrical signal accordingly
eiDefs.get_add_h5s(samples, scan_path)
eiDefs.get_scan_scalers(samples)
# in get_add_elect_channel() below: 
    # enter 1 if XBIC/V collected through us_ic
    # enter 2 if XBIC/V collected through ds_ic
# otherwise: see README.txt
eiDefs.get_add_elect_channel(samples, 2)  
eiDefs.cts_to_elect(samples)

elements = ['Cu', 'Cd_L']
# adds key value pairs into sample dictionaries
    # example: 'XBIC_eles': [[17,25], [14, 24]]
        # 17 and 14 are the index positions of the Cu_K map in two different scans
        # 25 and 24 are the index positions of the Cd_L map in two different scans
        # this needs to be done as differences in the data structures could exist from 
            # not fitting all scans using the same config file or processing scans from different beamtimes
rumH.find_ele_in_h5s(samples, elements)
# adds element maps to sample dictionaries
rumH.extract_ele_maps(samples)

# now apply XRF correction
# ele_iios in dicts above calculated using iio_vs_depth_simulation.py
    # Cu, Cd_L, and Te_L iios of CdTe layer found by typing in each element
    # and taking the average of the resulting iio vs. depth array
    # attenuation by upstream Mo and ZnTe accounted
rumH.apply_ele_iios(samples)
# checked first couple values in arrays by hand, looks good :)


