import xraylib as xl
import numpy as np

from importASCII_shrink import shrinkASCII
from XBIC_corrections import scale_XBIC, XBIC_counts_to_amp



path_to_ASCIIs = '/home/kineticcross/Desktop/XRF-dev'
EOI = ['Sn_L', 'S', 'Cd_L', 'Te_L', 'Cu', 'Zn_L', 'Cl', 'Mo_L']

scan439 = {'Scan #': 439, 'Name': 'TS58A XBIC', 'stanford': 200, 'lockin': 20, 'PIN beam_on': 225100, 'PIN beam_off': 624, 'PIN stanford': 500} 
scan440 = {'Scan #': 475, 'Name': 'NBL3-3 XBIC', 'stanford': 200, 'lockin': 20, 'PIN beam_on': 225100, 'PIN beam_off': 624}
scan450 = {'Scan #': 519, 'Name': 'NBL3-1 XBIC', 'stanford': 200, 'lockin': 20, 'PIN beam_on': 225100, 'PIN beam_off': 624}
scan451 = {'Scan #': 550, 'Name': 'NBL3-2 XBIC', 'stanford': 5000, 'lockin': 100, 'PIN beam_on': 225100, 'PIN beam_off': 624}

scan_list = [scan439, scan440, scan450, scan451]

smaller_dfs = shrinkASCII(scan_list)

correction_factors = XBIC_counts_to_amp(scan_list)

scale_XBIC(smaller_dfs)

# =============================================================================
# def interpolate_diode_calibration():
#     #enter ASU PIN diode values @ 12.8 and 8.08 keV
#     #prompt for energy of interest
#     #interpolate
#     #store interoolated value as key in scan dictionary
#     #reference key in get_flux
#     return
# 
# def get_flux(scan):
#     beamconversion = 10000
#     flux = ((scan['PIN beam_on'] - scan['PIN beam_off'])  /  beamconversion) * (scan["PIN stanford"] *10**-9) * scan["PIN calib"]
#     return
# =============================================================================


EOIs = ['Sn', 'S', 'Cd', 'Te', 'Cu', 'Zn', 'Cl', 'Mo']

beam_energy = 8.99                                                  #beamtime keV
beam_theta = 90                                                     #angle of the beam relative to the surface of the sample
beam_geometry = np.sin(beam_theta*np.pi/180)                        #convert to radians
detect_theta = 47                                                   #angle of the detector relative to the beam
detect_gemoetry = np.sin(detect_theta*np.pi/180)                    #convert to radians
dt = 10 * (1*10**-3) * (1*10**-4)                                   #convert 10nm step sizes to cm: 10nm * (1um/1000nm) * (1cm/10000um)


SNO2 =  {'Element':['Sn','O'],      'MolFrac':[1,2],    'Thick':0.6,    'LDensity': 6.85, 'Name': 'SnO2'}
CDS =   {'Element':['Cd','S'],      'MolFrac':[1,1],    'Thick':0.08,   'LDensity': 4.82, 'Name': 'CdS'}
CDTE =  {'Element':['Cd','Te'],     'MolFrac':[1,1],    'Thick':5.0,    'LDensity': 5.85, 'Name': 'CdTe'}
CU =    {'Element':['Cu'],          'MolFrac':[1],      'Thick':0.01,   'LDensity': 8.96, 'Name': 'Cu'}
ZNTE =  {'Element':['Zn','Te'],     'MolFrac':[1,1],    'Thick':0.375,  'LDensity': 6.34, 'Name': 'ZnTe'}
MO =    {'Element':['Mo'],          'MolFrac':[1],      'Thick':0.5,    'LDensity': 10.2, 'Name': 'Mo'}

#COMBINE THE LAYERS FROM ABOVE INTO A LIST (TOP LAYER FIRST, BOTTOM LAYER LAST)
layers = [MO, ZNTE, CU, CDTE, CDS, SNO2]
###
#the following functions compress xraylib functions to make the code more readable
def ele_dens(atomicNumber):
    D = xl.ElementDensity(atomicNumber)
    return D

def ele_weight(atomicNumber):
    W = xl.AtomicWeight(atomicNumber)
    return W

def symToNum(sym):
    S = xl.SymbolToAtomicNumber(str(sym))
    return S

def capXsect(element, energy):
    C = xl.CS_Total(symToNum(element), energy)
    return C
###

