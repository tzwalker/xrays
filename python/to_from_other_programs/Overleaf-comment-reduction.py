# -*- coding: utf-8 -*-
"""

Trumann
Sun Jul 31 10:04:31 2022


"""

FILE = r"C:\Users\Trumann\Dropbox (ASU)\DefectLab\Group Written Works\20220730 SRojsatien_CuXANES full comment export - Copy.txt"

OUT = r"C:\Users\Trumann\Dropbox (ASU)\DefectLab\Group Written Works\20220730 SRojsatien_CuXANES full comment export - Copy - Copy.txt"

# with is like your try .. finally block in this case
with open(FILE, 'r') as file:
    # read a list of lines into data
    data = file.readlines()
    
new = []
for line in data:
    if line[:7] == 'Changed':
        line = ' ' 
    elif line[:3] == 'Hit':
        line = ' '
    elif line[:3] == 'Jul':
        line = ' '
    elif line[:3] == 'May':
        line = ' '
        
    
    new.append(line)
        
with open(OUT, 'w') as file:
    file.writelines(new)