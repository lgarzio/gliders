#! /usr/bin/env python3

"""
Author: Lori Garzio on 10/23/2023
Last modified: 10/23/2023
"""
import numpy as np
import cmocean as cmo


def glider_extent(lats, lons):
    """
    Calculate the map extents for plotting a glider deployment
    """
    extent = [np.nanmin(lons) - 2, np.nanmax(lons) + 2,
              np.nanmin(lats) - 1.5, np.nanmax(lats) + 1.5]

    return extent

