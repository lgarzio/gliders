#!/usr/bin/env python

"""
Author: Lori Garzio on 1/11/2022
Last modified: 11/8/2023
Modified from code from Sam Coakley following theory from Carvalho et al 2016 https://doi.org/10.1002/2016GL071205
Calculate Mixed Layer Depth for glider profiles using density and pressure, then add the MLD variable to the .nc file.
The dataset provided must have 'time' or 'profile_time' as the only coordinate in order to convert the dataset to a
dataframe properly
"""

import os
import datetime as dt
import xarray as xr
import numpy as np
import pandas as pd
import gsw
import matplotlib.pyplot as plt
import functions.common as cf
import functions.mixed_layer_depth as mldfunc
plt.rcParams.update({'font.size': 14})
pd.set_option('display.width', 320, "display.max_columns", 20)  # for display in pycharm console


def main(fname, timevar, plots, mldvar, zvar):
    mld = np.array([], dtype='float32')
    max_n2 = np.array([], dtype='float32')

    savefile = f'{fname.split(".nc")[0]}_mld.nc'

    ds = xr.open_dataset(fname)
    ds = ds.sortby(ds.time)
    deploy = ds.title

    df = ds.to_dataframe()

    # remove data (pressure plus the variable you're using to calculate MLD) that's collected at the surface (< 1 dbar)
    df.loc[df.pressure < 1, ['pressure', mldvar]] = np.nan
    grouped = df.groupby(timevar, dropna=False)

    if plots:
        plots = os.path.join(plots, 'mld_analysis', deploy)
        os.makedirs(plots, exist_ok=True)

    for group in grouped:
        # Create temporary dataframe to interpolate to dz m depths
        ll = len(group[1])
        kwargs = {'depth_var': zvar}
        temp_df1 = group[1][[mldvar, zvar, 'temperature']].dropna(how='all')
        if len(temp_df1) == 0:
            mldx = np.repeat(np.nan, ll)
            max_n2x = np.repeat(np.nan, ll)
        else:
            temp_df = cf.depth_bin(temp_df1, **kwargs)
            temp_df.dropna(subset=[mldvar], inplace=True)
            temp_df.index.name = f'{zvar}_bins'
            temp_df.reset_index(inplace=True)
            if len(temp_df) == 0:
                mldx = np.repeat(np.nan, ll)
                max_n2x = np.repeat(np.nan, ll)
                qi = 'MLD not calculated'
            else:
                # calculate profile's pressure range
                pressure_range = (np.nanmax(temp_df[zvar]) - np.nanmin(temp_df[zvar]))

                if pressure_range < 5:
                    # if the profile spans <5 dbar, don't calculate MLD
                    mldx = np.repeat(np.nan, ll)
                    max_n2x = np.repeat(np.nan, ll)
                    qi = 'MLD not calculated'

                else:
                    kwargs = {'zvar': zvar}
                    mldx, N2, qi = mldfunc.profile_mld(temp_df, **kwargs)
                    mldx = np.repeat(mldx, ll)
                    max_n2x = np.repeat(N2, ll)

            if plots:
                try:
                    tstr = group[0].strftime("%Y-%m-%dT%H%M%SZ")
                except AttributeError:
                    tstr = pd.to_datetime(np.nanmin(group[1].time)).strftime("%Y-%m-%dT%H%M%SZ")
                # plot temperature
                fig, ax = plt.subplots(figsize=(8, 10))
                ax.scatter(temp_df['temperature'], temp_df[zvar])

                ax.invert_yaxis()
                ax.set_ylabel('Pressure (dbar)')
                ax.set_xlabel('temperature')

                ax.axhline(y=np.unique(mldx), ls='--', c='k')

                sfile = os.path.join(plots, f'temperature_{tstr}.png')
                plt.savefig(sfile, dpi=300)
                plt.close()

                # plot density
                fig, ax = plt.subplots(figsize=(8, 10))
                ax.scatter(temp_df['density'], temp_df[zvar])

                ax.invert_yaxis()
                ax.set_ylabel('Pressure (dbar)')
                ax.set_xlabel('density')
                ax.set_title(f'QI = {qi}\nN2 = {np.unique(max_n2x)[0]}')

                ax.axhline(y=np.unique(mldx), ls='--', c='k')

                sfile = os.path.join(plots, f'density{tstr}.png')
                plt.savefig(sfile, dpi=300)
                plt.close()

        mld = np.append(mld, mldx)
        max_n2 = np.append(max_n2, max_n2x)

    # add mld to the dataset
    mld_min = np.nanmin(mld)
    mld_max = np.nanmax(mld)
    attrs = {
        'actual_range': np.array([mld_min, mld_max]),
        'ancillary_variables': [mldvar, zvar],
        'observation_type': 'calculated',
        'units': ds[zvar].units,
        'comment': 'Mixed Layer Depth calculated as the depth of max Brunt‐Vaisala frequency squared (N**2) '
                   'from Carvalho et al 2016 (https://doi.org/10.1002/2016GL071205)',
        'long_name': 'Mixed Layer Depth'
        }
    da = xr.DataArray(mld, coords=ds[mldvar].coords, dims=ds[mldvar].dims,
                      name='mld_dbar', attrs=attrs)
    ds['mld_dbar'] = da

    # calculate MLD in meters
    mld_meters = gsw.z_from_p(-ds.mld_dbar.values, ds.latitude.values)

    attrs = {
        'actual_range': np.array([np.nanmin(mld_meters), np.nanmax(mld_meters)]),
        'observation_type': 'calculated',
        'units': 'm',
        'comment': 'Mixed Layer Depth calculated as the depth of max Brunt‐Vaisala frequency squared (N**2) from '
                   'Carvalho et al 2016 (https://doi.org/10.1002/2016GL071205). Calculated from MLD in dbar and latitude using gsw.z_from_p',
        'long_name': 'Mixed Layer Depth'
    }
    da = xr.DataArray(mld_meters, coords=ds.mld_dbar.coords, dims=ds.mld_dbar.dims,
                      name='mld', attrs=attrs)
    ds['mld'] = da

    # add maximum buoyancy frequency N2 (measure of stratification strength) to the dataset
    n2_min = np.nanmin(max_n2)
    n2_max = np.nanmax(max_n2)
    attrs = {
        'actual_range': np.array([n2_min, n2_max]),
        'ancillary_variables': [mldvar, zvar],
        'observation_type': 'calculated',
        'units': 's-2',
        'comment': 'Maximum Brunt‐Vaisala frequency squared (N**2) for each profile used to calculate Mixed Layer Depth '
                   'from Carvalho et al 2016 (https://doi.org/10.1002/2016GL071205). This can be used as a measurement '
                   'for stratification strength',
        'long_name': 'Maximum Buoyancy Frequency'
    }
    da = xr.DataArray(max_n2, coords=ds[mldvar].coords, dims=ds[mldvar].dims,
                      name='max_n2', attrs=attrs)
    ds['max_n2'] = da

    ds.to_netcdf(savefile)


if __name__ == '__main__':
    ncfile = '/Users/garzio/Documents/rucool/Saba/gliderdata/2023/ru39-20230817T1520/delayed/ncei/ru39-20230817T1520-delayed-ncei.nc'  # striper-20170907T1430.nc ru30-20180705T1825.nc
    time_variable = 'profile_time'  # time variable on which groups are generated (e.g. profile_time)
    generate_plots = False # '/Users/garzio/Documents/rucool/Saba/gliderdata/2023/ru39-20230817T1520/delayed/ncei'  # False or save_directory e.g. '/Users/garzio/Documents/rucool/Saba/gliderdata/plots'
    mldvar = 'density'  # variable used to calculate MLD
    zvar = 'pressure'  # pressure variable
    main(ncfile, time_variable, generate_plots, mldvar, zvar)
