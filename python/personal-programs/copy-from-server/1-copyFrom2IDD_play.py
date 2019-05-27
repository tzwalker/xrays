import shutil

def copyFrom2IDD(server_parent, local_parent):
    mda_src_path = server_parent + r"\mda"
    mda_dst_path = local_parent + r"\mda"
    h5_src_path = server_parent + r"\img.dat"
    h5_dst_path = local_parent + r"\img.dat"
    fly_src_path = server_parent + r"\flyXRF"
    fly_dst_path = local_parent + r"\flyXRF"
    for scan, point in zip(scans, points):
        mdaFilename = r"\2idd_0" + scan + ".mda"
        h5Filename = r"\2idd_0" + scan + ".h5"
        shutil.copy(mda_src_path + mdaFilename, mda_dst_path + mdaFilename)
        shutil.copyfile(h5_src_path + h5Filename, h5_dst_path + h5Filename)
        for p in range(points):
            findfly = r"\2idd_0{a}_2iddXMAP__{b}.nc".format(a=scan, b=p)
            shutil.copy(fly_src_path + findfly, fly_dst_path)
    return

def copyFrom26IDC():
    mda_src_path = input("Copy network path here: ")
    mda_dst_path = input("Copy destination path here: ")
    for scan in scans:
        file_name = r'\26idbSOFT_0{scan}.mda'.format(scan = scan)
        shutil.copy(mda_src_path + file_name, mda_dst_path)
    return


def copyFromNet(online, local):
    if sector == 2:
        copyFrom2IDD(online, local)
    else:
        copyFrom26IDC(online, local)
    return

sector = 2
scans = ['060','061','063']
points = [18, 11, 21]

server_parent_path = '\\\\en4093310.ecee.dhcp.asu.edu\\Lab\Synchrotron Data\\2017_12_2IDD\\raw'
local_parent_path = r'C:\Users\Trumann\Desktop\XANES'

copyFromNet(server_parent_path, local_parent_path)
