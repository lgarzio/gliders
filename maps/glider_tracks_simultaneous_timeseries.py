#!/usr/bin/env python

"""
Author: Lori Garzio on 10/25/2023
Last modified: 10/25/2023
Plot glider tracks that are deployed simultaneously. Glider tracks are colored by time. If the map extent is not
specified, it will be provided using the glider data
"""

import numpy as np
import xarray as xr
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cartopy.crs as ccrs
import cmocean as cmo
import cool_maps.plot as cplt
import functions.common as cf
plt.rcParams.update({'font.size': 14})
pd.set_option('display.width', 320, "display.max_columns", 10)  # for display in pycharm console


def main(flist, extent, sfilename):
    # grab locations from gliders and merge into one dataframe
    data = dict()
    deployments = []
    for f in flist:
        ds = xr.open_dataset(f)
        deploy = ds.trajectory.values[0]
        deployments.append(deploy)
        data[deploy] = dict(time=ds.time.values)
        data[deploy][f'lon_{deploy}'] = ds.longitude.values
        data[deploy][f'lat_{deploy}'] = ds.latitude.values

    df_list = []
    for k, v in data.items():
        df_list.append(pd.DataFrame(v))

    # merge all dataframes on time
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['time'], how='outer'), df_list)

    # define the plotting limits based on the glider data if the extent is not provided
    if not extent:
        latcols = [col for col in df_merged.columns if 'lat_' in col]
        loncols = [col for col in df_merged.columns if 'lon_' in col]
        extent = cf.glider_extent(df_merged[latcols], df_merged[loncols])

    kwargs = dict()
    kwargs['landcolor'] = 'none'
    kwargs['oceancolor'] = 'none'
    #kwargs['coast'] = 'low'
    fig, ax = cplt.create(extent, **kwargs)

    # add bathymetry
    bathymetry = '/Users/garzio/Documents/rucool/bathymetry/GEBCO_2014_2D_-100.0_0.0_-10.0_50.0.nc'
    bathy = xr.open_dataset(bathymetry)
    bathy = bathy.sel(lon=slice(extent[0] - .1, extent[1] + .1),
                      lat=slice(extent[2] - .1, extent[3] + .1))
    levels = np.arange(-5000, 5100, 50)
    bath_lat = bathy.lat
    bath_lon = bathy.lon
    bath_elev = bathy.elevation
    plt.contourf(bath_lon, bath_lat, bath_elev, levels, cmap=cmo.cm.topo, transform=ccrs.PlateCarree())

    levels = np.arange(-100, 0, 50)
    CS = plt.contour(bath_lon, bath_lat, bath_elev, levels, linewidths=.75, alpha=.5, colors='k',
                     transform=ccrs.PlateCarree())
    ax.clabel(CS, [-100], inline=True, fontsize=7, fmt='%d')

    # add glider tracks
    # have to change the nans to zero to get the times to line up for all glider deployments.
    # this could be a problem when flying gliders near the equator
    df_merged = df_merged.fillna(0)

    df_merged.set_index('time', inplace=True)
    for d in deployments:
        cols = [x for x in df_merged if d in x]
        df = df_merged[cols]

        ax.scatter(df[f'lon_{d}'], df[f'lat_{d}'], color='k', marker='.', s=75, transform=ccrs.PlateCarree(), zorder=10)
        sct = ax.scatter(df[f'lon_{d}'], df[f'lat_{d}'], c=df.index.values, marker='.', s=25, cmap='rainbow',
                         transform=ccrs.PlateCarree(), zorder=10, label='ru39')

    # Set colorbar height equal to plot height
    divider = make_axes_locatable(ax)
    cax = divider.new_horizontal(size='5%', pad=0.05, axes_class=plt.Axes)
    fig.add_axes(cax)

    # generate colorbar
    cbar = plt.colorbar(sct, cax=cax)
    cbar.ax.set_yticklabels(pd.to_datetime(cbar.ax.get_yticks()).strftime(date_format='%Y-%m-%d'))

    plt.savefig(sfilename, dpi=200)
    plt.close()


if __name__ == '__main__':
    file_list = ['/Users/garzio/Documents/rucool/Saba/gliderdata/2023/ru39-20230817T1520/delayed/ncei/ru39-20230817T1520-delayed-ncei.nc',
             '/Users/garzio/Documents/rucool/Saba/gliderdata/2023/ru40-20230817T1522/delayed/ru40-20230817T1522-profile-sci-delayed.nc',
             '/Users/garzio/Documents/rucool/Saba/gliderdata/2023/ru28-20230906T1601/ru28-20230906T1601-profile-sci-rt-slice.nc']
    map_extent = [-75, -72.25, 38.5, 40.75]  # None or list [-75, -72.25, 38.5, 40.75]
    savefile = '/Users/garzio/Documents/rucool/Saba/RMI/2023_lowDO_event/rmi_dep_deployments_202308-test.png'
    main(file_list, map_extent, savefile)
