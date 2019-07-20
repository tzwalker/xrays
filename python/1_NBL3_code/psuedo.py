# =============================================================================
# wanted =        ['cu', 'cd', 'te']
# h5_channels =   ['cd', 'fe', 'cu', 'zn', 'se', 'te']
# h5_channels = [x.encode('utf-8') for x in h5_channels]
# 
# def find_eles_in_channel_names(w, chan):
#     chan = [x.decode('utf-8') for x in chan]
#     index_list = [i for i,ele in enumerate(chan) for e in w if e == ele]
#     return index_list
# 
# new_list = find_eles_in_channel_names(wanted, h5_channels)
# =============================================================================

for v in f['/MAPS']:
    print(v)
    
import h5py

f = h5py.File(scan_path + '/2idd_0439.h5')
