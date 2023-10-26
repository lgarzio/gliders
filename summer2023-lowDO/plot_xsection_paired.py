#!/usr/bin/env python

"""
Author: Lori Garzio on 10/23/2023
Last modified: 10/24/2023
Plot cross-sections of data from paired glider deployments with shared axes.
THIS IS A WORK-IN-PROGRESS
"""

import os
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import cmocean as cmo
import functions.plotting as pf
import functions.oxy_colormap_mods as ocm
pd.set_option('display.width', 320, "display.max_columns", 10)  # for display in pycharm console
plt.rcParams.update({'font.size': 13})


def format_date_axis(axis, figure):
    #df = mdates.DateFormatter('%Y-%m-%d')
    df = mdates.DateFormatter('%b-%d\n%H:%M')
    axis.xaxis.set_major_formatter(df)
    figure.autofmt_xdate()


def main(fname1, fname2, fname3, vars, sdir):
    os.makedirs(sdir, exist_ok=True)

    ds1 = xr.open_dataset(fname1)
    ds2 = xr.open_dataset(fname2)
    ds3 = xr.open_dataset(fname3)

    data1 = dict(time=ds1.time.values,
                 depth1=ds1.depth_interpolated.values)
    data2 = dict(time=ds2.time.values,
                 depth2=ds2.depth_interpolated.values)
    data3 = dict(time=ds3.time.values,
                 depth3=ds3.depth_interpolated.values)

    for v in vars:
        try:
            data1[v] = ds1[v].values
        except KeyError:
            print('')
        try:
            data2[v] = ds2[v].values
        except KeyError:
            print('')
        try:
            data3[v] = ds3[v].values
        except KeyError:
            print('')

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)

    dfx = pd.merge(df1, df2, how='outer', on='time')
    df = pd.merge(dfx, df3, how='outer', on='time')
    df = df.sort_values(by='time')
    df.set_index('time', inplace=True)
    df.dropna(how='all', inplace=True)

    # plot temperature from ru39 and ru40
    kwargs = dict()
    kwargs['clabel'] = 'Temperature'
    kwargs['cmap'] = cmo.cm.thermal
    kwargs['title'] = 'ru39'
    kwargs['date_fmt'] = '%b-%d'
    kwargs['vlims'] = [10, 27]
    kwargs['xlabel'] = None
    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(14, 14), sharex=True, sharey=True)
    pf.xsection(fig, ax1, df.index.values, df.depth1, df.temperature_x, **kwargs)

    kwargs['title'] = 'ru40'
    pf.xsection(fig, ax2, df.index.values, df.depth2, df.temperature_y, **kwargs)

    kwargs['title'] = 'ru28'
    pf.xsection(fig, ax3, df.index.values, df.depth3, df.temperature, **kwargs)

    #ax1.invert_yaxis()

    sname = os.path.join(savedir, 'summer2023_rmi_dep_xsection_temp.png')
    plt.savefig(sname, dpi=200)
    plt.close()

    # plot chl from ru39 and ru40
    kwargs = dict()
    kwargs['clabel'] = 'Chlorophyll a (ug/L)'
    kwargs['cmap'] = cmo.cm.algae
    kwargs['title'] = 'ru39'
    kwargs['date_fmt'] = '%b-%d'
    kwargs['vlims'] = None
    kwargs['xlabel'] = None
    fig, (ax1, ax2) = plt.subplots(2, figsize=(14, 12), sharex=True, sharey=True)
    pf.xsection(fig, ax1, df.index.values, df.depth1, df.chlorophyll_a_x, **kwargs)

    kwargs['title'] = 'ru40'
    pf.xsection(fig, ax2, df.index.values, df.depth2, df.chlorophyll_a_y, **kwargs)

    ax1.invert_yaxis()

    sname = os.path.join(savedir, 'summer2023_rmi_paired_xsection_chl.png')
    plt.savefig(sname, dpi=200)
    plt.close()

    # plot DO
    kwargs = dict()
    kwargs['breaks'] = [3, 5]
    #kwargs['green'] = False
    kwargs['blue'] = False
    #mymap = ocm.cm_rygg(**kwargs)  # yellow
    #mymap = ocm.cm_rogg(**kwargs)  # orange
    mymap = ocm.cm_partialturbo_r(**kwargs)

    kwargs = dict()
    kwargs['clabel'] = 'Dissolved Oxygen (mg/L)'
    kwargs['title'] = 'ru40'
    kwargs['cmap'] = mymap  # cmo.cm.oxy  # cmo.cm.deep
    kwargs['date_fmt'] = '%b-%d'
    kwargs['vlims'] = [2, 9]
    kwargs['xlabel'] = None
    #fig, (ax1, ax2) = plt.subplots(2, figsize=(14, 12), sharex=True, sharey=True)
    fig, (ax1, ax2) = plt.subplots(2, figsize=(14, 12))

    do = df.oxygen_concentration_shifted_x * 31.998 / 1000  # convert from umol/L to mg/L
    pf.xsection(fig, ax1, df.index.values, df.depth2, do, **kwargs)

    kwargs['title'] = 'ru28'
    do = df.oxygen_concentration_shifted_y * 31.998 / 1000  # convert from umol/L to mg/L
    pf.xsection(fig, ax2, df.index.values, df.depth3, do, **kwargs)

    #ax1.invert_yaxis()

    sname = os.path.join(savedir, 'summer2023_rmi_dep_xsection_DO.png')
    plt.savefig(sname, dpi=200)
    plt.close()

    # plot pH and omega
    kwargs = dict()
    kwargs['clabel'] = 'pH'
    kwargs['cmap'] = cmo.cm.matter
    kwargs['date_fmt'] = '%b-%d'
    kwargs['vlims'] = None
    kwargs['xlabel'] = None
    fig, (ax1, ax2) = plt.subplots(2, figsize=(14, 12), sharex=True, sharey=True)
    pf.xsection(fig, ax1, df.index.values, df.depth1, df.pH_corrected, **kwargs)

    kwargs['clabel'] = 'Aragonite Saturation State'
    kwargs['cmap'] = cmo.cm.matter
    kwargs['vlims'] = None
    pf.xsection(fig, ax2, df.index.values, df.depth1, df.aragonite_saturation_state, **kwargs)

    # highlight where omega < 1
    dfomega = df[df.aragonite_saturation_state < 1]
    ax2.scatter(dfomega.index.values, dfomega.depth1, c='cyan', s=10, edgecolor='None', alpha=.5)

    ax1.invert_yaxis()

    sname = os.path.join(savedir, 'summer2023_rmi_paired_xsection_pH-omega.png')
    plt.savefig(sname, dpi=200)
    plt.close()


if __name__ == '__main__':
    ncfile1 = '/Users/garzio/Documents/rucool/Saba/gliderdata/2023/ru39-20230817T1520/delayed/ncei/ru39-20230817T1520-delayed-ncei.nc'
    ncfile2 = '/Users/garzio/Documents/rucool/Saba/gliderdata/2023/ru40-20230817T1522/delayed/ru40-20230817T1522-profile-sci-delayed.nc'
    ncfile3 = '/Users/garzio/Documents/rucool/Saba/gliderdata/2023/ru28-20230906T1601/ru28-20230906T1601-profile-sci-rt-slice.nc'
    vars = ['temperature', 'oxygen_concentration_shifted', 'oxygen_saturation_shifted', 'pH_corrected',
            'chlorophyll_a', 'aragonite_saturation_state', 'total_alkalinity']
    savedir = '/Users/garzio/Documents/rucool/Saba/RMI/2023_lowDO_event'
    main(ncfile1, ncfile2, ncfile3, vars, savedir)
