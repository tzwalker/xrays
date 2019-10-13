import h5py
from samp_dict_grow import build_dict

# transform integers in scan list to strings
def str_list(L):
    L = [str(v) for v in L]
    return L

def get_add_h5s(samps, path):
    for samp in samps:
        # make list containing full path+file for each scan
        # make list containing h5 files
        # add h5s to sample dictionary
        c_filenames = [(path + '/2idd_0' + scan + '.h5') for scan in str_list(samp['XBIC_scans'])]
        xbic_h5s = [h5py.File(file, 'r') for file in c_filenames]
        build_dict(samp, 'XBIC_h5s', xbic_h5s)
        
        v_filenames = [(path + '/2idd_0' + scan + '.h5') for scan in str_list(samp['XBIV_scans'])]
        xbiv_h5s = [h5py.File(file, 'r') for file in v_filenames]
        build_dict(samp, 'XBIV_h5s', xbiv_h5s)
    return