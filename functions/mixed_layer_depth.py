#! /usr/bin/env python3

import numpy as np


def gap(prange):
    """
    :param prange: pressure range of the profile
    :return: the maximum allowable data gap for the profile
    """
    if prange < 20:
        gap_threshold = 8
    elif 20 <= prange < 50:
        gap_threshold = 10
    elif 50 <= prange < 200:
        gap_threshold = 25
    elif 200 <= prange < 500:
        gap_threshold = 50
    else:
        gap_threshold = 75

    return gap_threshold


def profile_mld(df, mld_var='density', zvar='pressure', qi_threshold=0.5):
    """
    Written by Sam Coakley and Lori Garzio, Jan 2022
    Calculates the Mixed Layer Depth (MLD) for a single profile as the depth of max Brunt‐Vaisala frequency squared
    (N**2) from Carvalho et al 2016 (https://doi.org/10.1002/2016GL071205)
    :param df: depth profile in the form of a pandas dataframe
    :param mld_var: the name of the variable for which MLD is calculated, default is 'density'
    :param zvar: the name of the depth variable in the dataframe, default is 'pressure'
    :param qi_threshold: quality index threshold for determining well-mixed water, default is 0.5
    :return: the depth of the mixed layer in the units of zvar and the max buoyancy frequency in units of s-2
    """
    df.dropna(subset=[mld_var], inplace=True)
    pN2 = np.sqrt(9.81 / np.nanmean(df[mld_var]) * np.diff(df[mld_var], prepend=np.nan) / np.diff(df[zvar], prepend=np.nan)) ** 2
    if len(df) < 5:  # if there are <5 data bins, don't calculate MLD
        mld = np.nan
        maxN2 = np.nan
    elif np.sum(~np.isnan(pN2)) < 3:  # if there are <3 values calculated for pN2, don't calculate MLD
        mld = np.nan
        maxN2 = np.nan
    elif np.nanmax(np.diff(df[zvar])) > gap(np.nanmax(df[zvar]) - np.nanmin(df[zvar])):
        # if there is a gap in the profile that exceeds the defined threshold, don't calculate MLD
        mld = np.nan
        maxN2 = np.nan
    else:
        pressure_range = [np.nanmin(df[zvar]), np.nanmax(df[zvar])]

        maxN2 = np.nanmax(pN2)
        mld_idx = np.where(pN2 == maxN2)[0][0]

        # if the code finds the first or last data point to be the max pN2, return nan
        if np.logical_or(mld_idx == 0, mld_idx == len(df) - 1):
            mld = np.nan
            maxN2 = np.nan
        else:
            mld = np.nanmean([df[zvar][mld_idx], df[zvar][mld_idx + 1]])

            if mld < 5:
                # if MLD is <5, return nan
                mld = np.nan
                maxN2 = np.nan
            elif np.logical_or(mld < pressure_range[0] + 2, mld > pressure_range[1] - 2):
                # if MLD is within 2 dbar of the top or bottom of the profile, return nan
                mld = np.nan
                maxN2 = np.nan
            else:
                if qi_threshold:
                    # find MLD  1.5
                    mld15 = mld * 1.5
                    mld15_idx = np.argmin(np.abs(df[zvar] - mld15))

                    # Calculate Quality index (QI) from Lorbacher et al, 2006
                    surface_mld_values = df[mld_var][0:mld_idx]  # values from the surface to MLD
                    surface_mld15_values = df[mld_var][0:mld15_idx]  # values from the surface to MLD * 1.5

                    qi = 1 - (np.std(surface_mld_values - np.nanmean(surface_mld_values)) /
                              np.std(surface_mld15_values - np.nanmean(surface_mld15_values)))

                    if qi < qi_threshold:
                        # if the Quality Index is < the threshold, this indicates well-mixed water so don't return MLD
                        mld = np.nan
                        maxN2 = np.nan

    return mld, maxN2
