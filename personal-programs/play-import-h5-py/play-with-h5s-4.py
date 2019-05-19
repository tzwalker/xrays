import h5py as h5
import matplotlib.pyplot as plt


path = r'C:\Users\Trumann\Desktop\XRF-dev\personal-programs\play-import-h5-py'

scans = ['264', '422', '385']

def import_h5s(scans):
    imported_h5s = []
    for scan in scans:
        filename = '/2idd_0' + scan + '.h5'
        f = h5.File(path + filename)
        imported_h5s.append(f)
        
    return imported_h5s

files = import_h5s(scans)

#this function performs a strign comparison within the pertinent H5 group and extracts the index of interest
def get_desired_channel_index(H5_channel_names_as_strings, e):
    s=0                                                                             #initialize index search
    for index, channel_string in enumerate(H5_channel_names_as_strings):            #search channel_names for element string
        if e == channel_string.decode():                                            #compare element string to decoded channel_name string
            s = index                                                               #get appropriate index
    return s

#ChOIs = channels_of_interest
ChOIs = ['Cd_L', 'Te_L', 'Cu']

#this function makes a master list containing the index of the channel of interest within each respective scan
#the master list is a list of lists, where each internal list represents a scan
#each internal list contains the indices of the channels of interest for that specific scan, which may not be the same between scans
#the extraction of channel indices is required because this is how one navigates the H5 data structures
def get_ChOIs_for_all_scans(files, ChOIs):
    list_of_indices = []                                            #initialize master list
    
    for scan_index, file in enumerate(files):
        channel_names = file['/MAPS/channel_names']                 #navigate to the structure conatining the channel names as element strings, e.g. 'Cd_L'
        decoded_ele_string_indices = []                             #initialize internal list
        
        for ele in ChOIs:
            s = get_desired_channel_index(channel_names, ele)       #perform string comparison between 'channels of interest' and 'channel names', and extract index of interest
            decoded_ele_string_indices.append(s)                    #build internal list

        list_of_indices.append(decoded_ele_string_indices)          #add internal list (i.e. a scan) to master list
        
    return list_of_indices
    

master_index_list = get_ChOIs_for_all_scans(files, ChOIs)

#this function uses the element indices from the master_index_list to extract the 2D fitted data arrays from the H5 file
#it also build a master list that contains the 2D numpy arrays of interest, rather than just the indices
def extract_maps(H5s, list_of_lists):
    maps = []                                                       #initialize master list
    for H5, channel_indices in zip(H5s, list_of_lists):
        scan_maps = []                                              #initialize internal (single scan) list
        XRF_fits = H5['/MAPS/XRF_fits']                             #navigate to structure containing all fitted XRF data
        for element_index in channel_indices:
            map_of_interest = XRF_fits[element_index,:,:]           #use element index to extract map of interest
            scan_maps.append(map_of_interest)                       #build internal list
        maps.append(scan_maps)                                      #add internal list (i.e. a scan) to master list
    return maps

master_map_list = extract_maps(files, master_index_list)

#still debugging plotting function; see finished code in XRF-dev at home...
# =============================================================================
# for scan in master_map_list:
#     fig = plt.figure()
#     for channel in scan:
#         plt.imshow(channel)
#     cu_channel = scan[1]
#     plt.imshow(cu_channel, origin = 'lower')
# # =============================================================================
# #     for index, channel in enumerate(scan):
# #         Cu_channel = channel
# #         plt.imshow(channel, origin = 'lower')
# # =============================================================================
# 
# =============================================================================


