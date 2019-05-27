import shutil

#enter scan numbers (minimum three digits; make sure they are strings)
scans = ['001', '002']

def copyFrom26IDC():
    mda_src_path = input("Copy network path here: ")
    mda_dst_path = input("Copy destination path here: ")
    for scan in scans:
        file_name = r'\26idbSOFT_0{scan}.mda'.format(scan = scan)
        shutil.copy(mda_src_path + file_name, mda_dst_path)

copyFrom26IDC()