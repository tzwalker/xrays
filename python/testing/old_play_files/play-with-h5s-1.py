import h5py as h5

path = r'C:\Users\Trumann\Desktop\XRF-dev\import-h5\2idd_0264.h5'

file = h5.File(path, 'r')

ele = file['/MAPS/channel_names']

