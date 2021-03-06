"""

This script will import the scans of interest from the raw data directories (hopefully). 

PLEASE READ:
  
  Make sure all destination and source directories have read/write permissions enabled.
  
  Make sure your directories are correct. Network directories must have full network path, not the
    'mapped' drive letter Windows or the native OS assigns to the network drive; e.g. \\server\server
    
    folders must already exist in the destination
    
  Scan position must match point position in the scans/points list!!!
  
"""
import shutil

# code for Sector 2
def sector_2_import(scans):
    for scan in scans:
        findMDA = r"\2idd_0" +scan + ".mda"
        findH5 = r"\2idd_0" + scan + ".h5"
        shutil.copyfile(MDAsource + findMDA, MDAdest + findMDA)
        shutil.copyfile(H5source + findH5, H5dest + findH5)
    for scan, point in zip(scans, points):  
      for p in range(point):
        findfly = r"\2idd_0{a}_2iddXMAP__{b}.nc".format(a=scan, b=p)
        shutil.copyfile(flysource + findfly, flydest + findfly)
    return

# code for Sector 26
def sector_26_import(scans):
    for scan in scans:
        findMDA = r"\26idbSOFT_0" +scan + ".mda"
        shutil.copyfile(MDAsource + findMDA, MDAdest + findMDA)
    return

## enter scans and corresponding (y) points of the scan
scans_in = list(range(328,334)) + list(range(337,346)) #start from scan 328 and go until 334
scans = []
for s in scans_in:
    s = str(s)
    scans.append(s)
    
points = []
for scan in scans:
    p = 201
    points.append(p)


## enter directories; source --> server directory, dest --> local directory
MDAsource =     r'\\en4093310.ecee.dhcp.asu.edu\BertoniLab\Lab\Synchrotron Data\2019_06_2IDD\mda'
MDAdest =       r'C:\Users\Trumann\Desktop\2019_06_2IDD_stage\mda'

H5source =      r'\\en4093310.ecee.dhcp.asu.edu\BertoniLab\Lab\Synchrotron Data\2019_06_2IDD\img.dat'
H5dest =        r'C:\Users\Trumann\Desktop\2019_06_2IDD_stage\img.dat'

flysource =     r'\\en4093310.ecee.dhcp.asu.edu\BertoniLab\Lab\Synchrotron Data\2019_06_2IDD\flyXRF'
flydest =       r'C:\Users\Trumann\Desktop\2019_06_2IDD_stage\flyXRF'


## comment/uncomment function for correct Sector code for Sector which you did not visit
sector_2_import(scans)
#sector_26_import(scans)

