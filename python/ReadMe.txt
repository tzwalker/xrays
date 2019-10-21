This folder contains python code that can import, correct, and plot x-ray fluorescence data. The data is extracted from HDF5 (H5) file structures obtained from measurements Sector 2-ID-D Argonne Nat'l Lab.

The user is meant to interact with "home.py" and "pretty_plotting.py". The folder and the "example_data" folder should be downloaded/copied to a local path---not a server or Dropbox folder---to avoid read/write permission complications. A small example set of H5 data is included in the folder "example_data".

The programs/functions operate on the idea of transforming and building each sample's python dictionary. If the user is a python beginner, they should definitely become familiar with python dicitonaries and how to access entries within them before trying to use these programs. I reccommend: http://anh.cs.luc.edu/handsonPythonTutorial/dictionaries.html

Many of the functions provided allow the user to customize these dictionaries with whatever descriptive keys they wish. I do not advise attempting this until you are comfortable navigating the structures using the keys provided. To demonstrate how the sample dictionaries grow, the line "print(samples[0].keys())" is provided at various points throughout "home.py"


A brief description of each function is given here using the syntax "module.py/function_definition()". A function argument will be a descriptive term of what that positional argument is supposed to represent.

home_defs.py/import_h5s(samples, scan_path)
	adds h5 files to sample dictionary according to the scan numbers provided in the sample dictionary

home_defs.py/import_maps(samples, electrical_scans, electrical_channel, elements, XRF_normalization, XRF_quantification)
	converts electrical channel to amps and elemental channels to their respective area densities
		electrical_channel: 1 or 2 --> electrical signal collected through upstream or downstream ion chamber
		XRF_normalization: 'us_ic' or 'ds_ic' --> normalize to ion chamber cts/s 
		XRF_quantification == 'fit' or 'roi'--> quantify using fitted or raw area density conversion
	quantification_normalization

home_abs.py/get_layer_iios(samples, iio_elements, beam_settings0, iio_layer)
	retrieves iios for a given sample based on the measurement geometry and sample stack
	
home_abs.py/apply_iios(samples, electrical_scans, scans_of_interest, beamtime_iios, ele_map_idxs, ele_iio_idxs)
	scans_of_interest: a list fo lists; each sublist contains the indices of the scans for one sample
	beamtime_iios: key in sample dictionary to get iios; mathces the beamtime settings the iios represent
	idx arguments: used to apply an iio to the correct element map
		This function can be used to apply the absorption corrections for scans taken at multiple beamtimes, and the example for that is given in the home.py file. It is not necessary to import scans from different beam times, and avoiding this will simplify the code considerably. For simplicity, only the XBIC scans are shown in "home.py". Unfortunately, the this fuction must separate the data, but they can be easily recombined into a list resembling the original scan list by using "join_corrected_beamtimes()".
		
home_abs.py/join_corrected_beamtimes(samples, list_of_keys_to_combine, new_key_for_correct_data)
	simple function combining the different dict entries containing corrected XRF data

home_defs.py/make_mol_maps(samples, elements, corrected_XRF, new_key_for_mol_data)
	converts area density to molar area density; keeps both data

home_stat.py/stat_arrs(samples, corrected_data_key, new_key_for_stat_data)
	chops off extra NaN columns produced from flyscans and ravels the maps into a single array
		each row is a pixel, and each column is the feature (e.g. XBIC, Cu, Cd, Te, Mo)

home_stat.py/stand_arrs(samples, corrected_data_key, new_key_for_standardized_data)
	standardizes each feature in the statisitic array made by stat_arrs() for each sample


Miscellaneous nuances:
only the elements that were included during fitting will be imported; one way to check if they were  included is to check if the depth of "sample_dict['XBIC_maps']" matches length of "elements" e.g. 
len(elements) == np.shape(sample_dict['XBIC_maps'])[0] --> True

When applying iios, the number of sublists for each beamtime (i.e. the number of samples considered) needs to be the same.

Use the functions in pretty_plotting.py to plot the data according to scan and feature indices. Annotations are provided in that file.

Please contact me if you have questions!
