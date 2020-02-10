import h5py as h5

path = '/home/kineticcross/Desktop/XRF-dev/play-import-h5-py'

sample_names = ['NBL3_1', 'NBL3_2', 'NBL3_3', 'TS58A']
scans = ['343', '264', '422', '385']

def import_h5s(scans, sample_names):
    imported_h5s = {}
    
    for scan, name in zip(scans, sample_names):
        filename = '/2idd_0' + scan + '.h5'
        f = h5.File(path + filename)
        
        key1 = name + '_' + scan
        imported_h5s.setdefault(key1, scan)
        key2 = scan + '_H5'
        imported_h5s.setdefault(key2, f)
    return imported_h5s

MASTER = import_h5s(scans, sample_names)

#example of syntax for navigating H5
#channel_names = files[0]['/MAPS/channel_names'][0].decode()

#ChOIs = channels_of_interest
ChOIs = ['Cd_L', 'Te_L', 'Cu']
# =============================================================================
# 
# #
# def get_desired_channel_index(channel_names, e):
#     s=0
#     for index, channel in enumerate(channel_names):
#         if e == channel.decode():
#             s = index
#     return s
# 
# #this function makes a list that the index of desired channels within the H5 channel
# def get_channel_of_interest_index_for_each_scan(files, ChOIs):
#     list_of_file_dicts = []                                     #initialize list to contain dictionaries for each file/scan
#                                            
#     for scan_index, file in enumerate(files):
#         file_dict = {}                                          #initialize dictionary for chosen file/scan
#         decoded_ele_string_indices = []                         #initialize list to contain element of interest indices in H5 (to be used for mapping later)
#         channel_names = file['/MAPS/channel_names']             #access group containing coded strings for element channel names
#         
#                                
#         for ele in ChOIs:
#             s = get_desired_channel_index(channel_names, ele)   #find element of interest index in the H5
#             decoded_ele_string_indices.append(s)                #build list containing element of indices list
#         
#         #build dictionary for file/scan; give both a file name and 
#         key2 = 'scan_num'
#         file_dict.setdefault(key2, scans[scan_index])
#         key = 'ChOIs indices'
#         file_dict.setdefault(key, decoded_ele_string_indices)
# 
#         list_of_file_dicts.append(file_dict)
#     return list_of_file_dicts
#     
# 
# what = get_channel_of_interest_index_for_each_scan(files, ChOIs)
# =============================================================================

###MIGHT BE EASIER TO BUILD MASTER DICTIOANRY IN IMPORTH5 RATHER THAN HAVE A SEPARATE
###LIST CONTAINING THE FILES...


# =============================================================================
# 
# XRF_fits = f['/MAPS/XRF_fits']
# 
# maps = []
# for index in indices_for_mapping:
#     map_of_interest = XRF_fits[index,:,:]
#     maps.append(map_of_interest)
# =============================================================================
    