# -*- coding: utf-8 -*-
"""
created: Fri Aug 16 15:14:52 2019
author: Trumann
"""
import numpy as np

def custom_format_ticks(axes_object_labels, string_type):
    txt_labs = [label.get_text() for label in axes_object_labels]
    ticking = [string_type.format(float(txt)) for txt in txt_labs]
    return ticking

def get_real_coordinates(axis_list):
    data_coord = list(axis_list)
    axis_width = max(data_coord) - min(data_coord)
    axis_resolution = np.linspace(0, axis_width, len(data_coord))
    round_steps = [round(i,3) for i in axis_resolution]
    return round_steps


def get_colorbar_axis(c_map, num_of_std):
    M = c_map[:,:-2] # map without nan columns
    heatmap_min = M.mean() - M.std() * num_of_std
    heatmap_max = M.mean() + M.std() * num_of_std
    if heatmap_min < 0:
        heatmap_min = 0
    #if heatmap_max > 1: #for XBIC maximum...
        #heatmap_max = 1
    return heatmap_min, heatmap_max

