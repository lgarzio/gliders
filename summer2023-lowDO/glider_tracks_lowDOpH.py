#!/usr/bin/env python

"""
Author: Lori Garzio on 10/26/2023
Last modified: 11/1/2023
Plot glider tracks for the low DO/pH event in summer 2023, with the areas of low DO and omega or pH highlighted.
Also plot locations of reported fish/crab/lobster mortalities.
"""

import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cmocean as cmo
import cool_maps.plot as cplt
plt.rcParams.update({'font.size': 14})
pd.set_option('display.width', 320, "display.max_columns", 10)  # for display in pycharm console


def main(flist, extent, sfilename):
    # grab locations from gliders and merge into one dataframe
    data = dict()
    deployments = []
    plot_vars = ['oxygen_concentration_shifted', 'aragonite_saturation_state']  # 'aragonite_saturation_state'  'pH_corrected'
    for f in flist:
        ds = xr.open_dataset(f)
        deploy = ds.trajectory.values[0]
        deployments.append(deploy)
        data[deploy] = dict()
        data[deploy]['lon'] = ds.longitude.values
        data[deploy]['lat'] = ds.latitude.values
        for pv in plot_vars:
            try:
                data[deploy][pv] = ds[pv].values
            except KeyError:
                continue

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

    for key, values in data.items():
        df = pd.DataFrame(values)
        #ax.scatter(df.lon, df.lat, color='#595959', marker='.', s=10, transform=ccrs.PlateCarree(), zorder=5)  # dark gray
        ax.plot(df.lon, df.lat, color='#595959', linewidth=2, transform=ccrs.PlateCarree(), zorder=5)  # dark gray

        # plot locations where omega < 1
        if 'aragonite_saturation_state' in df.columns:
            df = df[df.aragonite_saturation_state < 1]
            ax.scatter(df.lon, df.lat, c='cyan', marker='.', s=150, transform=ccrs.PlateCarree(), zorder=10)

        # # plot locations where pH < 1
        # if 'pH_corrected' in df.columns:
        #     df = df[df.pH_corrected < 7.75]
        #     ax.scatter(df.lon, df.lat, c='magenta', marker='.', s=150, transform=ccrs.PlateCarree(), zorder=10)

        # plot locations where DO < 3 mg/L
        elif 'oxygen_concentration_shifted' in df.columns:
            df = df[df.oxygen_concentration_shifted * 31.998 / 1000 < 3]
            ax.scatter(df.lon, df.lat, c='magenta', marker='.', s=150, transform=ccrs.PlateCarree(), zorder=10)

    # plot locations of reported fish/crab/lobster mortalities
    ax.scatter(-73.525, 40.025, marker='X', c='r', edgecolors='k', s=200, transform=ccrs.PlateCarree(), zorder=10)  # Lillian wreck
    ax.scatter(-73.7, 40.167, marker='X', c='r', edgecolors='k', s=200, transform=ccrs.PlateCarree(), zorder=10)  # Mud Hole
    ax.scatter(-73.947, 40.123, c='r', marker='X', edgecolors='k', s=200, transform=ccrs.PlateCarree(), zorder=10)  # Middle of Sea Girt artificial reef
    ax.scatter(-73.985, 40.048, c='r', marker='X', edgecolors='k', s=200, transform=ccrs.PlateCarree(), zorder=10)  # Middle of Axel Carlson reef

    # seagirt_lons = [-73.928333, -73.9275, -73.945, -73.951667, -73.9575, -73.9525, -73.928333]
    # seagirt_lats = [40.144167, 40.136667, 40.121667, 40.102667, 40.103, 40.125, 40.144167]
    # ax.fill(seagirt_lons, seagirt_lats, color='r', edgecolor='black', transform=ccrs.PlateCarree(), zorder=10)
    #
    # axel_lons = [-73.994167, -73.976667, -73.991667, -74.01, -73.994167]
    # axel_lats = [40.068333, 40.0605, 39.996667, 40.005, 40.068333]
    # ax.fill(axel_lons, axel_lats, color='r', edgecolor='black', transform=ccrs.PlateCarree(), zorder=10)

    # Lillian wreck https://www.thebassbarn.com/threads/triple-wrecks-and-lillian.184597/
    # Mud Hole https://www.thefisherman.com/hot-spot/mud-hole/#:~:text=The%20Mud%20Hole's%20trench%20tells,of%2080%20or%2090%20feet.
    # Sea Girt artifical reef https://www.thefisherman.com/article/hot-spot-sea-girt-reef/
    # Axel Carlson Reef https://www.thefisherman.com/hot-spot/axel-carlson-reef/, https://njscuba.net/artificial-reefs/new-jersey-reefs/axel-carlson-reef/

    plt.savefig(sfilename, dpi=200)
    plt.close()


if __name__ == '__main__':
    file_list = ['/Users/garzio/Documents/rucool/Saba/gliderdata/2023/ru39-20230817T1520/delayed/ncei/ru39-20230817T1520-delayed-ncei.nc',
             '/Users/garzio/Documents/rucool/Saba/gliderdata/2023/ru40-20230817T1522/delayed/ru40-20230817T1522-profile-sci-delayed.nc',
             '/Users/garzio/Documents/rucool/Saba/gliderdata/2023/ru28-20230906T1601/ru28-20230906T1601-profile-sci-rt-slice.nc']
    map_extent = [-75, -72.25, 38.5, 40.75]
    savefile = '/Users/garzio/Documents/rucool/Saba/RMI/2023_lowDO_event/rmi_dep_deployments_202308-lowDO-magenta-omega-cyan.png'
    main(file_list, map_extent, savefile)
