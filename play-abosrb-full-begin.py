#this file is for testing

def get_iio_in(layer_index, layer_dict):
    
    
    
    return attenuation_of_incdent_beam_thru_upstream_layers

for index, layer in enumerate(STACK):
    iio_in = get_iio_in(index, layer)
    iio_out = get_iio_out(index, layer)
    iio_array = get_iio_array(index, layer)
    ele_iio = np.mean(iio_array)