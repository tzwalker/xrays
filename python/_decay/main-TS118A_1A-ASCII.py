"""
coding: utf-8

tzwalker
Wed May 27 18:25:55 2020

analyses for XBIC decay data

"""

from class_ascii_Sample import Sample
ASCII_PATH =  r'C:\Users\triton\decay_data' 
PATH_LOCKIN = r'C:\Users\triton\Dropbox (ASU)\1_XBIC_decay\decay_electrical.csv'

# create sample objects
TS1181A = Sample()

# define stack and scans of each sample
TS1181A.stack = {'Au':   [19.3, 100E-7], 
                 'CdTe': [5.85, 5E-4],
                 'Se': [4.82, 100E-7],
                 'SnO2': [100E-7]}
TS1181A.scans = [39,51]


# channels to import from ASCII
channels = ['26idc:3820:scaler1_cts2.B', 'Cu', 'Cd_L', 'Te_L', 'Au_M']

TS1181A.import_maps(ASCII_PATH, PATH_LOCKIN, channels, sector=26)

elements = [ele[0:2] for ele in channels[1:]]

#FS3.ug_to_mol(elements)
# attribute Sample.mol now exists; contains XRF maps as mol/cm2

# =============================================================================
# beam_settings = {'beam_energy': 12.7, 'beam_theta':75, 'detect_theta':15}
# 
# FS3iios = XRFcorr.get_iios(beam_settings, elements, FS3.stack, end_layer='Se')
# scans_for_correction = FS3.scans
# FS3.apply_iios(scans_for_correction, FS3iios)
# =============================================================================

# =============================================================================
# # quick idea: for unfiltered map, sum along an axis and compare to 
# # unfiltered timeseries
# 
# unfilt = TS1181A.scan195[0,:,:]
# b = np.sum(unfilt, axis=1)
# plt.plot(b)
# =============================================================================
