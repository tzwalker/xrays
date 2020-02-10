# -*- coding: utf-8 -*-
"""
kineticcross
Sun Feb  9 19:47:25 2020

each sample has a set of scans
each scan has an h5 and a set electrical settings
"""
# how do i import the electrical settings for a given scan?
    # the older code leverages index positions of the sample dict entries...
    # as the electrical settings are not in the h5, it's either use the 
    # index approach of the old code, or import a separate data file to 
    # be used with the corresponding h5...

# ideally, i'd be able to start with a sample dictionary like this:
NBL3_3 = {'Name': 'NBL3_3', 
          'XBIC_scans':     [264,265,266, 475,491], 
          'XBIV_scans':     [261,262,263, 472],
          'STACK': {'Mo':   [10.2, 500E-7], 
                    'ZnTe': [6.34, 375E-7],
                    'Cu':   [8.96, 10E-7], 
                    'CdTe': [5.85, 10.85E-4], 
                    'CdS':  [4.82, 80E-7], 
                    'SnO2': [100E-7]}
          }
      
      
      