def XRF_line(Element,Beam_Energy):
    Z = xl.SymbolToAtomicNumber(str(Element))       #converts element string to element atomic number
    F = xl.LineEnergy(Z,xl.KA1_LINE)                #initialize energy of fluorescence photon as highest energy K-line transition for the element
    if xl.EdgeEnergy(Z,xl.K_SHELL) > Beam_Energy:       #if beam energy is less than K ABSORPTION energy,
            F = xl.LineEnergy(Z,xl.LA1_LINE)            #energy of fluorescence photon equals highest energy L-line transition for the element
            if xl.EdgeEnergy(Z,xl.L1_SHELL) > Beam_Energy:      #if beam energy is less than L1 ABSORPTION energy, and so on...
                    F = xl.LineEnergy(Z,xl.LB1_LINE)
                    if xl.EdgeEnergy(Z,xl.L2_SHELL) > Beam_Energy:
                            F = xl.LineEnergy(Z,xl.LB1_LINE)
                            if xl.EdgeEnergy(Z,xl.L3_SHELL) > Beam_Energy:
                                    F = xl.LineEnergy(Z,xl.LG1_LINE)
                                    if xl.EdgeEnergy(Z,xl.M1_SHELL) > Beam_Energy:
                                            F = xl.LineEnergy(Z,xl.MA1_LINE)
    return F

#calculate total attenuataion w/ coherent scattering (cm2/g) at beam energy for element in layer
def MatMu(energy, layer):
    layer_elements = layer['Element']                           #get element list from layer                                            
    layer_molFrac = layer['MolFrac']                            #get element molar fraction list from layer
    layer_ele_index = range(len(layer_elements))                #initialize counter for index of element in list of elements inside the LAYER DICTIONARY
    layer_element_mol = 0                                       #initialize amount of element in layer
    for ele in layer_ele_index:
        layer_element_mol += ele_weight(symToNum(layer_elements[ele])) * layer_molFrac[ele]    #
    layer_ele_mu = 0
    for ele in layer_ele_index:
        layer_ele_mu += capXsect(layer_elements[ele], beam_energy) * ele_weight(symToNum(layer_elements[ele])) * layer_molFrac[ele] / layer_element_mol
    return layer_ele_mu

def getSublayers(layer):
    dt = 10 * (1*10**-3) * (1*10**-4)                           #convert 10nm step to cm: 10nm * (1um/1000nm) * (1cm/10000um)
    T = layer['Thick'] * (1/10000)                              #layer thickness in cm (1cm/10000um)
    sublayers = int(T/dt)                                       #number of 10nm sublayers in the layer
    key = 'numSublayers'                                        #add key to layer dictionary (for convenience)
    layer.setdefault(key, sublayers)                            #connect key to number of sublayers calculated
    return

def absorbCorrect(layers, elements):
    IIO_dict = {}
    iio = 1
    for layer in layers:
        #print()
        for EOI in elements:
            if EOI in layer['Element']:
                getSublayers(layer)                                 
                integral = [None]*layer['numSublayers']
                path_in = np.zeros((layer['numSublayers'],1))
                path_out = np.zeros((layer['numSublayers'],1))
                for sublayer in range(layer['numSublayers']):
                    for dx in range(sublayer+1):
                        path_in[dx] = -layer['LDensity'] * MatMu(beam_energy,layer) * dt / beam_geometry
                        path_out[dx] = -layer['LDensity'] * MatMu(XRF_line(EOI,beam_energy), layer) * dt / detect_gemoetry
                    integral[sublayer] = np.exp(np.sum(path_in+path_out))
                iio = iio * np.sum(integral)/layer['numSublayers']
                iio = round(iio, 5)
                key = EOI + '_' + layer['Name']
                IIO_dict.setdefault(key, iio)
    return IIO_dict

IIOs = absorbCorrect(layers, EOIs)



#this is the hard code for this specific example, really need to optimize this...
Cd_total = CDTE['Thick'] + CDS['Thick']
Te_total = CDTE['Thick'] + ZNTE['Thick']

Cd_CdTe_ratio = CDTE['Thick'] / Cd_total
Cd_CdS_ratio = CDS['Thick'] / Cd_total
Te_CdTe_ratio = CDTE['Thick'] / Te_total
Te_ZnTe_ratio = ZNTE['Thick'] / Te_total

#counts_for_Cd_CdTe = df['Cd_L'] * Cd_CdTe_ratio
#counts_for_Cd_S = df['Cd_L'] * Cd_CdS_ratio





# =============================================================================
# for df in smaller_dfs:
#     corrected_Cu = df['Cu'] / IIOs['Cu_Cu']
#     df["Cu"] = corrected_Cu
#     corrected_Cd = df['Cd_L'] / IIOs['Cd_CdTe']
#     df["Cd_L"] = corrected_Cd
#     corrected_Te = df['Te_L'] / IIOs['Te_CdTe']
#     df["Te_L"] = corrected_Te
# =============================================================================

