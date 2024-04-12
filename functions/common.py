#! /usr/bin/env python3

"""
Author: Lori Garzio on 10/23/2023
Last modified: 10/26/2023
"""
import numpy as np
import pandas as pd
import cmocean as cmo


def depth_bin(dataframe, depth_var='depth', depth_min=0, depth_max=None, stride=1):
    """
    Written by Mike Smith
    :param dataframe: depth profile in the form of a pandas dataframe
    :param depth_var: the name of the depth variable in the dataframe
    :param depth_min: the shallowest bin depth
    :param depth_max: the deepest bin depth
    :param stride: the amount of space between each bin
    :return: pandas dataframe where data has been averaged into specified depth bins
    """
    depth_max = depth_max or dataframe[depth_var].max()

    bins = np.arange(depth_min, depth_max+stride, stride)  # Generate array of depths you want to bin at
    cut = pd.cut(dataframe[depth_var], bins)  # Cut/Bin the dataframe based on the bins variable we just generated
    binned_df = dataframe.groupby(cut, observed=False).mean()  # Groupby the cut and do the mean
    return binned_df


def glider_extent(lats, lons):
    """
    Calculate the map extents for plotting a glider deployment
    """
    extent = [np.nanmin(lons) - 2, np.nanmax(lons) + 2,
              np.nanmin(lats) - 1.5, np.nanmax(lats) + 1.5]

    return extent

