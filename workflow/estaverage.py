"""
Python modules for estimating average of xarray over various time periods
"""

import numpy as np
import pandas as pd
import xarray as xr

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

#----------------------------------------------------------
def estimate_daily_average(ds):
    """Aggregate hourly data for each day and estimate daily mean
    :param: ds:         input data array

    :return:            output data array
    """
    # Estimate average for each day
    ds_new = ds.resample(time='1D').mean()

    # Copy attributes
    for var in ds.data_vars:
        ds_new[var].attrs = ds[var].attrs

    return (ds_new)

#----------------------------------------------------------
def estimate_daily_average_across_years(ds):
    """Estimate average across years for each day of the year
    :param: ds:         input data array

    :return:            output data array
    """
    # Estimate average for each day
    ds_new = ds.groupby('time.dayofyear').mean('time')

    # Copy attributes
    for var in ds.data_vars:
        ds_new[var].attrs = ds[var].attrs

    return (ds_new)

#----------------------------------------------------------
def estimate_monthly_average(ds):
    """Estimate average across years for each month
    :param: ds:         input data array

    :return:            output data array
    """
    # Estimate monthly average
    ds_new = ds.groupby('time.month').mean('time')

    # Copy attributes
    for var in ds.data_vars:
        ds_new[var].attrs = ds[var].attrs

    return (ds_new)

#----------------------------------------------------------
def estimate_annual_max(ds):
    """Estimate maximum for each year then average across years
    :param: ds:         input data array

    :return:            output data array
    """
    # Estimate maximum value for each year
    ds_new = ds.groupby('time.year').max()

    # Estimate average across years
    ds_new = ds_new.mean('year')

    # Copy attributes
    for var in ds.data_vars:
        ds_new[var].attrs = ds[var].attrs

    return (ds_new)
