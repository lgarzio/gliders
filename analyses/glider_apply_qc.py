#!/usr/bin/env python

"""
Author: Lori Garzio on 11/8/2023
Last modified: 11/8/2023
Apply QARTOD QC flags to data (set data flagged as 4/FAIL to nan). Set profiles flagged as 3/SUSPECT and 4/FAIL from
CTD hysteresis tests to nan (conductivity, temperature, salinity and density).
"""

import numpy as np
import pandas as pd
import xarray as xr
pd.set_option('display.width', 320, "display.max_columns", 10)  # for display in pycharm console


def main(fname):
    ds = xr.open_dataset(fname)
    try:
        ds = ds.drop_vars(names=['profile_id', 'rowSize'])
    except ValueError as e:
        print(e)
    try:
        ds = ds.swap_dims({'obs': 'time'})
    except ValueError as e:
        print(e)
    ds = ds.sortby(ds.time)
    savefile = f'{fname.split(".nc")[0]}_qc.nc'

    # apply QARTOD QC to all variables except pressure
    qcvars = [x for x in list(ds.data_vars) if '_qartod_summary_flag' in x]
    for qv in qcvars:
        if 'pressure' in qv:
            continue
        target_var = list([qv.split('_qartod_summary_flag')[0]])
        if target_var[0] in ['conductivity', 'temperature']:
            target_var.append('salinity')
            target_var.append('density')
        #qc_idx = np.where(np.logical_or(ds[qv].values == 3, ds[qv].values == 4))[0]
        qc_idx = np.where(ds[qv].values == 4)[0]
        if len(qc_idx) > 0:
            for tv in target_var:
                ds[tv][qc_idx] = np.nan

    # apply CTD hysteresis test QC
    qcvars = [x for x in list(ds.data_vars) if '_hysteresis_test' in x]
    for qv in qcvars:
        target_var = list([qv.split('_hysteresis_test')[0]])
        target_var.append('salinity')
        target_var.append('density')
        qc_idx = np.where(np.logical_or(ds[qv].values == 3, ds[qv].values == 4))[0]
        if len(qc_idx) > 0:
            for tv in target_var:
                ds[tv][qc_idx] = np.nan

    ds.to_netcdf(savefile)


if __name__ == '__main__':
    ncfile = '/Users/garzio/Documents/rucool/Saba/gliderdata/2023/ru40-20230817T1522/delayed/ru40-20230817T1522-profile-sci-rt-slice.nc'
    main(ncfile)
