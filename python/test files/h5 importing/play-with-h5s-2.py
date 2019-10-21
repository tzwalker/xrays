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
files[0]['/MAPS/channel_names'][0].decode()

for ele_string in files[0]['/MAPS/channel_names']:
    print(ele_string)

channels_of_interest = ['Cd_L', 'Te_L', 'Cu']

def get_desired_channel_indices(channel_names,e):
    s=0
    for index, channel in enumerate(channel_names):
        if e == channel.decode():
            s = index
    return s

def indices_of_interest(channels_of_interest):
    decoded_ele_strings = []
    for ele in channels_of_interest:
        s = get_desired_channel_indices(channel_names, ele)
        decoded_ele_strings.append(s)
    return decoded_ele_strings

indices_for_mapping = indices_of_interest(channels_of_interest)


XRF_fits = f['/MAPS/XRF_fits']

maps = []
for index in indices_for_mapping:
    map_of_interest = XRF_fits[index,:,:]
    maps.append(map_of_interest)
    