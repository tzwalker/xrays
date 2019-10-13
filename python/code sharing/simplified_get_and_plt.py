### path to custom functions/defintions (defs) ###
import sys
# the path below must contain the file "import_maps_H5.py"
# if "import_maps_H5.py" is in the same directory as this program ("simplified_get_and_plt.py"),
  # then you can comment out lines 2-7 in this file, including this comment you're reading
  # if an error is thrown saying something like 'no module exists', then follow comment on line 4
custom_def_path = r'C:\Users\Trumann\Desktop\xrays\python\personal-programs\twalker_defs'
sys.path.append(custom_def_path)

import import_maps_H5 # grabs custom defs

### path for files/scans ###
# the path below must contain the H5 files of interest
   # H5 filnames should in the form: "\2idd_001.h5" 
   # this code is not configureed for Sector 26 data, but yo can modify
      # def "import_h5s" in "import_maps_h5s.py" to reflect the proper filename string
scan_path = r'C:\Users\Trumann\Desktop\2019_03_2IDD_NBL3\img.dat'

# enter desired scan number as a three-digit string (e.g. '001' or '089')
scans = ['264', '422', '385']

# enter desired element channels_of_interest (ChOIs)
ChOIs = ['Cd_L', 'Te_L', 'Cu']

### import raw data ###
# the "." goes into the file "import_maps_H5.py" and grabs the def "import_h5s"
files = import_maps_H5.import_h5s(scans, scan_path) 
master_index_list = import_maps_H5.get_ChOIs_for_all_scans(files, ChOIs)
master_map_list = import_maps_H5.extract_maps(files, master_index_list)

# at this point you should have a list containing 2D matrices of the maps of interest for each scan
# each scan is represented by a list within "master_map_list"

# i'm going to leave it to you to figure out plotting