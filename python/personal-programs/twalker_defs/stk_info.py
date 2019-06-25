import xraylib as xl


def get_stack_info(STACKS, dens, T, E):
    stack_whole_info = []
    for S, D, t, e in zip(STACKS, dens, T, E):
        stack_layer_infos = []
        for layer, density, thickness in zip(S, D, t): 
            scan_layer_dict = dict()
            key = 'Name'
            scan_layer_dict.setdefault(key, layer)
            
            key = 'rho'
            scan_layer_dict.setdefault(key, density)
        
            key = 'cap-x-sect'
            capture = xl.CS_Total_CP(layer, e)
            scan_layer_dict.setdefault(key, capture)
    
            key = 'thick'
            scan_layer_dict.setdefault(key, thickness)
            
            layer_info = xl.CompoundParser(layer)
        #example for SnO2
        #layer_info = {'nElements': 2, 
                        #'nAtomsAll': 3.0, 
                        #'Elements': [8, 50], 
                        #'massFractions': [0.21235649346340169, 0.7876435065365983], 
                        #'nAtoms': [2.0, 1.0], 
                        #'molarMass': 150.69}
            scan_layer_dict.update(layer_info)
            stack_layer_infos.append(scan_layer_dict)
        
        stack_whole_info.append(stack_layer_infos)
    return stack_whole_info


#ahhh!!! if i want to make a code that can adjust for different thicknesses of CdTe
    #i all of a sudden have lists of two different length here...
    
# first i was making a list of dicts where each dict was a layer

# now i want a list containing lists for a scan that contain the 
    #stack_info for that scan
