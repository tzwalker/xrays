# -*- coding: utf-8 -*-
"""

Trumann
Tue May 24 08:37:53 2022

run "main-PVSe33-ASCII-xsect" before this program

this file integrates the maps from 
2021_07_2IDD
scans 72,119,144, or 151

"""


### for infinite cross section integration along length
# =============================================================================
# # scan 119
# df_sums = []
# for df in df_maps:
#     df_arr = np.array(df)
#     df_sum = df_arr.sum(axis=0)
#     df_sums.append(df_sum)
#     
# df_sums_arr = np.array(df_sums).T
# =============================================================================

# =============================================================================
# # scan 151 to match scan length (10um) and resolution (11pts) of scan 119
# keep_pixels = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60]
# 
# df_sums = []
# for df in df_maps:
#     df_arr = np.array(df)
#     df_match = df_arr[keep_pixels, :]
#     df_sum = df_match.sum(axis=0)
#     df_sums.append(df_sum)
# df_sums_arr = np.array(df_sums).T
#     
# =============================================================================


# redo integrate window scan 072 (0hr), apply -2deg rotation

# redo integrate window scan 144 (500hr), apply -2deg rotation

