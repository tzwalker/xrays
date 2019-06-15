import xraylib as xl
#returns a list of dictionaries
#each dictionary contains information on the layer to be used in the absorption correction
def get_stack_info(STACK, layer_density, E):
    STACK_dicts = []
    for layer, dens in zip(STACK, layer_density):
        layer_dict = dict()
        key = 'Name'
        layer_dict.setdefault(key, layer)
        
        key = 'rho'
        layer_dict.setdefault(key, dens)
        
        key = 'cap-x-sect'
        capture = xl.CS_Total_CP(layer, E)
        layer_dict.setdefault(key, capture)
        
        for ###
        key = 'thick'
        layer_dict.setdefault(key, )
        
        layer_info = xl.CompoundParser(layer)
        #example for SnO2
        #layer_info = {'nElements': 2, 
                        #'nAtomsAll': 3.0, 
                        #'Elements': [8, 50], 
                        #'massFractions': [0.21235649346340169, 0.7876435065365983], 
                        #'nAtoms': [2.0, 1.0], 
                        #'molarMass': 150.69}
        layer_dict.update(layer_info)
        
        STACK_dicts.append(layer_dict)
    return STACK_dicts


#ahhh!!! if i want to make a code that can adjust for different thicknesses of CdTe
    #i all of a sudden have lists of two different length here...
    
# first i was making a list of dicts where each dict was a layer

# now i want a list containing lists for a scan that contain the 
    #stack_info for that scan
