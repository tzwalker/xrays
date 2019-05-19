import h5py as h5

path = '/home/kineticcross/Desktop/XRF-dev/play-import-h5-py'

scans = ['343', '264', '422', '385']

def import_h5s(scans):
    imported_h5s = []
    for scan in scans:
        filename = '/2idd_0' + scan + '.h5'
        f = h5.File(path + filename)
        imported_h5s.append(f)
        
    return imported_h5s

files = import_h5s(scans)

#this line will isolate the Na channel in the h5 and convert it to a string that's identifiable
#channel_names = files[0]['/MAPS/channel_names'][0].decode()

def get_desired_channel_index(channel_names, e):
    s=0
    for index, channel in enumerate(channel_names):
        if e == channel.decode():
            s = index
    return s

#ChOIs = channels_of_interest
ChOIs = ['Cd_L', 'Te_L', 'Cu']

#this function makes a list that  the index of desired channels within the H5 channel
def get_channel_of_interest_index_for_each_scan(files, ChOIs):
    list_of_indices = []                                            #initialize list containing dictionaries for each file/scan
    
    for scan_index, file in enumerate(files):
        channel_names = file['/MAPS/channel_names']
        decoded_ele_string_indices = []
        
        for ele in ChOIs:
            s = get_desired_channel_index(channel_names, ele)
            decoded_ele_string_indices.append(s)

        list_of_indices.append(decoded_ele_string_indices)
        
    return list_of_indices
    

master_ele_index_list = get_channel_of_interest_index_for_each_scan(files, ChOIs)

def extract_maps(H5s, list_of_lists):
    maps = []
    for H5, channel_indices in zip(H5s, list_of_lists):
        scan_maps = []
        XRF_fits = H5['/MAPS/XRF_fits']
        for element_index in channel_indices:
            map_of_interest = XRF_fits[element_index,:,:]
            scan_maps.append(map_of_interest)
        maps.append(scan_maps)
    return maps

master_map_list = extract_maps(files, master_ele_index_list)

#two simple lines to plot the figures! y axis is inverted and not calibrated, but its a quick start :) 
#a = master_map_list[2][2]
#plt.imshow(a)
#having trouble showing only one channel inside the master map list (i.e. grabbing one index inside another index...)


