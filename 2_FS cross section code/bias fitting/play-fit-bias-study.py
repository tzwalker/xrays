import pandas as pd
#from scipy.stats import norm
from astropy import modeling
import matplotlib.pyplot as plt
#from scipy.stats import norm

path_to_ASCIIs = r'C:\Users\Trumann\Desktop\2019_03_2IDD_BIAS\output'

scans = list(range(552,620,2))

def noColNameSpaces(pd_csv_df):
    old_colnames = pd_csv_df.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    pd_csv_df.rename(columns = {i:j for i,j in zip(old_colnames,new_colnames)}, inplace=True)
    return pd_csv_df

def importASCIIS(scans):
    line_scans = []
    usecols = list(range(7))                                            #line plots exported only with ds_ic channel
    for scan in scans:
        s = str(scan)
        filename = r'\line2idd_0'+s+'.h5.csv'
        df = pd.read_csv(path_to_ASCIIs + filename, usecols=usecols)
        noColNameSpaces(df)
        line_scans.append(df)
    return line_scans

dfs = importASCIIS(scans)

lockin = 2000
stanford = 5000*10**-9
scale_factor = stanford / (200000 * lockin)

def collect_XBIC(dfs):
    for df in dfs:
        df["ds_ic[cts/s]"] = df["ds_ic[cts/s]"].astype(float)              #reformat column for floating arithmetic operations
        scaled_dsic = df.loc[:,'ds_ic[cts/s]'] * scale_factor              #apply amplifaction settings  (converts counts to amps)
        df['XBIC'] = scaled_dsic                                           #make new XBIC column          
    return 

collect_XBIC(dfs)

# =============================================================================
# def fit_normal(dfs):
#     mus = []
#     st_devs = []
#     for df in dfs:
#         mu , std = norm.fit(df['ds_ic[cts/s]'])
#         mus.append(mu)
#         st_devs.append(std)
#     return mus, st_devs
# 
# mus, st_devs = fit_normal(dfs)
# =============================================================================
fitter = modeling.fitting.LevMarLSQFitter()     #isolate 
model = modeling.models.Gaussian1D()   #choose gaussian 1D model from model library

def fitGaussians(dfs):
    gauss_models = []
    for df in dfs:
        x = df['pixel_number']
        y = df['XBIC']
        fitted_model = fitter(model, x, y)
        gauss_models.append(fitted_model)
    return gauss_models

fits = fitGaussians(dfs)

# =============================================================================
# #extract amplitudes and positions in fits
# positions_in_pix = []
# amplitudes = []
# for fit in fits:
#     positions_in_pix.append(fit.mean.value)
#     amplitudes.append(fit.amplitude.value)
# 
# #plots all raw data
# for df, fit in zip(dfs, fits):
#     x = df['pixel_number']
#     y = df['XBIC']
#     plt.plot(x, y)
# 
# #plots all fits
# for df, fit in zip(dfs, fits):
#     x = df['pixel_number']
#     plt.plot(x, fit(x))
# 
# #plots raw data and its corresponding fit; NOTE: check the scans that are forward bias or reverse bias...
# for df, fit in zip(dfs, fits):
#     plt.figure()
#     x = df['pixel_number']
#     plt.plot(x, df['XBIC'])
#     plt.plot(x, fit(x))
# =============================================================================
