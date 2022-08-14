import os
import numpy as np
import pandas as pd
import xarray as xr
import rioxarray as rxr

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

from util_myDict_labels import *
from util_read_data import *

#----------------------------------------------------------
def create_summer_average_monthly(ds, sum_mon, sum_mon_str, varname, conv_factor, est_mon_total):
    """Estimate average monthly for summer months
    :param: ds:            xarray
    :param: conv_factor:   conversion factor for each variable
    """

    monthly_data = False
    daily_data   = False

    max_time_step = max(ds.time.dt.day.values)
    if(max_time_step < 31):
       monthly_data = True
    if(max_time_step == 31):
       daily_data = True

    # Scale by conversion factor
    ds            = ds/conv_factor
   
    if(est_mon_total): 
        if(monthly_data):
           # Estimate days in each month
           month_length = ds.time.dt.days_in_month
    
           # Estimate monthly total
           ds = ds * month_length

        if(daily_data):
           # Estimate monthly total
           ds = ds.resample(time='1M', skipna=False).sum(skipna=False)

    # Only keep data for summer months
    ds_summer     = ds.sel(time = ds.time.dt.month.isin(sum_mon))

    # Average monthly (averaging across years)
    ds_summer_avg = ds_summer.groupby('time.month').mean()

    # Modify month coordinates to string
    ds_summer_avg = ds_summer_avg.assign_coords({'month': sum_mon_str})

    # Rename dataarray
    ds_summer_avg = ds_summer_avg.rename(varname)    

    return ds_summer_avg

#----------------------------------------------------------
def create_mean_annual_da(ds, varname, conv_factor, est_mon_total):
    """Estimate mean annual flux from monthly data
    :param: ds:            xarray
    :param: varname:       variable of interest
    :param: conv_factor:   conversion factor for each variable
    """
    
    monthly_data = False
    daily_data   = False

    max_time_step = max(ds.time.dt.day.values)
    if(max_time_step < 31):
       monthly_data = True
    if(max_time_step == 31):
       daily_data = True

    # Scale by conversion factor
    ds            = ds/conv_factor

    if(est_mon_total):
       if(monthly_data):
          # Estimate days in each month
          month_length = ds.time.dt.days_in_month
 
          # Estimate monthly total
          ds = ds * month_length

       # Estimate annual average
       ds_annual     = ds.groupby('time.year').sum(dim='time', skipna=False)  # Annual
    else:
       # Annual average
       ds_annual     = ds.groupby('time.year').mean()
 
    ds_annual_avg = ds_annual.mean(dim='year')               # Annual average

    # Rename dataarray
    ds_annual_avg = ds_annual_avg.rename(varname)    

    #ds_month_max  = ds.max(dim='time')                       # Maximum of monthly averages
   
    # Convert to data set and rename variable
    # ds_annual_avg = ds_annual_avg.to_dataset().rename_vars({varname : 'annual_avg'})
    # ds_month_max  = ds_month_max.to_dataset().rename_vars({varname : 'monthly_max'})
    
    # Merge the two datasets and convert to a data array for spatial plot
    #da_plot = xr.merge([ds_annual_avg, ds_month_max]).to_array('da_plot')
    
    return ds_annual_avg

# -----------------------------------------------------------

def estimate_mean_annual_yield(da, varname):
    """Estimate mean annual yield
    :param: da:         input dataarray
    """

    # Estimate annual average
    da_annual_max = da.groupby('time.year').max(dim='time')
    da_annual_avg = da_annual_max.mean(dim='year')              # Annual average
    
    # Rename dataarray
    da_annual_avg = da_annual_avg.rename(varname)    
   
    return da_annual_avg

# -----------------------------------------------------------
def estimate_mean_annual_dates(da, varname):
    """Estimate mean annual planting and harvest
    :param: da:         input dataarray
    """

    # Replace 999 and 0 (grids with no crops) with nan
    da = da.where(da != 999)  
    da = da.where(da != 0)  

    # Estimate annual average
    da_annual = da.sel(time = da.time.dt.month.isin([12]))
    da_annual_avg = da_annual.mean(dim='time')              # Annual average
    
    # Rename dataarray
    da_annual_avg = da_annual_avg.rename(varname)    
   
    return da_annual_avg

#----------------------------------------------------------
# Clip to Midwest region
def clip_to_midwest_region(ds, var):

   # Polygon geometry for clipping global dataset to the MidWest region
   geometries = [
   {'type': 'Polygon',
    'coordinates': [[
       [-99.25, 37.25],
       [-99.25, 46.75],
       [-82.25, 46.75],
       [-82.25, 37.25],
       [-99.25, 37.25]
    ]]
   }]

   # Assign coordinate reference system (CRS) to dataset
   ds = ds.rename({'lon': 'x', 'lat': 'y'})
   ds = ds.rio.write_crs('epsg:4326', inplace=True)

   # Clip the data
   ds = ds.rio.clip(geometries)
   ds = ds.rename({'x':'lon', 'y':'lat'})

   # Convert from -180 to 180 fomat to 0 to 360 format
   ds.coords['lon'] = (ds.coords['lon'] + 360) % 360
   ds = ds.sortby(ds.lon)

   # Rename dataarray
   ds = ds.rename(var) 

   return(ds)

#----------------------------------------------------------
# Read FluxCom data, estimate mean annual, and assign nan appropriately
def FluxCom_global_estimate_mean_annual(fname, fpath, var):

   # Open FluxCom netCDF data file and load the data into xarray
   ds = read_FluxCom_data(FluxCom_yr_start, FluxCom_yr_end, fpath, fname, var)

   # Estimate mean annual from monthly data
   da_plot = create_mean_annual_da(ds, var, 1, est_mon_total=True)

   # Replace -9999.0 (fill value) with nan
   da_plot = da_plot.where(da_plot != -9999.0)  
   da_plot = da_plot.where(da_plot != 0.0)
   if(var == 'GPP'):
      da_plot = da_plot.where(da_plot > 0.0)

   #print(da_plot.sel(lat=-88.25, lon=-178.25).values)

   return(da_plot)

#----------------------------------------------------------
def estimate_MODIS_annual(ds, varname, annual_stat):

   if (annual_stat == 'sum'):
      # Estimate total annual
      ds_annual = ds.sum(dim='month')  # Annual
   elif (annual_stat == 'mean'):
      # Estimate total annual
      ds_annual = ds.mean(dim='month')  # Annual

   # Rename dataarray
   ds_annual = ds_annual.rename(varname)

   return ds_annual
