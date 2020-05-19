# -*- coding: utf-8 -*-
"""
coding: utf-8

tzwalker
Tue May 19 08:15:21 2020

imports masked XBIC and XRF data of cores and boundaries
construct seaborn readable dataframe

imported files created using 'masked-data-save-arrays-to-csv.py'

there is no easy way to contruct the data frame because
the number of data points for each region for each sample
is different

insert 'bksub_' at beginning of file names to get masked standardized data
    (those data aren't too useful; see ppt notes4)
plots violin curves using seaborn package
"""


import pandas as pd

PATH_SYS = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\Core Boundary csvs'

# prepare data and labels
# NBL31 data
PATH_FILE = r'\NBL31_scan341_bound_0in_1out_mask.csv'
PATH_IN = PATH_SYS + PATH_FILE
nbl31_bound = pd.read_csv(PATH_IN, sep=',', names=["XBIC", "Cu", "Cd", "Te","Zn"])
PATH_FILE = r'\NBL31_scan341_cores_0in_mask.csv'
PATH_IN = PATH_SYS + PATH_FILE
nbl31_core = pd.read_csv(PATH_IN, sep=',', names=["XBIC", "Cu", "Cd", "Te","Zn"])

nbl31_label_len = len(nbl31_bound) + len(nbl31_core)
nbl31_label = ['HTLC']*nbl31_label_len
nbl31_core_label = ['Core']*len(nbl31_core)
nbl31_gb_label = ['GBs']*len(nbl31_bound)

# NBL32 data
PATH_FILE = r'\NBL32_scan422_bound_0in_1out_mask.csv'
PATH_IN = PATH_SYS + PATH_FILE
nbl32_bound = pd.read_csv(PATH_IN, sep=',', names=["XBIC", "Cu", "Cd", "Te","Zn"])
PATH_FILE = r'\NBL32_scan422_cores_0in_mask.csv'
PATH_IN = PATH_SYS + PATH_FILE
nbl32_core = pd.read_csv(PATH_IN, sep=',', names=["XBIC", "Cu", "Cd", "Te","Zn"])

nbl32_label_len = len(nbl32_bound) + len(nbl32_core)
nbl32_label = ['HTMC']*nbl32_label_len
nbl32_core_label = ['Core']*len(nbl32_core)
nbl32_gb_label = ['GBs']*len(nbl32_bound)

# NBL33 data
PATH_FILE = r'\NBL33_scan264_bound_0in_1out_mask.csv'
PATH_IN = PATH_SYS + PATH_FILE
nbl33_bound = pd.read_csv(PATH_IN, sep=',', names=["XBIC", "Cu", "Cd", "Te","Zn"])
PATH_FILE = r'\NBL33_scan264_cores_0in_mask.csv'
PATH_IN = PATH_SYS + PATH_FILE
nbl33_core = pd.read_csv(PATH_IN, sep=',', names=["XBIC", "Cu", "Cd", "Te","Zn"])

nbl33_label_len = len(nbl33_bound) + len(nbl33_core)
nbl33_label = ['HTHC']*nbl33_label_len
nbl33_core_label = ['Core']*len(nbl33_core)
nbl33_gb_label = ['GBs']*len(nbl33_bound)

# TS58A data
PATH_FILE = r'\TS58A_scan386_bound_0in_1out_mask.csv'
PATH_IN = PATH_SYS + PATH_FILE
ts58a_bound = pd.read_csv(PATH_IN, sep=',', names=["XBIC", "Cu", "Cd", "Te","Zn"])
PATH_FILE = r'\TS58A_scan386_cores_0in_mask.csv'
PATH_IN = PATH_SYS + PATH_FILE
ts58a_core = pd.read_csv(PATH_IN, sep=',', names=["XBIC", "Cu", "Cd", "Te","Zn"])

ts58a_label_len = len(ts58a_bound) + len(ts58a_core)
ts58a_label = ['LTMC']*ts58a_label_len
ts58a_core_label = ['Core']*len(ts58a_core)
ts58a_gb_label = ['GBs']*len(ts58a_bound)

# construct data frame
sample_labels = nbl31_label + nbl32_label + nbl33_label + ts58a_label
master_df_len = range(len(sample_labels))
column_labels = ['Sample', 'Region',"XBIC", "Cu", "Cd", "Te","Zn"]

master_df = pd.DataFrame(index=master_df_len, columns=column_labels)

master_df['Sample'] = sample_labels

region_labels0 = nbl31_core_label + nbl31_gb_label
region_labels1 = nbl32_core_label + nbl32_gb_label
region_labels2 = nbl33_core_label + nbl33_gb_label
region_labels3 = ts58a_core_label + ts58a_gb_label
region_labels = region_labels0 + region_labels1 + region_labels2 + region_labels3

master_df['Region'] = region_labels

reg0 = pd.concat([nbl31_core,nbl31_bound], ignore_index=True)
reg1 = pd.concat([nbl32_core,nbl32_bound], ignore_index=True)
reg2 = pd.concat([nbl33_core,nbl33_bound], ignore_index=True)
reg3 = pd.concat([ts58a_core,ts58a_bound], ignore_index=True)

region_data = pd.concat([reg0,reg1,reg2,reg3], ignore_index=True)

master_df.update(region_data)

# convert data from object type to numeric type
numeric_columns = ["XBIC", "Cu", "Cd", "Te","Zn"]
master_df[numeric_columns] = master_df[numeric_columns].apply(pd.to_numeric)
#%%
import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

sns.set(style="whitegrid", font='arial', font_scale=1.5)
sns.set_style("ticks", {"xtick.major.size": 10, "ytick.major.size": 10})
ax=sns.violinplot(x='Sample', y='Cu', data=master_df, 
                  hue='Region', split=True, inner="quartile", 
                  linewidth=1, palette="Oranges")
plt.ylim([0,6])
